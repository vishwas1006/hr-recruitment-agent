from fastapi import FastAPI, Form, WebSocket
from fastapi.responses import HTMLResponse
from agent import graph
from database import SessionLocal, Candidate

app = FastAPI()


# ---------------- HOME ----------------
@app.get("/", response_class=HTMLResponse)
async def home():
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

    <br>
    <a href="/dashboard">View Dashboard</a><br>
    <a href="/chat-ui">Open Chatbot</a>
    """


# ---------------- SUBMIT ----------------
@app.post("/submit", response_class=HTMLResponse)
async def submit(
    name: str = Form(...),
    email: str = Form(...),
    resume: str = Form(...)
):
    result = graph.invoke({
        "name": name,
        "email": email,
        "resume": resume
    })

    score = result["score"]
    status = result["status"]
    questions = result.get("questions", [])
    hr_questions = result.get("hr_questions", [])

    db = SessionLocal()
    db.add(Candidate(name=name, email=email, score=score, status=status))
    db.commit()
    db.close()

    if status == "Rejected":
        return f"""
        <h3>Rejected (Score: {score})</h3>
        <a href='/'>Back</a>
        """

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


# ---------------- DASHBOARD ----------------
@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    db = SessionLocal()
    data = db.query(Candidate).all()
    db.close()

    html = f"<h2>Dashboard (Total: {len(data)})</h2>"

    for c in data:
        color = "green" if c.status != "Rejected" else "red"

        html += f"""
        <div style="border:1px solid black; padding:10px; margin:10px;">
            <p><b>Name:</b> {c.name}</p>
            <p><b>Email:</b> {c.email}</p>
            <p><b>Score:</b> {c.score}</p>
            <p><b>Status:</b> <span style="color:{color}">{c.status}</span></p>
        </div>
        """

    return html

# ---------------- CLEAR DATABASE ----------------
@app.get("/clear")
async def clear_data():
    db = SessionLocal()
    db.query(Candidate).delete()
    db.commit()
    db.close()
    return {"message": "All data cleared"}

# ---------------- CHAT UI ----------------
@app.get("/chat-ui", response_class=HTMLResponse)
async def chat_ui():
    return """
    <h2>HR Chatbot (WebSocket)</h2>

    <input id="msg" placeholder="Type..." />
    <button onclick="sendMsg()">Send</button>

    <pre id="chat"></pre>

    <p>Try:</p>
    <ul>
        <li>all</li>
        <li>selected</li>
        <li>rejected</li>
        <li>count</li>
        <li>update Vishwas selected</li>
        <li>create role python developer</li>
    </ul>

    <script>
        const ws = new WebSocket("ws://127.0.0.1:8000/ws/chat");

        ws.onmessage = function(event) {
            document.getElementById("chat").innerText += event.data + "\\n";
        };

        function sendMsg() {
            let input = document.getElementById("msg");
            ws.send(input.value);
            input.value = "";
        }
    </script>
    """


# ---------------- WEBSOCKET CHATBOT ----------------
@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()

    db = SessionLocal()

    try:
        while True:
            data = await websocket.receive_text()
            query = data.lower()

            candidates = db.query(Candidate).all()
            response = ""

            if "all" in query:
                for c in candidates:
                    response += f"{c.name} - {c.status}\n"

            elif "selected" in query:
                for c in candidates:
                    if c.status != "Rejected":
                        response += f"{c.name} - {c.status}\n"

            elif "rejected" in query:
                for c in candidates:
                    if c.status == "Rejected":
                        response += f"{c.name} - Rejected\n"

            elif "count" in query:
                response = f"Total: {len(candidates)}"

            elif "update" in query:
                parts = query.split()

                if len(parts) >= 3:
                    name = parts[1]
                    new_status = parts[2].capitalize()

                    candidate = db.query(Candidate).filter(Candidate.name == name).first()

                    if candidate:
                        candidate.status = new_status
                        db.commit()
                        response = f"{name} status updated to {new_status}"
                    else:
                        response = "Candidate not found"
                else:
                    response = "Usage: update <name> <status>"

            elif "create role" in query:
                response = "New role created. Email templates prepared."

            else:
                response = "Try: all, selected, rejected, count, update <name> <status>, create role <role>"

            await websocket.send_text(response)
   
    except:
        db.close()