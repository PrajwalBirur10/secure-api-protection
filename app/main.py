from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from utils.security_check import analyze_text
from datetime import datetime
import json, os

app = FastAPI(title="Secure API Protection Dashboard")

# Serve UI assets
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

LOG_FILE = "scan_logs.json"

def write_log(entry: dict):
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f:
            json.dump([], f)
    with open(LOG_FILE, "r+") as f:
        data = json.load(f)
        data.append(entry)
        f.seek(0)
        json.dump(data, f, indent=2)

@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/scan", response_class=HTMLResponse)
def scan_input(request: Request, text: str = Form(...)):
    result = analyze_text(text)
    log = {"time": str(datetime.now()), "input": text, "result": result}
    write_log(log)
    return templates.TemplateResponse("index.html", {"request": request, "result": result})

@app.get("/logs", response_class=HTMLResponse)
def show_logs(request: Request):
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            logs = json.load(f)
    else:
        logs = []
    return templates.TemplateResponse("logs.html", {"request": request, "logs": logs})

@app.get("/health")
def health():
    return {"status": "healthy"}
