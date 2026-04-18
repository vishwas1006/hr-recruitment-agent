from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from agent import graph

app = FastAPI()

# Simple in-memory storage
candidates = []


@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <h2>HR Recruitment Agent</h2>
    <form action="/submit" method="post">
        
        Name: <br>
        <input type="text" name="name" required><br><br>

        Email: <br>
        <input type="email" name="email" required><br><br>

        Resume: <br>
        <textarea name="resume" rows="10" cols="50" placeholder="Paste Resume"></textarea><br><br>

        <button type="submit">Submit</button>
    </form>
    """


@app.post("/submit", response_class=HTMLResponse)
def submit(
    name: str = Form(...),
    email: str = Form(...),
    resume: str = Form(...)
):
    score = 80 if "python" in resume.lower() else 60

    questions = [
        "What is Python?",
        "Explain OOP?",
        "What is API?"
    ]

    candidate = {
        "name": name,
        "email": email,
        "resume": resume,
        "score": score,
        "status": "Interview" if score >= 80 else "Rejected",
        "questions": questions
    }

    candidates.append(candidate)
    print("Email sent to candidate")

    if score < 80:
        return f"""
        <h3>Rejected (Score: {score})</h3>
        <a href='/'>Back</a>
        """

    # Show interview questions
    q_html = ""
    for q in questions:
        q_html += f"<p>{q}</p><input type='text'><br>"

    return f"""
    <h3>Interview Round</h3>
    {q_html}
    <br>
    <a href="/dashboard">Go to Dashboard</a>
    """


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    html = "<h2>Dashboard</h2>"

    for c in candidates:
        html += f"""
        <div style="border:1px solid black; padding:10px; margin:10px;">
            <p><b>Name:</b> {c['name']}</p>
            <p><b>Email:</b> {c['email']}</p>
            <p><b>Score:</b> {c['score']}</p>
            <p><b>Status:</b> {c['status']}</p>
        </div>
        """

    return html