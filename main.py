from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from agent import graph  
from database import SessionLocal,Candidate

app = FastAPI()


# candidates = []


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
    #  LangGraph execution
    result = graph.invoke({
        "name": name,
        "email": email,
        "resume": resume
    })

    score = result["score"]
    status = result["status"]
    questions = result.get("questions", [])
    hr_questions = result.get("hr_questions", [])

    # SAVE TO DATABASE
    db = SessionLocal()

    new_candidate = Candidate(
        name=name,
        email=email,
        score=score,
        status=status
    )

    db.add(new_candidate)
    db.commit()
    db.close()

    print("Saved to DB")



    # Rejection case
    if status == "Rejected":
        return f"""
        <h3>Rejected (Score: {score})</h3>
        <a href='/'>Back</a>
        """

    # Build question UI
    q_html = ""

    for q in questions:
        q_html += f"<p>{q}</p><input type='text'><br>"

    for q in hr_questions:
        q_html += f"<p>{q}</p><input type='text'><br>"

    return f"""
    <h3>Interview + HR Round</h3>
    <p><b>Name:</b> {name}</p>
    <p><b>Email:</b> {email}</p>
    {q_html}
    <br>
    <a href="/dashboard">Go to Dashboard</a>
    """

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    db = SessionLocal()
    data = db.query(Candidate).all()

    html = "<h2>Dashboard</h2>"

    for c in data:
        html += f"""
        <div style="border:1px solid black; padding:10px; margin:10px;">
            <p><b>Name:</b> {c.name}</p>
            <p><b>Email:</b> {c.email}</p>
            <p><b>Score:</b> {c.score}</p>
            <p><b>Status:</b> {c.status}</p>
        </div>
        """

    db.close()
    return html