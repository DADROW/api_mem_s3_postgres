### Meme Manager

This project provides an API for managing memes, allowing you to retrieve, add, update, and delete memes.

### Installation and Setup

To run the project, Docker is required. Follow these steps in the directory containing the `docker-compose.yml` file:

```bash
docker-compose up --build -d
```
### Available Endpoints
### GET /memes

  * Description: Retrieve a list of all memes with pagination. 
  * Query Parameters: page (page number), size (number of records per page).


* Example Request:
  ```python
  import requests

  params = {'page': 1, 'size': 10}
  response = requests.get('http://localhost:2424/memes', params=params)
  ```
* Example Response:
  ```json
  {
    "total_pages": 5,
    "page": 1,
    "memes": [{
          "id": 1,
          "mem_path": "1132412.2134.jpeg",
          "text": "Text mem"
        },
        {
          "id": 2,
          "mem_path": "1241243.4212.png",
          "text": "Mems funny"
        },
        ...
      ] 
    }
  ```
}
### GET /memes/{id}

  * Description: Retrieve a specific meme by its ID.


* Example Request:
  ```python
  import requests
  
  response = requests.get('http://localhost:2424/memes/123')
  ```
* Example Response:
  ```json
  {
    "mem_id": "123",
    "text": "Funny mem 123 LOL",
    "image_base64": "iVBORw0KGgoAAAANSUhEUg..."
  }
  ```
### POST /memes

* Description: Add a new meme with an image and text.

* Request Body: Image file and meme text.

* Example Request (Python):
  ```python
  import requests
  
  files = {'file': open('path_to_image/mem.jpeg', 'rb')}
  data = {'mem_text': 'Wow really, oh...'}
  response = requests.post('http://localhost:2424/memes', files=files, data=data)
  ```
* Example Response:
  ```json
  {
    "success": "Mem created successfully",
    "mem_text": "Wow really, oh..."
  }
  ```

### PUT /memes/{id}

* Description: Update an existing meme by ID.

* Request Body: Image file and new meme text.

* Example Request (Python):
  ```python
  import requests
  
  files = {'file': open('path_to_image/mem.jpeg', 'rb')}
  data = {'mem_text': 'New meme text'}
  response = requests.put('http://localhost:2424/memes/123', files=files, data=data)
  ```
* Example Response:
  ```json
  {
      "success": "Mem updated successfully",
      "mem_text": "New meme text"
  }
  ```

### DELETE /memes/{id}

* Description: Delete a meme by its ID.
* Example Request:
  ```python
  import requests

  response = requests.delete('http://localhost:2424/memes/123')
  ```
* Example Response:
  ```json
  {
      "success": "Mem deleted"
  }
  ```
### Note
Ensure all image files are located in the correct directory and accessible for reading when making POST and PUT requests.

### Technical Requirements
* Docker
