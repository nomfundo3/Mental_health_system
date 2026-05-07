# Presentation Guide

## Demo Goal
Show that the system provides a safe, structured first-line mental health support workflow for students.

## Before Presenting
1. Open a terminal in `mental_health_chatbot/backend`
2. Run:
```bash
..\.venv\Scripts\python.exe manage.py migrate
..\.venv\Scripts\python.exe manage.py seed_resources
..\.venv\Scripts\python.exe manage.py bootstrap_demo
..\.venv\Scripts\python.exe manage.py runserver
```
3. Open the home page in the browser

## Demo Accounts
- Student: `studentdemo` / `StrongPass123!`
- Support admin: `supportdemo` / `StrongPass123!`

## Suggested Demo Flow
1. Show the homepage layout and explain that it is a student mental health support assistant.
2. Register a new student or use the demo student account.
3. Log in and open a new chat.
4. Send a message like:
   - `I feel stressed about exams and deadlines.`
5. Show saved session history and resources.
6. Save a mood check-in.
7. Log in as support/admin and load flagged review.
8. Send a high-risk demo message such as:
   - `I feel like I want to hurt myself.`
9. Show that the system escalates safely and flags the interaction.

## Talking Points for Lecturers
- The system is not presented as a therapist or diagnostic tool.
- It uses clear safety boundaries and escalation guidance.
- The backend is modular and test-covered.
- The app is portable for demo environments because SQLite is the default.
- CI, Docker, and deployment starter files are included.

## Honest Limitation
The chatbot is not yet equivalent to ChatGPT because it still uses rules-based assistant responses. The project demonstrates safe workflow design, architecture, and support features rather than a production-grade conversational model.
