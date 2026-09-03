# Robot Explorer Bridge

A real-time bridge between a hosted static Three.js app and a local Python program, using WebSockets.

**Hosted app:** https://sagarbawanthade.github.io/devops-assignment/

The Three.js robot scene is hosted as a plain static site on GitHub Pages. When it loads, it opens a WebSocket connection to a Python script running on your machine, no backend is added to the hosting, and no build step is required.

- **Browser → Python:** streams live robot position/rotation every frame.
- **Python → Browser:** sends movement commands (`forward`, `back`, `left`, `right`, `run`, `stop`) that drive the robot.

---

## Why WebSockets

I chose a direct WebSocket connection because it gives real-time, sub-second, two-way communication with minimal code and no extra moving parts, no browser extension, no separate relay server, no automation tooling. The hosted page stays a plain static file, and the local Python process just listens on `ws://localhost:8765`; alternatives like a Chrome extension or WebRTC would solve the same problem but add setup complexity this assignment doesn't need.

---

## Project Structure

```text
devops-assignment/
├── index.html
├── python/
│   └── server.py
└── README.md
```

---

## Setup & Run

1. **Clone the repo**
   ```bash
   git clone https://github.com/sagarbawanthade/devops-assignment.git
   cd devops-assignment
   ```

2. **Install dependency**
   ```bash
   pip install websockets
   ```

3. **Start the Python server**
   ```bash
   python python/server.py
   ```
   You'll be asked how to display state updates:
   ```text
   1) Auto   - continuously print position/rotation as it streams in
   2) Manual - stay quiet; type 'state' to fetch it on demand
   ```

4. **Open the hosted app:** https://sagarbawanthade.github.io/devops-assignment/
   Open DevTools (F12) — you should see `Connected to Python bridge` in the console, and the Python terminal will start showing/streaming robot state.

5. **Drive the robot from Python** — type any of:
   ```text
   forward | back | left | right | run | stop | state | quit
   ```
   Directions are toggles (send again to release), and `forward`/`back` and `left`/`right` are mutually exclusive also activating one cancels its opposite. `state` prints the current position on demand (useful in manual mode). `stop` clears movement but leaves `run` as-is.

---


## Limitations

- **If the Python server restarts, the browser's WebSocket does not auto-reconnect, you have to refresh the page to re-establish the connection.**
- Requires the local Python server to be running; no authentication is implemented.
- Intended for local development/demo purposes, not production use.
