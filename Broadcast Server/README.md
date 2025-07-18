# Broadcast Server

A simple Python-based broadcast server using WebSockets. This application allows a server to send messages to multiple connected clients simultaneously.

## Features

*   **WebSocket Communication:** Utilizes the `websockets` library for real-time, bidirectional communication.
*   **Asynchronous I/O:** Built with `asyncio` for efficient handling of concurrent connections.
*   **Dynamic Client Management:** The server dynamically tracks the number of connected clients.
*   **Console Input:** The server uses `aioconsole` to accept messages from the command line without blocking the event loop.

## Requirements

*   Python 3.7+
*   `websockets`
*   `aioconsole`

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/AmanDevelops/python-mini-projects.git
    cd python-mini-projects/Broadcast Server
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Start the server:**
    Open a terminal and run the following command:
    ```bash
    python server.py
    ```
    The server will start and display the current number of connected clients.

2.  **Connect clients:**
    Open one or more separate terminals and run the following command for each client:
    ```bash
    python client.py
    ```
    Each client will connect to the server and wait for messages.

3.  **Broadcast messages:**
    Go back to the server's terminal. Type a message and press Enter. The message will be broadcast to all connected clients.

## How It Works

### `server.py`

*   The server maintains a `set` of `CONNECTED_CLIENTS`.
*   The `handler` function is called for each new client connection. It adds the client's WebSocket connection to the `CONNECTED_CLIENTS` set. When the client disconnects, it's removed from the set.
*   The `send_messages` function runs in an infinite loop, waiting for input from the server's console using `aioconsole.ainput`. When a message is entered, it's sent to all clients in the `CONNECTED_CLIENTS` set.
*   The `print_status` function prints the number of connected clients to the server's console.

### `client.py`

*   The client connects to the server at `ws://localhost:8765`.
*   It then enters an infinite loop, waiting to receive messages from the server using `websocket.recv()`.
*   When a message is received, it's printed to the client's console.
