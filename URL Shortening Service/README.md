# URL Shortening Service

This is a simple URL shortening service built with Flask. It allows users to register, login, and create, update, delete, and view their own shortened URLs.

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
  - [Running the Application](#running-the-application)
  - [API Endpoints](#api-endpoints)
- [Project Structure](#project-structure)
- [Built With](#built-with)

## Features

- User registration and login with JWT authentication.
- Create, retrieve, update, and delete shortened URLs.
- Redirects from short codes to the original URL.
- Custom exception handling for clear error responses.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.11
- Docker (optional, for running a PostgreSQL database)

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/AmanDevelops/python-mini-projects
    cd "python-mini-projects/URL Shortening Service"
    ```

2.  **Create and activate a virtual environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**

    Create a `.env` file in the root directory and add the following:

    ```
    JWT_SECRET=your_jwt_secret
    ```

    Replace `your_jwt_secret` with a strong, secret key.

5.  **Initialize the database:**

    The application uses SQLite by default. The database file `instance.db` will be created automatically when the application starts.

    If you prefer to use PostgreSQL, you can use the provided `docker-compose.yaml` file:

    ```bash
    docker-compose up -d
    ```

    Then, update the `engine` in `database.py` to connect to your PostgreSQL instance.

## Usage

### Running the Application

To run the Flask development server, use the following command:

```bash
flask run
```

The application will be available at `http://127.0.0.1:5000`.

### API Endpoints

All API endpoints are documented below.

#### Authentication

- **`POST /auth/register`**: Register a new user.

  - **Request Body:**
    ```json
    {
      "username": "your_username",
      "password": "your_password"
    }
    ```
  - **Response:** `201 Created`

- **`POST /auth/login`**: Log in an existing user.
  - **Request Body:**
    ```json
    {
      "username": "your_username",
      "password": "your_password"
    }
    ```
  - **Response:**
    ```json
    {
      "token": "your_jwt_token"
    }
    ```

#### URL Shortening

- **`POST /shorten/`**: Create a new shortened URL.

  - **Headers:** `Authorization: Bearer your_jwt_token`
  - **Request Body:**
    ```json
    {
      "url": "https://example.com/very/long/url"
    }
    ```
  - **Response:**
    ```json
    {
      "id": 1,
      "url": "https://example.com/very/long/url",
      "short_code": "some_short_code",
      "created_at": "2025-07-16T12:00:00",
      "updated_at": "2025-07-16T12:00:00",
      "created_by": 1,
      "views": 0
    }
    ```

- **`GET /shorten/`**: Get a specific shortened URL.

  - **Headers:** `Authorization: Bearer your_jwt_token`
  - **Request Body:**
    ```json
    {
      "id": 1
    }
    ```

- **`GET /shorten/all`**: Get all shortened URLs for the authenticated user.

  - **Headers:** `Authorization: Bearer your_jwt_token`

- **`PUT /shorten/`**: Update a shortened URL.

  - **Headers:** `Authorization: Bearer your_jwt_token`
  - **Request Body:**
    ```json
    {
      "id": 1,
      "url": "https://new-example.com",
      "short_code": "new_short_code"
    }
    ```

- **`DELETE /shorten/`**: Delete a shortened URL.

  - **Headers:** `Authorization: Bearer your_jwt_token`
  - **Request Body:**
    ```json
    {
      "id": 1
    }
    ```

- **`GET /<short_code>`**: Redirect to the original URL.

## Project Structure

```
.
├── auth
│   ├── handlers.py
│   ├── models.py
│   ├── routes.py
│   └── schemas.py
├── exceptions
│   └── custom_exceptions.py
├── service
│   ├── models.py
│   ├── routes.py
│   └── schemas.py
├── .env
├── app.py
├── config.py
├── database.py
├── docker-compose.yaml
└── requirements.txt
```

## Built With

- [Flask](https://flask.palletsprojects.com/) - The web framework used
- [SQLAlchemy](https://www.sqlalchemy.org/) - The ORM for database interaction
- [Pydantic](https://pydantic-docs.helpmanual.io/) - Data validation
- [PyJWT](https://pyjwt.readthedocs.io/) - JWT implementation
- [Bcrypt](https://pypi.org/project/bcrypt/) - Password hashing
