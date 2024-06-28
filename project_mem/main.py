import os

import uvicorn

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import RedirectResponse

import core


BUCKET_NAME = os.getenv("MINIO_BUCKET_NAME")

app = FastAPI()


@app.exception_handler(404)
async def custom_404_handler(_, __):
    return RedirectResponse("/")


@app.get("/")
def index():
    return {'message': '/docs'}


@app.get("/memes")
def get_list_of_page(page: int = 1, size: int = 10):
    result = core.get_list(page, size)
    return result


@app.get("/memes/{mem_id}")
def get_mem(mem_id: int):
    result = core.get_mem_for_id(BUCKET_NAME, mem_id)
    return result


@app.post("/memes")
def post_mem(mem_text: str = Form(...), file: UploadFile = File(...)):
    result = core.add_mem(BUCKET_NAME, file.filename, mem_text, file)
    return result


@app.put("/memes/{mem_id}")
def update_mem(mem_id: int, mem_text: str = Form(...), file: UploadFile = File(...)):
    result = core.update_mem(BUCKET_NAME, mem_id, file.filename, mem_text, file)
    return result


@app.delete("/memes/{mem_id}")
def delete_mem(mem_id: int):
    result = core.delete_mem(BUCKET_NAME, mem_id)
    return result


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=2024)
