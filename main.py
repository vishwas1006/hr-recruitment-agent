from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Simple in-memory storage
candidates = []

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <h2>HR Recruitment Agent</h2>
    <form action="/submit" method="post">
        <textarea name="resume" rows="10" cols="50" placeholder="Paste Resume"></textarea><br><br>
        <button type="submit">Submit</button>
    </form>
    """

@app.post("/submit", response_class=HTMLResponse)
def submit(resume: str = Form(...)):
    score = 80 if "python" in resume.lower() else 60
    
    candidate = {
        "resume": resume,
        "score": score,
        "status": "Selected" if score >= 80 else "Rejected"
    }
    
    candidates.append(candidate)

    return f"""
    <h3>Result</h3>
    <p>Score: {score}</p>
    <p>Status: {candidate['status']}</p>
    <a href="/">Go Back</a>
    """

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    html = "<h2>Dashboard</h2>"
    
    for c in candidates:
        html += f"<p>Score: {c['score']} | Status: {c['status']}</p>"
    
    return html