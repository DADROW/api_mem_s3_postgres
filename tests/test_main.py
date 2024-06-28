import pytest
import requests


BASE_URL = "http://localhost:2424"


@pytest.mark.parametrize("page, size, expected_error", [
    (0, 10, 'Both "page" and "size" must be greater than or equal to 1'),
    (1, 0, 'Both "page" and "size" must be greater than or equal to 1'),
    (-1, 10, 'Both "page" and "size" must be greater than or equal to 1'),
    (1, -1, 'Both "page" and "size" must be greater than or equal to 1'),
])
def test_get_list_invalid_params(page, size, expected_error):
    params = {
        "page": page,
        "size": size,
    }
    result = requests.get(f"{BASE_URL}/memes", params=params)
    result = result.json()
    assert isinstance(result, dict)
    assert 'message' in result
    assert result['message'] == expected_error


def test_get_memes():
    params = {
        'page': 1,
        'size': 10
    }
    response = requests.get(f"{BASE_URL}/memes", params=params)

    assert response.status_code == 200
    assert 'memes' in response.json()


def test_get_mem():
    response = requests.get(f"{BASE_URL}/memes/1")
    assert response.status_code == 200
    assert "mem_id" in response.json()
    assert "text" in response.json()
    assert "image_base64" in response.json()


def test_post_mem():
    files = {'file': open('tests/mem.jpeg', 'rb')}
    data = {'mem_text': 'Ностальгия эх...'}
    response = requests.post(f"{BASE_URL}/memes", files=files, data=data)
    assert response.status_code == 200
    assert "success" in response.json()


def test_update_mem():
    files = {'file': open('tests/mem.jpeg', 'rb')}
    data = {
        'mem_text': 'Ностальгия эх...'
    }
    response = requests.put(f"{BASE_URL}/memes/1", files=files, data=data)
    assert response.status_code == 200
    assert "success" in response.json()


def test_delete_mem():
    response = requests.delete(f"{BASE_URL}/memes/1")
    assert response.status_code == 200
    assert "success" in response.json() or "message" in response.json()