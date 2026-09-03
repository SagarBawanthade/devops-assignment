import asyncio
import json
import websockets

connected = set()
latest_state = {"x": 0.0, "z": 0.0, "rotationY": 0.0}
STATE_MODE = "auto"  # set once at startup: "auto" or "manual"


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
    Continuously receive the robot's live state from the browser.

    - In 'auto' mode: prints a few times a second (throttled so it
      doesn't flood the terminal and bury the '>' prompt).
    - In 'manual' mode: silently stores the latest value; nothing is
      printed until you type 'state' at the prompt.
    """
    global latest_state
    last_print = 0
    PRINT_INTERVAL = 0.3  # seconds between printed updates (auto mode only)

    async for message in websocket:
        data = json.loads(message)
        latest_state = data  # always keep the freshest value available

        if STATE_MODE == "auto":
            loop = asyncio.get_event_loop()
            now = loop.time()
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
      state     - print current position (useful in manual mode)
      quit      - close the connection
    Commands stay active until you send another one (e.g. 'forward' keeps
    the robot moving until you type 'stop').
    """
    print("\nType a command and press Enter: forward | back | left | right | run | stop | quit")
    if STATE_MODE == "manual":
        print("(manual state mode) type 'state' anytime to print the current position\n")

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
            opposites = {"forward": "back", "back": "forward", "left": "right", "right": "left"}
            state[cmd] = not state[cmd]
            if state[cmd]:
                # turning this direction on cancels its opposite so you
                # never end up with both forward+back or left+right true
                state[opposites[cmd]] = False
        elif cmd == "run":
            state["run"] = not state["run"]
        elif cmd == "state":
            d = latest_state
            print(f"[state] x={d['x']:.2f} z={d['z']:.2f} rot={d['rotationY']:.2f}")
            continue
        else:
            print("Unknown command. Use: forward | back | left | right | run | stop | quit | state")
            continue

        print(f"[cmd] Sending: {state}")
        await websocket.send(json.dumps(state))


def choose_state_mode():
    """Ask the user, once at startup, how state updates should be shown."""
    global STATE_MODE
    print("How should robot state updates be shown?")
    print("  1) Auto   - continuously print position/rotation as it streams in")
    print("  2) Manual - stay quiet; type 'state' to fetch it on demand")
    while True:
        choice = input("Select 1 or 2 [default 1]: ").strip()
        if choice in ("", "1"):
            STATE_MODE = "auto"
            break
        elif choice == "2":
            STATE_MODE = "manual"
            break
        else:
            print("Please enter 1 or 2.")


async def main():
    choose_state_mode()
    async with websockets.serve(handler, "localhost", 8765):
        print(f"Listening on ws://localhost:8765  (state mode: {STATE_MODE})")
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())