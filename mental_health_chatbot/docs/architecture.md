# System Architecture

## Overview
The project uses a layered Django web architecture with a browser-based frontend rendered from server templates.

## Layers
1. Presentation Layer
   - Django template: `backend/templates/home.html`
   - Frontend behavior: `backend/static/js/home.js`
   - Styling: `backend/static/css/home.css`

2. Application Layer
   - `apps.users` for registration, login, logout, and current-user APIs
   - `apps.chat` for chat sessions, chat messages, and mood check-ins
   - `apps.recommendations` for support resource retrieval
   - `apps.admin_panel` for flagged review and dashboard summaries
   - `apps.ai_engine` for service health visibility

3. Domain / Service Layer
   - `services.sentiment_service` for risk and sentiment assessment
   - `services.response_service` for supportive response generation
   - `services.nlp_service` for message analysis abstraction

4. Data Layer
   - SQLite by default for local/demo portability
   - PostgreSQL supported when `DB_ENGINE=postgresql`

## Runtime Flow
1. User registers or logs in
2. Frontend stores active username in the session workflow
3. User sends a chat message to `/api/chat/message/`
4. Backend assesses sentiment/risk
5. Backend stores both user and assistant messages
6. Backend returns updated session data plus recommended resources
7. High-risk messages are flagged and visible to support/admin endpoints

## Simplified Component Diagram
```text
Browser UI
  |
  v
Django Template + Static JS/CSS
  |
  v
REST-style API Views
  |
  +--> Users App
  +--> Chat App
  +--> Recommendations App
  +--> Admin Panel App
  +--> AI Health App
  |
  v
Service Functions
  |
  v
SQLite / PostgreSQL
```

## Security Notes
- authentication uses Django sessions
- admin panel endpoints require authenticated support/admin access
- passwords are stored hashed, never plain text

## Deployment Notes
- `Dockerfile` provided for backend containerization
- `docker-compose.yml` provided for local container startup
- `Procfile` provided for simple platform deployment flow
- GitHub Actions CI runs checks, migrations, and backend tests
