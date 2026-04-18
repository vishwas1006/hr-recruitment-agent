# HR Recruitment Agent System

## 📌 Overview

This project is an AI-powered HR recruitment system that automates the hiring pipeline from resume submission to interview screening and management. It uses a stateful agent workflow built with LangGraph and provides a dashboard and chatbot for HR operations.

---

## 🚀 Features

* Resume submission and ATS-based scoring
* Technical interview question generation
* HR screening questions
* Candidate dashboard with status tracking
* WebSocket-based HR chatbot
* Candidate status updates via chatbot
* Role creation simulation
* Persistent data storage using SQLite

---

## 🧠 Architecture

User → FastAPI Backend → LangGraph Agent Workflow
          ↓
       SQLite Database
          ↓
    Dashboard + WebSocket Chatbot

---

## ⚙️ Technology Choices

* **FastAPI**: Used for building high-performance backend APIs
* **LangGraph**: Implements stateful multi-step agent workflow (ATS → Interview → HR)
* **SQLite**: Provides lightweight persistent storage for candidate data
* **WebSockets**: Enables real-time chatbot interaction
* **Python**: Core programming language

---

## 🧩 System Design

### Agent Workflow (LangGraph)

* ATS Node: Scores resume
* Interview Node: Generates technical questions
* HR Node: Generates HR screening questions
* Shared state carries data across nodes (short-term memory)

### Memory

* **Short-Term Memory**: Managed through LangGraph state
* **Long-Term Memory**: Stored in SQLite database

### Chatbot

* WebSocket-based
* Queries only database (no hallucination)
* Supports:

  * Viewing candidates
  * Counting candidates
  * Updating candidate status
  * Creating roles

---

## ▶️ Setup Instructions

1. Clone the repository:
   git clone <your-repo-link>

2. Navigate to project folder:
   cd hr-recruitment-agent

3. Create virtual environment:
   python -m venv venv

4. Activate environment:
   venv\Scripts\activate   (Windows)

5. Install dependencies:
   pip install -r requirements.txt

6. Run the application:
   uvicorn main:app --reload

7. Open in browser:
   http://127.0.0.1:8000

---

## 🎯 Demo Flow

1. Submit candidate with Python skills → Interview + HR questions
2. Submit candidate without Python → Rejected
3. View dashboard → Shows all candidates
4. Open chatbot → Perform queries:

   * all
   * selected
   * rejected
   * count
   * update <name> <status>
   * create role <role>

---

## 📂 Project Structure

* main.py → FastAPI application and routes
* agent.py → LangGraph agent workflow
* database.py → Database models and connection
* requirements.txt → Dependencies
* README.md → Project documentation

---

## ✅ Key Highlights

* Uses LangGraph for stateful agent execution
* Implements both short-term and long-term memory
* Chatbot responses are strictly database-driven
* Clean and minimal UI for demonstration
