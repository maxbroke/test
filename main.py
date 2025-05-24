from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
import sqlite3
import time

DB_FILE = 'database.sqlite3'
COOLDOWN = 15  # seconds

app = FastAPI()

HTML_CONTENT = """<!DOCTYPE html>
<html>
<head>
<title>Button App</title>
<style>
body {font-family: Arial, sans-serif; text-align: center; margin-top: 50px;}
#press-btn {
  width: 200px;
  height: 60px;
  background: linear-gradient(#4CAF50, #2E7D32);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 20px;
  box-shadow: 0 6px #1B5E20;
  transition: transform 0.1s, box-shadow 0.1s;
}
#press-btn.pressed {
  transform: translateY(4px);
  box-shadow: 0 2px #1B5E20;
}
#timer { margin-bottom: 20px; font-size: 24px; }
</style>
</head>
<body>
<div id="timer"></div>
<button id="press-btn">Press me</button>
<script>
let remaining = 0;
const COOLDOWN = 15;
async function fetchState() {
  const res = await fetch('/state');
  if (res.ok) {
    const data = await res.json();
    remaining = data.remaining;
    updateUI();
  }
}
function updateUI() {
  const btn = document.getElementById('press-btn');
  const timer = document.getElementById('timer');
  if (remaining > 0) {
    btn.classList.add('pressed');
    btn.disabled = true;
    timer.textContent = `Wait ${remaining}s`;
  } else {
    btn.classList.remove('pressed');
    btn.disabled = false;
    timer.textContent = '';
  }
}
async function press() {
  const res = await fetch('/press', {method: 'POST'});
  if (res.ok) {
    remaining = COOLDOWN;
  }
}
setInterval(() => { if (remaining > 0) { remaining--; updateUI(); } }, 1000);
setInterval(fetchState, 5000);
fetchState();
document.getElementById('press-btn').addEventListener('click', press);
</script>
</body>
</html>"""

def get_conn():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("CREATE TABLE IF NOT EXISTS state (id INTEGER PRIMARY KEY, last_pressed REAL)")
    return conn

def get_last(conn):
    cur = conn.execute("SELECT last_pressed FROM state WHERE id=1")
    row = cur.fetchone()
    return row[0] if row else None

def set_last(conn, ts):
    conn.execute("INSERT OR REPLACE INTO state (id, last_pressed) VALUES (1, ?)", (ts,))
    conn.commit()

@app.get('/', response_class=HTMLResponse)
def index():
    return HTML_CONTENT

@app.get('/state')
def state():
    conn = get_conn()
    last = get_last(conn)
    now = time.time()
    remaining = int(COOLDOWN - (now - last)) if last else 0
    if remaining < 0:
        remaining = 0
    pressed = remaining > 0
    conn.close()
    return {'pressed': pressed, 'remaining': remaining}

@app.post('/press')
def press():
    conn = get_conn()
    last = get_last(conn)
    now = time.time()
    if last and now - last < COOLDOWN:
        remaining = int(COOLDOWN - (now - last))
        conn.close()
        raise HTTPException(status_code=400, detail={'remaining': remaining})
    set_last(conn, now)
    conn.close()
    return {'pressed': True}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)

