# Personal Blog

A simple, file-based personal blog application built with Python and the Flask web framework.

## Description

This project is a lightweight personal blog that allows an administrator to create, edit, and delete posts. It is designed for simplicity and does not require a traditional database. Instead, it uses a Python pickle file (`posts.pkl`) to store and retrieve blog posts, making it easy to set up and run locally.

The public-facing side of the blog displays published posts, while a password-protected admin panel provides full control over the content.

## Features

- **View Posts**: A clean interface for visitors to read blog posts.
- **Admin Dashboard**: A secure area for managing all blog posts.
- **CRUD Operations**: Create, Read, Update, and Delete posts through the admin panel.
- **File-Based Storage**: No database setup required; posts are stored in a local `posts.pkl` file.
- **Basic Authentication**: The admin panel is protected by a simple username and password.

## Technologies Used

- **Backend**: Python, Flask
- **Frontend**: HTML, Jinja2 Templating
- **Data Storage**: Python Pickle Module

## Setup and Installation

Follow these steps to get the application running on your local machine.

**1. Clone the Repository**

First, get the project files onto your machine. If you have git, you can clone it:

```bash
    git clone https://github.com/AmanDevelops/python-mini-projects.git
    cd python-mini-projects
    cd Personal\ Blog
```

**2. Create and Activate a Virtual Environment**

It is highly recommended to use a virtual environment to manage project-specific dependencies.

```bash
# Create the virtual environment
python3 -m venv venv

# Activate it (on Linux/macOS)
source venv/bin/activate

# On Windows
# .\venv\Scripts\activate
```

**3. Install Dependencies**

The project relies on Flask. Install it using pip.

```bash
pip install -r requirements.txt
```

## Running the Application

Once the dependencies are installed, you can run the application using the `flask` command.

```bash
# Tell Flask where to find the application
export FLASK_APP=app

# (Optional) Run in development mode for live reloading and debugging
export FLASK_DEBUG=1

# Run the application
flask run
```

The application will be available at `http://127.0.0.1:5000`.

## How to Use

### Public View

- **Home Page**: Navigate to `http://127.0.0.1:5000/` to see a list of all published posts.
- **View a Single Post**: Click on a post title to view its full content on a dedicated page.

### Admin Panel

To manage posts, you need to access the admin dashboard.

1.  **Navigate to the Admin URL**: Go to `http://127.0.0.1:5000/admin`.
2.  **Enter Credentials**: You will be prompted for a username and password. Use the following default credentials:
    -   **Username**: `admin`
    -   **Password**: `password`

From the admin dashboard, you can:
- Create a new post.
- Edit an existing post.
- Delete a post.

## Screenshots
![Screenshot from 2025-07-09 12-09-10](https://github.com/user-attachments/assets/7d326e03-06a5-4860-a699-9523479bac47)
![image](https://github.com/user-attachments/assets/0360808c-d3fb-47a9-bbef-b726f9cdce25)
![image](https://github.com/user-attachments/assets/71dc1bfa-2403-47ee-9a4a-1c0f66595f95)
![image](https://github.com/user-attachments/assets/5ad6061e-b24b-498a-9926-03fc8dfd948d)
![image](https://github.com/user-attachments/assets/6641c816-258f-4911-8ebc-e511e013ec49)



## Project Structure

```
.
├── app.py              # Main Flask application file with all routes
├── db.py               # Database class for handling data persistence
├── posts.pkl           # Data file where posts are stored (created automatically)
├── templates/
│   ├── index.html      # Public home page
│   ├── view_post.html  # View a single post
│   ├── admin_dashboard.html # Admin home page
│   ├── new_post.html   # Form for new posts
│   └── edit_post.html  # Form for editing posts
└── venv/               # Python virtual environment directory
```

## Future Improvements

This is a simple project, but it could be extended with more features:

- **Replace Pickle with a Database**: Switch to a more robust database like SQLite for better scalability and data integrity.
- **User Authentication System**: Implement a proper user login system instead of hardcoded basic auth.
- **Add Comments**: Allow readers to comment on posts.
- **Markdown Support**: Use Markdown for writing and rendering post content.
