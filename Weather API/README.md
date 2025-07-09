# Weather API

A simple weather API that provides weather information for a given city. It uses the Visual Crossing Weather API as its data source and incorporates caching with **Redis** to improve performance and reduce API calls.

## Features

*   **Current Weather Data:** Get the current weather for any city.
*   **Rate Limiting:** Implemented to prevent abuse of the API.
*   **Caching:** Caches weather data for two hours to provide faster responses and reduce the number of calls to the external weather API.
*   **Dockerized:** The application is fully containerized for easy setup and deployment.

## Technologies Used

*   **Backend:** Python, Flask
*   **Caching:** Redis
*   **Containerization:** Docker, Docker Compose
*   **External API:** [Visual Crossing Weather API](https://www.visualcrossing.com/weather-api)

## Setup and Installation

### Prerequisites

*   [Docker](https://www.docker.com/get-started)
*   [Docker Compose](https://docs.docker.com/compose/install/)

### 1. Clone the repository

```bash
git clone https://github.com/AmanDevelops/python-mini-projects.git
cd '.\python-mini-projects\Weather API\'
```

### 2. Set up environment variables

Create a `.env` file in the root directory by copying the example file:

```bash
cp .env.example .env
```

Now, edit the `.env` file and add your Visual Crossing Weather API key:

```
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=your-redis-password
WEATHER_API_KEY=your-visual-crossing-api-key
```

### 3. Run the application

```bash
docker-compose up -d
```

The application will be available at `http://localhost:5000`.

## API Endpoints

### Get Weather by City

*   **URL:** `/weather/<city_name>`
*   **Method:** `GET`
*   **URL Params:** `city_name=[string]` (Required)
*   **Success Response:**
    *   **Code:** 200
    *   **Content:** `{ "address": "Lucknow", "currentConditions": { ... } }`
*   **Error Response:**
    *   **Code:** 400 `Bad Request` - Invalid Location
    *   **Code:** 401 `Unauthorized` - Invalid API Key
    *   **Code:** 502 `Bad Gateway` - Failed to fetch weather data
    *   **Code:** 503 `Service Unavailable` - Weather service unavailable

### Example usage (using curl):

```bash
curl http://localhost:5000/weather/Lucknow
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request.

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b [project]feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin [project]feature/AmazingFeature`)
5.  Open a Pull Request

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
