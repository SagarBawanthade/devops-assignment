# Robot Explorer Bridge

Bridges the hosted Robot Explorer web app to a local Python program in real time using a WebSocket connection.

The web application remains a fully static website hosted on GitHub Pages. No backend server is added to the hosting environment.

## How It Works

```text
Hosted Web App (GitHub Pages)
            │
            │ WebSocket
            ▼
Local Python Server (localhost:8765)
```

The browser establishes a WebSocket connection directly to a Python server running on the local machine.

The web page continuously streams the robot's position and rotation to Python. Python can also send commands back to the browser, allowing the robot to be controlled remotely.

This creates a real-time, bidirectional bridge between the hosted static page and local Python code.

## Features

### Read Live State from the Browser

The browser streams robot state data to Python in real time:

```text
x=12.54 z=31.28 rot=1.57
x=12.60 z=31.35 rot=1.57
x=12.68 z=31.43 rot=1.57
```

### Send Commands from Python

Python can send commands back to the browser:

```json
{
  "forward": true
}
```

The browser receives the command and drives the robot accordingly.

## Setup

### 1. Start the Python Server

```bash
cd python
pip install websockets
python server.py
```

You should see:

```text
Listening on ws://localhost:8765
```

### 2. Open the Hosted Application

Open:

```text
https://sagarbawanthade.github.io/devops-assignment/
```

When the connection is established, the browser console will show:

```text
Connected to Python bridge
```

The Python terminal will immediately start receiving live robot state updates.

## Project Structure

```text
.
├── index.html
├── python
│   └── server.py
└── README.md
```

## Why I Chose This Approach

I chose a direct WebSocket connection because it is the simplest way to achieve real-time communication while keeping the application completely static.

The hosted web page remains just HTML, CSS, and JavaScript. No backend infrastructure, browser extension, or automation framework is required.

Compared to browser-extension-based approaches, this solution requires less setup and works across modern browsers without additional installation steps.

## Trade-offs

### Advantages

- Real-time communication
- Low latency
- Simple architecture
- No browser extension required
- No backend added to the hosted application
- Easy to reproduce on another machine

### Limitations

- Requires a local Python server to be running
- The browser must be able to connect to localhost
- No authentication is implemented (acceptable for a local development bridge)

## Demo

The demonstration shows:

1. The hosted browser page streaming live robot state to Python.
2. Python receiving updates in real time.
3. Python sending commands back to the browser.
4. The robot responding immediately inside the hosted page.

## Assignment Requirements Covered

✅ Works against a hosted URL

✅ Real-time communication (sub-second latency)

✅ Reads live robot state without screenshot scraping

✅ Sends commands from Python back to the browser

✅ Keeps the application hosting fully static

✅ Includes clear setup instructions and architecture explanation