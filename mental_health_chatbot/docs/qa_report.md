# QA and Testing Report

## Testing Scope
The project was tested around the core presentation workflow:
- registration
- login
- current-user lookup
- logout
- session creation through chat
- medium-risk and high-risk message handling
- mood check-in creation
- support/admin dashboard authorization
- flagged-message retrieval

## Automated Test Modules
- `apps.users.tests`
- `apps.chat.tests`
- `apps.admin_panel.tests`

## Verified Scenarios
1. User registration creates a new account.
2. Login works with email.
3. Current-user endpoint returns authenticated user data.
4. Logout endpoint returns success.
5. Sending a normal distress message creates a session and assistant response.
6. Sending a high-risk message marks the session as escalated.
7. Mood check-ins attach correctly to user and session.
8. Admin dashboard access is blocked for unauthorized users and allowed for admin/support users.

## Manual QA Checklist
- Homepage loads correctly
- Modal login/register opens and closes
- New chat button resets the active session
- Chat history loads after login
- Resources drawer loads recommendation cards
- Mood check-in form submits successfully
- Flagged review drawer requires support/admin authentication

## Known Limitation
- The conversational quality is intentionally simple because the assistant is still rules-based
- No browser automation suite is included yet

## Recommendation
For future work, add Selenium or Playwright-based UI smoke tests to validate the full browser workflow automatically.
