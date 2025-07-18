import asyncio

import websockets


async def send_message():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        print("Waiting for messages...")
        while True:
            response = await websocket.recv()
            print(f"[Server]: {response}")


if __name__ == "__main__":
    try:
        asyncio.run(send_message())
    except KeyboardInterrupt:
        print("Server Disconnected!")
    except OSError:
        print("Could not connect to server")
    except websockets.exceptions.ConnectionClosedOK:
        print("Server abruply disconnected!")
