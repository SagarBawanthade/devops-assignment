# Robot Explorer Bridge

Bridges the hosted static page at
`https://sagarbawanthade.github.io/devops-assignment/` to a local Python
process, in real time, using a small Chrome extension and a local
WebSocket server.

## How it works

```
Hosted page (window.postMessage)
        |
        v
Content script (extension, runs in the page's tab)
        |
        v
Background service worker  <-- WebSocket -->  Python server (localhost:8765)
```

- The page already broadcasts `window.postMessage({ type: "robot-state", ... })`
  every animation frame, and listens for
  `window.postMessage({ type: "robot-command", ... })` to drive the robot.
- The extension's **content script** listens for `robot-state` messages and
  forwards them to the **background service worker**.
- The background worker holds a WebSocket connection to a local Python
  server and relays state to it in real time, and relays any
  `robot-command` messages sent back from Python into the tab.

No backend was added to the hosted app — it's still pure static files.
The extension and Python server run entirely on the local machine.

## Setup

### 1. Python server
```bash
cd python
pip install websockets
python server.py
```
Leave this running — it will print live `x / z / rotationY` as the robot
moves, and after a client connects it will also demo a "forward" command
being pushed back into the browser.

### 2. Load the extension
1. Open `chrome://extensions`
2. Enable "Developer mode" (top right)
3. Click "Load unpacked", select the `extension/` folder
4. Open `https://sagarbawanthade.github.io/devops-assignment/` in a new tab

Once the tab is open, the extension icon's background worker connects to
`ws://localhost:8765` automatically, and state should start streaming into
the Python terminal within a second.

## Why this mechanism

I chose a **Chrome extension + local WebSocket server** over the
alternatives (Chrome DevTools Protocol, Playwright/Selenium automation,
WebRTC, native messaging) because it matches the scenario in the prompt
most literally: a person has the *already-hosted* page open in their
normal browser, and the bridge taps into that live tab, rather than Python
spinning up and owning its own browser instance (which is what CDP/
Playwright would do). It's also lower-complexity than native messaging
(no manifest registration for a native host) or WebRTC (no signaling/ICE
setup needed for a purely local machine), while still being fully
real-time and push-based rather than polling.

## Trade-offs (honest accounting)

- **Latency:** sub-second, effectively one WebSocket hop each way — driven
  by the page's own per-frame `postMessage` broadcast.
- **Security:** the WebSocket server has no auth and listens on
  `localhost` only. Fine for a local dev bridge; for anything beyond a
  take-home I'd add a token handshake and restrict the extension's
  `host_permissions` more tightly (already scoped to just this page's
  origin, not `<all_urls>`).
- **Browser permissions required:** the user has to manually load an
  unpacked extension (`chrome://extensions` → Developer mode). That's a
  real friction point compared to, say, a script that "just runs" — it's
  the cost of not touching the page's own hosting/build.
- **Fragility:** if the Python server isn't running when the tab loads,
  the background worker just retries every 2s — no data is lost, but
  nothing is buffered while disconnected either.