# Unit Converter

A simple web-based unit converter application built with Python and Flask.

## Features

*   Convert between different units of:
    *   Length (millimeter, centimeter, meter, kilometer, inch, foot, yard, mile)
    *   Weight (milligram, gram, kilogram, ounce, pound)
    *   Temperature (Celsius, Fahrenheit, Kelvin)
*   Simple and intuitive user interface.
*   Easy to extend with new units and conversion types.

## Technologies Used

*   **Backend:** Python, Flask
*   **Frontend:** HTML, CSS, Jinja2

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/AmanDevelops/python-mini-projects.git
    cd python-mini-projects/Unit\ Converter/
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application:**
    ```bash
    flask run
    ```

    The application will be available at `http://127.0.0.1:5000`.

## How to Use

1.  Open your web browser and navigate to `http://127.0.0.1:5000`.
2.  Select the type of conversion you want to perform (Length, Weight, or Temperature) from the navigation bar.
3.  Enter the value you want to convert in the "Input" field.
4.  Select the "from" and "to" units from the dropdown menus.
5.  Click the "Calculate" button to see the result.

## File Structure

*   `app.py`: The main Flask application file containing the conversion logic and routes.
*   `requirements.txt`: A list of the Python dependencies required to run the application.
*   `static/style.css`: The CSS file for styling the application.
*   `templates/index.html`: The HTML template for the user interface.


## Screenshot
![Screenshot from 2025-07-07 19-20-57](https://github.com/user-attachments/assets/633699ce-294d-4e5b-bd8c-597c153f608b)


## Inspiration

[roadmap.sh](https://roadmap.sh/projects/unit-converter)
