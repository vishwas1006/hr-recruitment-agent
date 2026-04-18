from langgraph.graph import StateGraph

# State object (dict is enough)
from typing import TypedDict, List

class State(TypedDict, total=False):
    name: str
    email: str
    resume: str
    score: int
    status: str
    questions: List[str]
    hr_questions: List[str]

# ---------------- NODE 1 ----------------
# ATS Scoring
def ats_node(state: State):
    resume = state["resume"]

    score = 80 if "python" in resume.lower() else 60
    status = "Interview" if score >= 80 else "Rejected"

    return {
        "score": score,
        "status": status
    }


# ---------------- NODE 2 ----------------
# Interview Questions
def interview_node(state: State):
    if state["status"] == "Rejected":
        return {}

    return {
        "questions": [
            "What is Python?",
            "Explain OOP?",
            "What is API?"
        ]
    }

# ---------------- NODE 3 ----------------
# HR Screening
def hr_node(state: State):
    if state["status"] == "Rejected":
        return {}

    return {
        "hr_questions": [
            "What is your notice period?",
            "When can you join?"
        ]
    }


# ---------------- BUILD GRAPH ----------------
builder = StateGraph(State)

builder.add_node("ats", ats_node)
builder.add_node("interview", interview_node)
builder.add_node("hr", hr_node)

builder.set_entry_point("ats")

builder.add_edge("ats", "interview")
builder.add_edge("interview", "hr")

graph = builder.compile()