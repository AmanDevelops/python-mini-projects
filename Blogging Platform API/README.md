# Blogging Platform API

This is a simple Blogging Platform API built with Flask and SQLAlchemy.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You will need to have the following installed on your machine:

- Python 3
- pip
- PostgreSQL

### Installation

1.  Clone the repo
    ```sh
    git clone https://github.com/AmanDevelops/python-mini-projects.git
    cd '.\python-mini-projects\Blogging Platform API\'
    ```
2.  Create a virtual environment
    ```sh
    python -m venv venv
    ```
3.  Activate the virtual environment
    ```sh
    venv\Scripts\activate
    ```
4.  Install the required packages
    ```sh
    pip install -r requirements.txt
    ```
5.  Create a `.env` file in the root directory of the project and add the following line:

    ```
    POSTGRES_URI=postgresql+psycopg://postgres:postgres@localhost:5432/blog
    ```

    _You may need to change the username, password, and database name to match your PostgreSQL setup._

6.  Create the database tables by running the following command in the Python interpreter:
    ```python
    from models import Base, engine
    Base.metadata.create_all(engine)
    ```

## Running the Application

To run the application, use the following command:

```sh
flask run
```

The application will be running on `http://127.0.0.1:5000`.

## Testing the Application

You can test the API endpoints using a tool like `curl` or Postman.

### API Endpoints

#### Create a Post

- **Method:** `POST`
- **URL:** `/posts`
- **Request Body:**
  ```json
  {
    "title": "My First Post",
    "content": "This is the content of my first post.",
    "category": "Technology",
    "tags": ["python", "flask", "sqlalchemy"]
  }
  ```
- **Sample Response:**
  ```json
  {
    "success": true,
    "message": "Post created successfully",
    "data": {
      "id": 1,
      "title": "My First Post",
      "content": "This is the content of my first post.",
      "category": "Technology",
      "tags": ["python", "flask", "sqlalchemy"],
      "created_at": "2025-07-10T12:00:00.000000Z",
      "updated_at": "2025-07-10T12:00:00.000000Z"
    }
  }
  ```

#### Get All Posts

- **Method:** `GET`
- **URL:** `/posts`
- **Query Parameters:**
  - `term` (optional): Search term to filter posts by title, content, or category.
- **Sample Response:**
  ```json
  {
    "success": true,
    "data": [
      {
        "id": 1,
        "title": "My First Post",
        "content": "This is the content of my first post.",
        "category": "Technology",
        "tags": ["python", "flask", "sqlalchemy"],
        "created_at": "2025-07-10T12:00:00.000000Z",
        "updated_at": "2025-07-10T12:00:00.000000Z"
      }
    ]
  }
  ```

#### Get a Single Post

- **Method:** `GET`
- **URL:** `/posts/<post_id>`
- **Sample Response:**
  ```json
  {
    "success": true,
    "data": {
      "id": 1,
      "title": "My First Post",
      "content": "This is the content of my first post.",
      "category": "Technology",
      "tags": ["python", "flask", "sqlalchemy"],
      "created_at": "2025-07-10T12:00:00.000000Z",
      "updated_at": "2025-07-10T12:00:00.000000Z"
    }
  }
  ```

#### Update a Post

- **Method:** `PUT`
- **URL:** `/posts/<post_id>`
- **Request Body:**
  ```json
  {
    "title": "My Updated Post",
    "content": "This is the updated content of my post.",
    "category": "Programming",
    "tags": ["python", "flask", "sqlalchemy", "rest"]
  }
  ```
- **Sample Response:**
  ```json
  {
    "success": true,
    "message": "Post updated successfully",
    "data": {
      "id": 1,
      "title": "My Updated Post",
      "content": "This is the updated content of my post.",
      "category": "Programming",
      "tags": ["python", "flask", "sqlalchemy", "rest"],
      "created_at": "2025-07-10T12:00:00.000000Z",
      "updated_at": "2025-07-10T12:05:00.000000Z"
    }
  }
  ```

#### Delete a Post

- **Method:** `DELETE`
- **URL:** `/posts/<post_id>`
- **Sample Response:**
  - **Status Code:** `204 No Content`
