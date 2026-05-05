# AI-Powered Mental Health Chatbot

This repository now includes a usable backend starter for the project proposal:

- Django project configuration
- Custom user model
- Chat sessions and chat messages
- Mood check-ins
- Resource recommendations
- Flagged-message admin endpoint
- Rules-based sentiment and crisis detection starter

## Backend setup

1. Create a virtual environment.
2. Install dependencies:

```bash
pip install -r backend/requirements.txt
```

3. Run migrations:

```bash
cd backend
python manage.py makemigrations
python manage.py migrate
```

4. Start the server:

```bash
python manage.py runserver
```

## Starter API endpoints

- `POST /api/users/register/`
- `GET /api/chat/sessions/`
- `POST /api/chat/message/`
- `POST /api/chat/mood-checkins/`
- `GET /api/recommendations/`
- `GET /api/admin-panel/flagged-messages/`
- `GET /api/ai/health/`

## Suggested sprint 1 focus

- Connect a simple frontend chat UI
- Seed recommendation resources
- Add tests for chat safety flows
- Add authentication and permissions
- Replace rules-based responses with an LLM integration when ready
