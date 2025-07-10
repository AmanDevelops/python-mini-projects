# Todo List API

This is a simple Todo List API built with Flask.

## Setup

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/AmanDevelops/python-mini-projects.git
    cd '.\python-mini-projects\Todo List API\'
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Create a `.env` file** and add the following environment variable:
    ```
    JWT_SECRET=your_jwt_secret
    ```
4.  **Run the application:**
    ```bash
    flask run
    ```

## API Endpoints

### Authentication

#### `/register`

- **Method:** `POST`
- **Description:** Registers a new user.
- **Request Body:**
  ```json
  {
    "name": "Test User",
    "email": "test@example.com",
    "password": "password123"
  }
  ```
- **Response:**
  - `201 Created`: If the user is created successfully.
    ```json
    {
      "message": "User Created succesfully!"
    }
    ```
  - `400 Bad Request`: If the request data is invalid.
  - `409 Conflict`: If the user already exists.

#### `/login`

- **Method:** `POST`
- **Description:** Authenticates a user and returns a JWT token.
- **Request Body:**
  ```json
  {
    "email": "test@example.com",
    "password": "password123"
  }
  ```
- **Response:**
  - `200 OK`: If authentication is successful.
    ```json
    {
      "message": "User authenticated Successfully",
      "token": "your_jwt_token"
    }
    ```
  - `401 Unauthorized`: If the email or password is invalid.

### Todos

**Note:** All todo endpoints require a valid JWT token in the `Authorization` header.

#### `/todos`

- **Method:** `POST`
- **Description:** Creates a new todo.
- **Request Body:**
  ```json
  {
    "title": "My First Todo",
    "description": "This is my first todo item."
  }
  ```
- **Response:**
  - `201 Created`: If the todo is created successfully.
    ```json
    {
      "id": 1,
      "title": "My First Todo",
      "description": "This is my first todo item."
    }
    ```
  - `400 Bad Request`: If the request data is invalid.

#### `/todos`

- **Method:** `GET`
- **Description:** Retrieves a list of all todos.
- **Query Parameters:**
  - `page` (optional): The page number to retrieve. Defaults to `1`.
  - `limit` (optional): The number of todos to retrieve per page. Defaults to `10`.
- **Response:**
  - `200 OK`:
    ```json
    {
      "todos": [
        {
          "id": 1,
          "title": "My First Todo",
          "description": "This is my first todo item."
        },
        {
          "id": 2,
          "title": "Another Todo",
          "description": "This is another todo item."
        },
        ...
      ]
    }
    ```

#### `/todos/<int:todo_id>`

- **Method:** `PUT`
- **Description:** Updates an existing todo.
- **Request Body:**
  ```json
  {
    "title": "Updated Todo Title",
    "description": "Updated todo description."
  }
  ```
- **Response:**
  - `200 OK`: If the todo is updated successfully.
    ```json
    {
      "id": 1,
      "title": "Updated Todo Title",
      "description": "Updated todo description."
    }
    ```
  - `400 Bad Request`: If the request data is invalid.
  - `404 Not Found`: If the todo with the specified ID does not exist.

#### `/todos/<int:todo_id>`

- **Method:** `DELETE`
- **Description:** Deletes a todo.
- **Response:**
  - `204 No Content`: If the todo is deleted successfully.
  - `404 Not Found`: If the todo with the specified ID does not exist.
