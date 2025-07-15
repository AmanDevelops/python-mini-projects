# Markdown Note-taking App

This is a simple Flask application that allows you to upload Markdown files, converts them to HTML, and performs spell checking on the content.

## Features

*   **File Upload:** Upload your Markdown files to the server.
*   **Markdown to HTML Conversion:** Automatically converts your Markdown files to HTML.
*   **Spell Checking:** Checks for and corrects misspelled words in your document.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/AmanDevelops/python-mini-projects.git
    cd python-mini-projects/Markdown\ Note-taking\ App/
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Run the Flask application:**
    ```bash
    flask run
    ```

2.  **Upload a Markdown file:**
    Use a tool like `curl` or any HTTP client to send a POST request to the `/api/upload` endpoint.

    ```bash
    curl -X POST -F "file=@/path/to/your/note.md" http://localhost:5000/api/upload
    ```

3.  **Access the converted file:**
    The server will respond with a JSON object containing the URL to the converted HTML file.

    ```json
    {
      "url": "http://localhost:5000/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx.html"
    }
    ```

    Open the URL in your browser to view the note.

## API Endpoints

*   `POST /api/upload`
    *   **Method:** `POST`
    *   **Description:** Uploads a Markdown file for processing.
    *   **Form Data:** `file` - The Markdown file to upload.
    *   **Success Response:** `200 OK` with a JSON object containing the URL of the converted file.
    *   **Error Response:** `400 Bad Request` if no file is provided.

*   `GET /<file_id>`
    *   **Method:** `GET`
    *   **Description:** Retrieves the processed HTML file.
    *   **URL Parameters:** `file_id` - The unique identifier of the file.
    *   **Success Response:** `200 OK` with the HTML content of the file.
    *   **Error Response:** `404 Not Found` if the file does not exist.
