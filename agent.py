from langgraph.graph import StateGraph

# State object (dict is enough)
class State(dict):
    pass


# ---------------- NODE 1 ----------------
# ATS Scoring
def ats_node(state: State):
    resume = state["resume"]

    score = 80 if "python" in resume.lower() else 60

    state["score"] = score
    state["status"] = "Interview" if score >= 80 else "Rejected"

    return state


# ---------------- NODE 2 ----------------
# Interview Questions
def interview_node(state: State):
    if state["status"] == "Rejected":
        return state

    state["questions"] = [
        "What is Python?",
        "Explain OOP?",
        "What is API?"
    ]

    return state


# ---------------- NODE 3 ----------------
# HR Screening
def hr_node(state: State):
    if state["status"] == "Rejected":
        return state

    state["hr_questions"] = [
        "What is your notice period?",
        "When can you join?"
    ]

    return state


# ---------------- BUILD GRAPH ----------------
builder = StateGraph(State)

builder.add_node("ats", ats_node)
builder.add_node("interview", interview_node)
builder.add_node("hr", hr_node)

builder.set_entry_point("ats")

builder.add_edge("ats", "interview")
builder.add_edge("interview", "hr")

graph = builder.compile()