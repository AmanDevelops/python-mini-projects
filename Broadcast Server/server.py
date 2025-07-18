import asyncio

import aioconsole
import websockets

CONNECTED_CLIENTS = set()


async def print_status():
    await aioconsole.aprint(f"\nTotal Clients: {len(CONNECTED_CLIENTS)}")
    await aioconsole.aprint("> ", end="", flush=True)


async def send_messages():
    while True:
        message = await aioconsole.ainput("> ")
        await asyncio.gather(*(client.send(message) for client in CONNECTED_CLIENTS))


async def handler(websocket):
    CONNECTED_CLIENTS.add(websocket)
    await print_status()

    try:
        async for _ in websocket:
            pass
    finally:
        CONNECTED_CLIENTS.remove(websocket)
        await print_status()


async def main():
    async with websockets.serve(handler, "localhost", 8765):
        print(f"\nTotal Clients: {len(CONNECTED_CLIENTS)}")
        await send_messages()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Shutting Down Server!")
