import asyncio
import json
import websockets

async def handler(websocket):
    print("Browser connected")

    async def send_commands():
        await asyncio.sleep(3)

        print("Moving robot forward")

        await websocket.send(
            json.dumps({
                "forward": True
            })
        )

        await asyncio.sleep(2)

        await websocket.send(
            json.dumps({
                "forward": False
            })
        )

        print("Robot stopped")

    asyncio.create_task(send_commands())

    async for message in websocket:
        data = json.loads(message)

        print(
            f"x={data['x']:.2f} "
            f"z={data['z']:.2f} "
            f"rot={data['rotationY']:.2f}"
        )

async def main():
    async with websockets.serve(handler, "localhost", 8765):
        print("Listening on ws://localhost:8765")
        await asyncio.Future()

asyncio.run(main())