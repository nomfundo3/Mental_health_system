# Project Starter Plan

## What has been set up

- Django backend foundation
- API routes for registration, chat, mood tracking, resources, and flagged messages
- Starter safety logic for distress and crisis wording

## Best next steps for the team

1. Install dependencies and run migrations.
2. Create Django migrations for the new apps.
3. Add seed data for campus counselling contacts and emergency resources.
4. Build a minimal frontend with:
   - login/register form
   - chat box
   - mood check-in form
   - resources panel
5. Add tests for:
   - normal support response
   - medium-risk distress response
   - high-risk crisis escalation
6. Decide which AI provider to integrate for empathetic responses.

## Basic API payloads

### Register

```json
{
  "username": "student1",
  "email": "student@example.com",
  "password": "strongpass123",
  "consent_accepted": true
}
```

### Send chat message

```json
{
  "username": "student1",
  "message": "I feel stressed about exams and I can't focus"
}
```

### Mood check-in

```json
{
  "mood": "stressed",
  "notes": "Too many deadlines this week"
}
```
