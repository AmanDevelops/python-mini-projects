# Expense Tracker API

This is a simple Expense Tracker API built with Flask. It allows users to register, login, and manage their expenses.

## Table of Contents

- [Expense Tracker API](#expense-tracker-api)
  - [Table of Contents](#table-of-contents)
  - [Setup](#setup)
  - [API Endpoints](#api-endpoints)
    - [Authentication](#authentication)
      - [POST /auth/register](#post-authregister)
      - [POST /auth/login](#post-authlogin)
    - [Expenses](#expenses)
      - [POST /expenses/create](#post-expensescreate)
      - [GET /expenses](#get-expenses)
      - [PUT /expenses/<id>](#put-expensesid)
      - [DELETE /expenses/<id>](#delete-expensesid)
  - [Models](#models)
    - [User](#user)
    - [Expense](#expense)
    - [Category](#category)
  - [Error Handling](#error-handling)

## Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/user/expense-tracker-api.git
    cd expense-tracker-api
    ```
2.  **Create a virtual environment and activate it:**
    ```bash
    python -m venv venv
    source venv/bin/activate # on windows use `venv\Scripts\activate`
    ```
3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Set up the environment variables:**
    Create a `.env` file in the root directory and add the following:
    ```
    JWT_SECRET=your_jwt_secret
    ```
5.  **Run the application:**
    ```bash
    flask run
    ```

## API Endpoints

### Authentication

#### POST /auth/register

Registers a new user.

-   **Request Body:**
    ```json
    {
        "username": "testuser",
        "password": "password123"
    }
    ```
-   **Success Response (201):**
    ```json
    {
        "message": "User created successfully!"
    }
    ```
-   **Error Responses:**
    -   `400 Bad Request`: If username already exists, or if required fields are missing or invalid.

#### POST /auth/login

Logs in a user and returns a JWT token.

-   **Request Body:**
    ```json
    {
        "username": "testuser",
        "password": "password123"
    }
    ```
-   **Success Response (200):**
    ```json
    {
        "message": "User authenticated successfully",
        "token": "your_jwt_token"
    }
    ```
-   **Error Responses:**
    -   `400 Bad Request`: If username or password is incorrect.

### Expenses

All expense endpoints require a valid JWT token in the `Authorization` header.
`Authorization: Bearer <your_jwt_token>`

#### POST /expenses/create

Creates a new expense.

-   **Request Body:**
    ```json
    {
        "title": "Coffee",
        "amount": 5,
        "category": "Food"
    }
    ```
-   **Success Response (201):**
    ```json
    {
        "message": "Expense Created!",
        "data": {
            "id": 1,
            "title": "Coffee",
            "amount": 5,
            "created_at": 1678886400,
            "owner": "testuser"
        }
    }
    ```
-   **Error Responses:**
    -   `400 Bad Request`: If required fields are missing or invalid.

#### GET /expenses

Retrieves a list of expenses for the authenticated user.

-   **Query Parameters:**
    -   `filter` (optional): Number of days to filter expenses by (e.g., `?filter=30` for the last 30 days). Defaults to 365.
-   **Success Response (200):**
    ```json
    {
        "data": [
            {
                "id": 1,
                "title": "Coffee",
                "amount": 5,
                "created_at": 1678886400
            }
        ]
    }
    ```

#### PUT /expenses/<id>

Updates an existing expense.

-   **Request Body:**
    ```json
    {
        "title": "Expensive Coffee",
        "amount": 10,
        "category": "Drinks"
    }
    ```
-   **Success Response (200):**
    ```json
    {
        "message": "Expense Updated",
        "data": {
            "id": 1,
            "title": "Expensive Coffee",
            "amount": 10,
            "created_at": 1678886400,
            "owner": "testuser"
        }
    }
    ```
-   **Error Responses:**
    -   `400 Bad Request`: If the expense does not exist or if the request body is invalid.

#### DELETE /expenses/<id>

Deletes an existing expense.

-   **Success Response (204):** No content.
-   **Error Responses:**
    -   `400 Bad Request`: If the expense does not exist.

## Models

### User

| Field    | Type   | Description                |
| :------- | :----- | :------------------------- |
| id       | int    | Primary Key                |
| username | str    | Unique username            |
| password | str    | Hashed password            |

### Expense

| Field       | Type   | Description                |
| :---------- | :----- | :------------------------- |
| id          | int    | Primary Key                |
| title       | str    | Title of the expense       |
| category_id | int    | Foreign Key to Category    |
| amount      | int    | Amount of the expense      |
| created_at  | int    | Timestamp of creation      |
| user_id     | int    | Foreign Key to User        |

### Category

| Field | Type | Description       |
| :---- | :--- | :---------------- |
| id    | int  | Primary Key       |
| name  | str  | Name of the category |

## Error Handling

The API returns JSON error messages with appropriate status codes.

| Status Code | Message                        |
| :---------- | :----------------------------- |
| 400         | Bad Request - Invalid input    |
| 401         | Unauthorized - Invalid token   |
| 404         | Not Found - Endpoint not found |
| 405         | Method Not Allowed             |
