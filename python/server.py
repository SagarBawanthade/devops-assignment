import asyncio
import json
import websockets

connected = set()


async def handler(websocket):
    print("Browser connected")
    connected.add(websocket)

    try:
        # Run the state-reader and the command-input loop concurrently
        reader_task = asyncio.create_task(read_state(websocket))
        await command_input_loop(websocket)
        reader_task.cancel()
    finally:
        connected.discard(websocket)
        print("Browser disconnected")


async def read_state(websocket):
    """
    Continuously receive the robot's live state, but only print it a few
    times a second (not on every single frame) so it doesn't flood the
    terminal and bury the '>' input prompt.
    """
    last_print = 0
    PRINT_INTERVAL = 0.3  # seconds between printed updates

    async for message in websocket:
        data = json.loads(message)
        now = asyncio.get_event_loop().time()
        if now - last_print >= PRINT_INTERVAL:
            last_print = now
            print(
                f"\r[state] x={data['x']:.2f} "
                f"z={data['z']:.2f} "
                f"rot={data['rotationY']:.2f}"
                "          "
            )


async def command_input_loop(websocket):
    """
    Type commands in this terminal to drive the robot live:
      forward   - move forward
      back      - move backward
      left      - turn left
      right     - turn right
      run       - toggle run (shift/speed boost)
      stop      - stop all movement
      quit      - close the connection
    Commands stay active until you send another one (e.g. 'forward' keeps
    the robot moving until you type 'stop').
    """
    print("Type a command and press Enter: forward | back | left | right | run | stop | quit")

    state = {"forward": False, "back": False, "left": False, "right": False, "run": False}

    loop = asyncio.get_event_loop()

    while True:
        cmd = await loop.run_in_executor(None, input, "> ")
        cmd = cmd.strip().lower()

        if cmd == "quit":
            print("Closing connection...")
            break
        elif cmd == "stop":
            state.update({"forward": False, "back": False, "left": False, "right": False})
        elif cmd in ("forward", "back", "left", "right"):
            # toggle: pressing the same command again releases it
            state[cmd] = not state[cmd]
        elif cmd == "run":
            state["run"] = not state["run"]
        else:
            print("Unknown command. Use: forward | back | left | right | run | stop | quit")
            continue

        print(f"[cmd] Sending: {state}")
        await websocket.send(json.dumps(state))


async def main():
    async with websockets.serve(handler, "localhost", 8765):
        print("Listening on ws://localhost:8765")
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())