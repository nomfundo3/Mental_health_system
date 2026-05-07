# Software Requirements Specification

## Project Title
AI-Powered Mental Health Chatbot Assistant for Student Support

## Purpose
This system provides first-line mental health support for students through a web-based chatbot experience. It offers supportive conversation, mood check-ins, resource recommendations, and safety escalation for high-risk messages.

## Problem Statement
Students often experience stress, anxiety, burnout, and emotional pressure while facing limited access to immediate support. Traditional counselling services may be delayed, costly, or difficult to access after hours.

## Proposed Solution
The project delivers a web application where students can:
- register and log in
- start and continue support chat sessions
- complete mood check-ins
- receive coping guidance and referral resources
- trigger safer fallback responses when distress risk is high

## Stakeholders
- Students and young adults seeking support
- Lecturers evaluating the project
- Support staff or administrators reviewing flagged interactions
- Development team maintaining the application

## Functional Requirements
1. The system shall allow a user to register with consent acceptance.
2. The system shall allow a user to log in using username or email.
3. The system shall allow a user to start a new chat session.
4. The system shall store chat sessions and messages.
5. The system shall assess a message for sentiment and risk level.
6. The system shall provide supportive assistant replies.
7. The system shall provide safer escalation messaging for high-risk content.
8. The system shall allow users to record mood check-ins.
9. The system shall list support resources by recommendation category.
10. The system shall provide a restricted flagged-message review endpoint for support/admin roles.
11. The system shall provide an admin dashboard summary endpoint.
12. The system shall allow demo bootstrap and resource seeding for presentation setup.

## Non-Functional Requirements
- Usability: the interface shall be simple, calm, and presentation-ready.
- Security: passwords shall be hashed using Django authentication.
- Maintainability: the system shall use modular Django apps and service functions.
- Portability: the project shall run with SQLite by default for easier classroom demos.
- Reliability: key backend workflows shall be covered by automated tests.
- Performance: normal API responses should complete within a few seconds in local demo conditions.

## AI-Specific Requirements
- Input: plain-text user messages
- Output: supportive, non-diagnostic responses
- Safety control: high-risk messages shall trigger fallback escalation responses
- Transparency: the UI shall state that the system is not a licensed professional
- Reviewability: flagged content shall be visible to support/admin reviewers

## Scope
### Included
- authentication
- chat sessions
- mood tracking
- recommendation resources
- risk detection
- admin review endpoints
- deployment and demo setup files

### Excluded
- medical diagnosis
- prescribing medication
- live therapist communication
- emergency intervention beyond referral guidance
- full LLM-grade conversation quality

## Acceptance Criteria
- a new user can register successfully
- a user can log in successfully
- a chat message creates or updates a session
- medium-risk messages return supportive coping guidance
- high-risk messages return escalation guidance and become flagged
- mood check-ins can be saved
- support resources can be loaded
- admin/support users can access flagged-message data

## Current Limitation
The chatbot currently uses rules-based response logic rather than a real large language model. This is suitable for a semester prototype but not equivalent to ChatGPT-quality conversation.
