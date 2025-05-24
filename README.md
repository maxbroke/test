# Button App

A simple web application with a 3D button written in Python using FastAPI and SQLite.

## Requirements
- Python 3.8+
- fastapi
- uvicorn

These packages are preinstalled in the Codex environment.

## Usage

Run the application:

```bash
python3 main.py
```

Open your browser at `http://localhost:8000` to see the button.

Pressing the button stores the timestamp in the database and keeps the button pressed for 15 seconds. During this cooldown, a countdown timer is shown.
