from fastapi import FastAPI, Request, Form, HTTPException, Header
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from utils.security_check import analyze_text
from datetime import datetime
import os
from utils.db import save_log, get_logs
from collections import Counter

# Get API_KEY from environment variable or fallback to "dev-key" if not set
API_KEY = os.getenv("API_KEY", "dev-key")

# Create FastAPI app instance
app = FastAPI(title="Secure API Protection Dashboard")

# Serve static files (CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Jinja2 templates directory
templates = Jinja2Templates(directory="templates")

# Root endpoint to render the dashboard
@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# POST endpoint to handle scan requests with API key validation
@app.post("/scan", response_class=HTMLResponse)
def scan_input(
    request: Request,
    text: str = Form(...),
    x_api_key: str = Header(default=None)
):
    # Allow no key for web form, require key for API clients
    user_agent = request.headers.get("user-agent", "")
    if "Mozilla" not in user_agent and x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid API key")

    result = analyze_text(text)
    save_log(text, result["status"], result["score"])
    return templates.TemplateResponse("index.html", {"request": request, "result": result})

# Endpoint to show scan logs
@app.get("/logs", response_class=HTMLResponse)
def show_logs(request: Request):
    # Fetch the logs from the database (or other storage)
    logs = get_logs()
    
    # Return the logs in the logs.html template
    return templates.TemplateResponse("logs.html", {"request": request, "logs": logs})

@app.get("/metrics")
def metrics():
    logs = get_logs()
    risks = [log.result for log in logs if "Risk" in log.result]
    summary = dict(Counter(risks))
    avg_score = sum(log.score for log in logs) / len(logs) if logs else 0
    return {
        "total_scans": len(logs),
        "avg_risk_score": avg_score,
        "risk_summary": summary
    }

# Health check endpoint
@app.get("/health")
def health():
    return {"status": "healthy"}

