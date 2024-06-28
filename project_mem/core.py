import os
import time
import base64

from minio import Minio
from sqlalchemy import func, select

from db_models import session_db, Mem


ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']


client = Minio(str(os.getenv("MINIO_URL")),
               access_key=os.getenv("MINIO_ACCESS_KEY"),
               secret_key=os.getenv("MINIO_SECRET_KEY"),
               secure=False
               )


def create_bucket_not_exists(bucket_name):
    if not client.bucket_exists(bucket_name):
        try:
            client.make_bucket(bucket_name)
        except Exception as e:
            raise e


create_bucket_not_exists(os.getenv("MINIO_BUCKET_NAME"))


def delete_mem(bucket_name, mem_id):
    with session_db() as session:
        mem_object = session.query(Mem).filter(Mem.id == mem_id).first()
        if mem_object is None:
            return {'message': 'Mem not found'}
        mem_path = mem_object.mem_path
        session.delete(mem_object)
        session.commit()
    client.remove_object(bucket_name, mem_path)
    return {'success': 'Mem deleted'}


def update_mem(bucket_name, mem_id, filename, mem_text, file_data):
    file_extension = filename.split('.')[-1].lower()
    if file_extension not in ALLOWED_EXTENSIONS:
        return {'message': 'File extension not allowed'}

    with session_db() as session:
        object_mem = session.query(Mem).filter(Mem.id == mem_id).first()
        if object_mem is None:
            return {'success': 'Mem does not exist'}
        object_name_path = object_mem.mem_path
        object_mem.text = mem_text
        session.commit()

    client.put_object(
        bucket_name=bucket_name,
        object_name=f'{object_name_path}',
        data=file_data.file,
        length=file_data.size,
    )
    return {"success": "Mem update successfully", "mem_text": mem_text}


def add_mem(bucket_name, filename, mem_text, file_data):
    file_extension = filename.split('.')[-1].lower()
    if file_extension not in ALLOWED_EXTENSIONS:
        return {'message': 'File extension not allowed'}

    object_name_path = f"{time.time()}.{file_extension}"
    client.put_object(
        bucket_name=bucket_name,
        object_name=f'{object_name_path}',
        data=file_data.file,
        length=file_data.size,
    )
    with session_db() as session:
        session.add(Mem(mem_path=object_name_path, text=mem_text))
        session.commit()
    return {"success": "Mem create successfully", "mem_text": mem_text}


def get_mem_for_id(bucket_name, mem_id):
    with session_db() as session:
        mem_object = session.query(Mem).filter(Mem.id == mem_id).scalar()

    if not mem_object:
        return {
            'mem_id': mem_id,
            'text': None,
            'image_base64': None
        }

    result = client.get_object(bucket_name, mem_object.mem_path)
    response_data = {
        'mem_id': mem_object.id,
        'text': mem_object.text,
        'image_base64': base64.b64encode(result.data)
    }
    return response_data



def get_list(page: int = 1, size: int = 10):
    if page < 1 or size < 1:
        return {'message': 'Both "page" and "size" must be greater than or equal to 1'}

    with session_db() as session:
        offset = (page - 1) * size
        total_count = session.execute(func.count(Mem.id))
        total_count = total_count.scalar()

        total_pages = (total_count + size - 1) // size

        result = session.execute(select(Mem).offset(offset).limit(size))
        memes = result.scalars().all()

        memes_list = [{
            'id': mem.id,
            'mem_path': mem.mem_path,
            'text': mem.text
        } for mem in memes]

        return {
            'total_pages': total_pages,
            'page': page,
            'memes': memes_list
        }