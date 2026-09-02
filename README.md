# Robot Explorer Bridge

A real-time bridge between a hosted static Three.js application and a local Python program using WebSockets.

The Robot Explorer application is hosted on GitHub Pages as a completely static website. A local Python script connects to the running browser session and can both receive live robot state updates and send commands back to the robot.

---

## Assignment Goal

The challenge was to prove that a fully static hosted web application can still communicate with a Python program running on a local machine without converting the website into a traditional client-server application.

This project demonstrates that by creating a direct WebSocket connection between the browser and a local Python process.

---

## Architecture

```text
Hosted Web App (GitHub Pages)
            │
            │ WebSocket
            ▼
Local Python Program
     ws://localhost:8765
```

The website remains a static HTML page hosted on GitHub Pages.

When the page loads, it opens a WebSocket connection to a Python server running on the user's machine.

This creates a real-time two-way communication channel:

- Browser → Python
  - Sends robot position and rotation continuously.

- Python → Browser
  - Sends movement commands to control the robot.

---

## Hosted Application

Open the application:

https://sagarbawanthade.github.io/devops-assignment/

---

## Features

### 1. Read Live State from the Browser

The browser continuously streams robot state data to Python:

```text
x=12.54 z=31.28 rot=1.57
x=12.60 z=31.35 rot=1.57
x=12.68 z=31.43 rot=1.57
```

This data is generated directly from the Three.js scene and is not obtained through screenshots or image processing.

---

### 2. Send Commands from Python

Python can send commands back to the browser:

```json
{
  "forward": true
}
```

The browser receives the command and applies it to the robot controls.

Example:

```python
await websocket.send(
    json.dumps({
        "forward": True
    })
)
```

The robot immediately starts moving forward inside the hosted application.

---

## Project Structure

```text
devops-assignment/
│
├── index.html
│
├── python/
│   └── server.py
│
└── README.md
```

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/sagarbawanthade/devops-assignment.git

cd devops-assignment
```

---

### 2. Create a Virtual Environment (Optional)

Linux / macOS:

```bash
python -m venv .venv

source .venv/bin/activate
```

Windows:

```bash
python -m venv .venv

.venv\Scripts\activate
```

---

### 3. Install Dependencies

```bash
pip install websockets
```

---

### 4. Start the Python Server

```bash
python python/server.py
```

Expected output:

```text
Listening on ws://localhost:8765
```

---

### 5. Open the Hosted Website

Visit:

```text
https://sagarbawanthade.github.io/devops-assignment/
```

Open Developer Tools (F12) and you should see:

```text
Connected to Python bridge
```

The Python terminal will begin receiving robot state updates immediately.

---

## Example Output

Python terminal:

```text
Browser connected

x=0.00 z=14.21 rot=0.00
x=0.00 z=14.29 rot=0.00
x=0.00 z=14.37 rot=0.00
x=0.00 z=14.46 rot=0.00
```

This confirms that the hosted browser page is sending live state information to the local Python program.

---

## Why I Chose WebSockets

I chose WebSockets because they provide a simple and reliable way to achieve real-time two-way communication.

Benefits of this approach:

- Very low latency
- Easy to understand
- Minimal code
- No browser extension required
- No additional hosted backend required
- Works directly with a static website

Alternative approaches such as browser extensions, WebRTC, browser automation tools, or external relay servers would add extra complexity for this assignment.

---

## Trade-offs

### Advantages

- Real-time communication
- Two-way data exchange
- Simple architecture
- Easy to reproduce
- Keeps hosting fully static
- No screenshot scraping

### Limitations

- Requires a local Python server to be running
- Browser must be able to reach localhost
- No authentication is implemented
- Intended for local development and demonstration purposes

---

## Requirements Checklist

### Works against a hosted URL

✅ Yes

The application runs from GitHub Pages and not from `localhost` or `file://`.

---

### Real-time communication

✅ Yes

Robot state is streamed continuously through WebSockets with sub-second latency.

---

### Read live state from the page

✅ Yes

Python receives robot coordinates and rotation directly from the running Three.js application.

---

### Write into the page

✅ Yes

Python can send commands to the browser that control robot movement.

---

### Static hosting remains unchanged

✅ Yes

The website is still a plain static HTML application hosted on GitHub Pages.

No backend was added to the hosting environment.

---

### Code is understandable

✅ Yes

The solution uses a straightforward WebSocket connection with minimal code and clear data flow.

---

## Conclusion

This project demonstrates that a completely static web application can communicate with a local Python program in real time.

The hosted Three.js application streams robot state data to Python while also accepting commands from Python, creating a full bidirectional bridge without introducing any backend infrastructure to the hosted website.
