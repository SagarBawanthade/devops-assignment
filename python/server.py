import asyncio
import json
import websockets

async def handler(websocket):
    print("Browser connected")

    async for message in websocket:
        data = json.loads(message)

        print(
            f"x={data['x']:.2f} "
            f"z={data['z']:.2f} "
            f"rot={data['rotationY']:.2f}"
        )

        # Example command
        # await websocket.send(
        #     json.dumps({
        #         "forward": True
        #     })
        # )

async def main():
    async with websockets.serve(handler, "localhost", 8765):
        print("Listening on ws://localhost:8765")
        await asyncio.Future()

asyncio.run(main())