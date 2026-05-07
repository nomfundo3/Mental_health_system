# AI-Powered Mental Health Chatbot Assistant for Student Support

This project is a presentation-ready semester prototype for student mental health support. It provides:

- registration and login
- session-based chatbot conversations
- mood check-ins
- support resource recommendations
- risk detection and crisis fallback
- restricted admin/support review for flagged messages
- demo bootstrap data
- CI and deployment starter files

## Stack
- Django 5
- Django REST Framework
- SQLite by default for demos
- Optional PostgreSQL via environment variables
- HTML/CSS/JavaScript frontend rendered from Django templates

## Quick Start
1. Install dependencies:

```bash
pip install -r backend/requirements.txt
```

2. Run migrations:

```bash
cd backend
python manage.py migrate
```

3. Seed support resources and demo users:

```bash
python manage.py seed_resources
python manage.py bootstrap_demo
```

4. Start the server:

```bash
python manage.py runserver
```

## Demo Accounts
- Student: `studentdemo` / `StrongPass123!`
- Support admin: `supportdemo` / `StrongPass123!`

## Main Endpoints
- `POST /api/users/register/`
- `POST /api/users/login/`
- `GET /api/users/me/`
- `POST /api/users/logout/`
- `GET /api/chat/sessions/`
- `POST /api/chat/message/`
- `POST /api/chat/mood-checkins/`
- `GET /api/recommendations/`
- `GET /api/admin-panel/dashboard/`
- `GET /api/admin-panel/flagged-messages/`
- `GET /api/ai/health/`

## Testing
Run the backend test suite:

```bash
cd backend
python manage.py test apps.users.tests apps.chat.tests apps.admin_panel.tests
```

## Documentation
- [Project Starter Plan](./docs/project_starter_plan.md)
- [SRS](./docs/srs.md)
- [Architecture](./docs/architecture.md)
- [QA Report](./docs/qa_report.md)
- [Presentation Guide](./docs/presentation_guide.md)

## Honest Status
The application is working and presentation-ready as a semester prototype. The chatbot is still rules-based, so it is not yet equivalent to a true large language model such as ChatGPT.
