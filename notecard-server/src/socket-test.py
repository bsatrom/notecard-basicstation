import asyncio
import websockets

async def main():
    uri = "ws://notecard-server:8765"
    async with websockets.connect(uri) as websocket:
        msg = "B3Rydg=="

        await websocket.send(msg)
        print(f"> {msg}")

        response = await websocket.recv()
        print(f"< {response}")

asyncio.get_event_loop().run_until_complete(main())