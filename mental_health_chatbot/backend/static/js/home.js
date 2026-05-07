const registerForm = document.getElementById("register-form");
const loginForm = document.getElementById("login-form");
const chatForm = document.getElementById("chat-form");
const moodForm = document.getElementById("mood-form");

const registerStatus = document.getElementById("register-status");
const loginStatus = document.getElementById("login-status");
const chatStatus = document.getElementById("chat-status");
const moodStatus = document.getElementById("mood-status");
const resourcesStatus = document.getElementById("resources-status");

const resourcesList = document.getElementById("resources-list");
const responseCard = document.getElementById("chat-response");
const assistantMessage = document.getElementById("assistant-message");
const sentiment = document.getElementById("sentiment");
const riskLevel = document.getElementById("risk-level");

const sessionList = document.getElementById("session-list");
const dashboardStatus = document.getElementById("dashboard-status");
const chatTranscript = document.getElementById("chat-transcript");
const heroEmpty = document.getElementById("hero-empty");
const flaggedList = document.getElementById("flagged-list");

const activeUser = document.getElementById("active-user");
const activeUserMeta = document.getElementById("active-user-meta");
const activeSession = document.getElementById("active-session");
const activeSessionMeta = document.getElementById("active-session-meta");
const activeSafety = document.getElementById("active-safety");
const activeSafetyMeta = document.getElementById("active-safety-meta");
const chatTitle = document.getElementById("chat-title");

const factSessionCount = document.getElementById("fact-session-count");
const factResourceCount = document.getElementById("fact-resource-count");
const factFlaggedCount = document.getElementById("fact-flagged-count");

const stepRegister = document.getElementById("step-register");
const stepLogin = document.getElementById("step-login");
const stepChat = document.getElementById("step-chat");

const newChatButton = document.getElementById("new-chat");
const loadSessionsButton = document.getElementById("load-sessions");
const loadResourcesButton = document.getElementById("load-resources");
const loadFlaggedButton = document.getElementById("load-flagged");
const showMoodPanelButton = document.getElementById("show-mood-panel");

const openLoginButton = document.getElementById("open-login");
const openLoginTopButton = document.getElementById("open-login-top");
const openRegisterButton = document.getElementById("open-register");
const closeAuthModalButton = document.getElementById("close-auth-modal");
const authModal = document.getElementById("auth-modal");
const loginPanel = document.getElementById("login-panel");
const registerPanel = document.getElementById("register-panel");
const accountSummary = document.getElementById("account-summary");
const logoutButton = document.getElementById("logout-button");

const utilityDrawer = document.getElementById("utility-drawer");
const closeDrawerButton = document.getElementById("close-drawer");
const moodPanel = document.getElementById("mood-panel");

let currentUser = null;
let currentSessionId = null;

function setStepState(step, state) {
    step.classList.remove("active-step", "done-step");
    if (state === "active") {
        step.classList.add("active-step");
    }
    if (state === "done") {
        step.classList.add("done-step");
    }
}

function updateOrderedFlow() {
    if (!currentUser) {
        setStepState(stepRegister, "active");
        setStepState(stepLogin, "");
        setStepState(stepChat, "");
        return;
    }

    setStepState(stepRegister, "done");
    setStepState(stepLogin, "done");
    setStepState(stepChat, currentSessionId ? "done" : "active");
}

function openAuthPanel(mode) {
    authModal.classList.remove("hidden");
    loginPanel.classList.toggle("hidden", mode !== "login");
    registerPanel.classList.toggle("hidden", mode !== "register");
}

function closeAuthPanel() {
    authModal.classList.add("hidden");
}

function openDrawer() {
    utilityDrawer.classList.remove("hidden");
}

function closeDrawer() {
    utilityDrawer.classList.add("hidden");
}

function toggleChatEmpty(isEmpty) {
    heroEmpty.classList.toggle("hidden", !isEmpty);
    chatTranscript.classList.toggle("hidden", isEmpty);
}

function setActiveUser(user) {
    currentUser = user;
    document.getElementById("username").value = user ? user.username : "";
    activeUser.textContent = user ? (user.display_name || user.username) : "Guest";
    activeUserMeta.textContent = user
        ? `${user.username} is signed in and ready to continue.`
        : "Register or log in to begin.";
    chatTitle.textContent = user ? `Welcome back, ${user.display_name || user.username}` : "What's on your mind today?";
    accountSummary.classList.toggle("hidden", !user);
    updateOrderedFlow();
}

function setSessionSummary(session) {
    currentSessionId = session ? session.id : null;
    activeSession.textContent = session ? `#${session.id}` : "No session";
    activeSessionMeta.textContent = session
        ? `${session.status} conversation with ${session.messages.length} saved messages.`
        : "A calmer, structured assistant for student wellbeing.";
    updateOrderedFlow();
}

function setSafetySummary(assessment) {
    activeSafety.textContent = assessment ? `${assessment.risk_level.toUpperCase()} risk` : "Monitoring";
    activeSafetyMeta.textContent = assessment
        ? `Sentiment: ${assessment.sentiment}. Categories: ${assessment.resource_categories.join(", ")}.`
        : "Risk detection updates after each message.";
}

function renderTranscript(messages) {
    if (!messages.length) {
        chatTranscript.innerHTML = "";
        toggleChatEmpty(true);
        return;
    }

    toggleChatEmpty(false);
    chatTranscript.innerHTML = messages.map((entry) => `
        <article class="message-row ${entry.role}">
            <div class="avatar">${entry.role === "assistant" ? "S" : "Y"}</div>
            <div class="message-body">
                <p class="message-role">${entry.role === "assistant" ? "Mental Health Assistant" : "You"}</p>
                <p>${entry.content}</p>
                <span class="message-meta">${entry.risk_level} risk | ${entry.source.replace("_", " ")}</span>
            </div>
        </article>
    `).join("");
}

function renderSessions(sessions) {
    factSessionCount.textContent = sessions.length;
    if (!sessions.length) {
        sessionList.className = "session-list empty-state";
        sessionList.textContent = "No sessions saved for this user yet.";
        return;
    }

    sessionList.className = "session-list";
    sessionList.innerHTML = sessions.map((session) => `
        <button type="button" data-session-id="${session.id}" class="session-item ${session.id === currentSessionId ? "active" : ""}">
            <strong>${session.title}</strong>
            <span>${session.last_risk_level} risk</span>
        </button>
    `).join("");
}

function renderResources(resources) {
    factResourceCount.textContent = resources.length;
    resourcesList.innerHTML = "";
    resources.forEach((resource) => {
        const card = document.createElement("article");
        card.className = `resource-item ${resource.is_emergency ? "emergency" : ""}`;
        card.innerHTML = `
            <p class="resource-tag">${resource.category}</p>
            <h3>${resource.title}</h3>
            <p>${resource.description}</p>
            ${resource.url ? `<a href="${resource.url}" target="_blank" rel="noreferrer">Open resource</a>` : ""}
        `;
        resourcesList.appendChild(card);
    });
}

function renderFlagged(flagged) {
    factFlaggedCount.textContent = flagged.length;
    if (!flagged.length) {
        flaggedList.className = "flagged-list empty-state";
        flaggedList.textContent = "No flagged conversations were returned.";
        return;
    }

    flaggedList.className = "flagged-list";
    flaggedList.innerHTML = flagged.map((item) => `
        <article class="flagged-item">
            <h3>Session #${item.session_id}</h3>
            <p>${item.content}</p>
            <span>${item.risk_level} risk | ${item.sentiment} sentiment</span>
        </article>
    `).join("");
}

async function postJson(url, payload = {}) {
    const response = await fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
    });

    const data = await response.json().catch(() => ({}));
    if (!response.ok) {
        const firstError = Object.values(data)[0];
        const message = Array.isArray(firstError) ? firstError[0] : firstError;
        throw new Error(message || `Request failed with status ${response.status}`);
    }

    return data;
}

async function loadCurrentUser() {
    try {
        const response = await fetch("/api/users/me/");
        if (!response.ok) {
            return;
        }
        const payload = await response.json();
        if (payload.authenticated && payload.user) {
            setActiveUser(payload.user);
            await loadSessions();
        }
    } catch (error) {
        // no-op
    }
}

async function loadSessions() {
    const username = document.getElementById("username").value.trim();
    if (!username) {
        dashboardStatus.textContent = "Log in to fetch chat history.";
        renderSessions([]);
        return;
    }

    dashboardStatus.textContent = "Loading sessions...";
    try {
        const response = await fetch(`/api/chat/sessions/?username=${encodeURIComponent(username)}`);
        if (!response.ok) {
            throw new Error(`Request failed with status ${response.status}`);
        }
        const sessions = await response.json();
        dashboardStatus.textContent = sessions.length ? "" : "No saved sessions for this user yet.";
        renderSessions(sessions);
    } catch (error) {
        dashboardStatus.textContent = "Could not load sessions yet.";
    }
}

async function loadResources() {
    resourcesStatus.textContent = "Loading resources...";
    openDrawer();
    try {
        const response = await fetch("/api/recommendations/");
        if (!response.ok) {
            throw new Error(`Request failed with status ${response.status}`);
        }
        const resources = await response.json();
        resourcesStatus.textContent = resources.length ? "" : "No resources have been added yet.";
        renderResources(resources);
    } catch (error) {
        resourcesStatus.textContent = "Could not load resources yet.";
    }
}

async function loadFlaggedMessages() {
    flaggedList.className = "flagged-list empty-state";
    flaggedList.textContent = "Loading flagged cases...";
    openDrawer();
    try {
        const response = await fetch("/api/admin-panel/flagged-messages/");
        if (!response.ok) {
            throw new Error(`Request failed with status ${response.status}`);
        }
        const payload = await response.json();
        renderFlagged(payload.flagged_messages || []);
    } catch (error) {
        flaggedList.textContent = "Support login is required to view flagged cases.";
    }
}

registerForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    registerStatus.textContent = "Creating account...";

    const password = document.getElementById("register-password").value;
    const confirmPassword = document.getElementById("register-confirm-password").value;
    if (password !== confirmPassword) {
        registerStatus.textContent = "Passwords do not match.";
        return;
    }

    const payload = {
        username: document.getElementById("register-username").value.trim(),
        email: document.getElementById("register-email").value.trim(),
        display_name: document.getElementById("register-display-name").value.trim(),
        preferred_language: "en",
        password,
        confirm_password: confirmPassword,
        consent_accepted: document.getElementById("register-consent").checked,
    };

    try {
        const data = await postJson("/api/users/register/", payload);
        registerStatus.textContent = `Account created for ${data.user.username}. You can log in now.`;
        registerForm.reset();
        setStepState(stepRegister, "done");
        setStepState(stepLogin, "active");
        openAuthPanel("login");
    } catch (error) {
        registerStatus.textContent = error.message || "Could not create the account yet.";
    }
});

loginForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    loginStatus.textContent = "Signing you in...";

    const payload = {
        identifier: document.getElementById("login-identifier").value.trim(),
        password: document.getElementById("login-password").value,
    };

    try {
        const data = await postJson("/api/users/login/", payload);
        loginStatus.textContent = "Login successful.";
        setActiveUser(data.user);
        closeAuthPanel();
        await loadSessions();
    } catch (error) {
        loginStatus.textContent = error.message || "Could not log in yet.";
    }
});

chatForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    chatStatus.textContent = "Sending message...";

    const payload = {
        username: document.getElementById("username").value,
        message: document.getElementById("message").value.trim(),
        session_id: currentSessionId,
    };

    if (!payload.username) {
        chatStatus.textContent = "Please log in before chatting.";
        openAuthPanel("login");
        return;
    }

    if (!payload.message) {
        chatStatus.textContent = "Type a message first.";
        return;
    }

    try {
        const data = await postJson("/api/chat/message/", payload);
        const messages = data.session.messages;
        const lastAssistantMessage = [...messages].reverse().find((entry) => entry.role === "assistant");

        assistantMessage.textContent = lastAssistantMessage ? lastAssistantMessage.content : "No response received.";
        sentiment.textContent = data.assessment.sentiment;
        riskLevel.textContent = data.assessment.risk_level;
        responseCard.classList.remove("hidden");
        chatStatus.textContent = "Message sent successfully.";
        setSessionSummary(data.session);
        setSafetySummary(data.assessment);
        renderTranscript(messages);
        renderResources(data.resources);
        await loadSessions();
        document.getElementById("message").value = "";
    } catch (error) {
        chatStatus.textContent = error.message || "Could not send message yet.";
    }
});

moodForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    moodStatus.textContent = "Saving check-in...";

    const payload = {
        username: document.getElementById("username").value,
        session_id: currentSessionId,
        mood: document.getElementById("mood").value,
        notes: document.getElementById("mood-notes").value,
        stress_level: document.getElementById("stress-level").value,
    };

    try {
        await postJson("/api/chat/mood-checkins/", payload);
        moodStatus.textContent = "Mood check-in saved.";
        moodForm.reset();
        document.getElementById("stress-level").value = "3";
    } catch (error) {
        moodStatus.textContent = error.message || "Could not save the mood check-in yet.";
    }
});

sessionList.addEventListener("click", async (event) => {
    const button = event.target.closest(".session-item");
    if (!button) {
        return;
    }

    const sessionId = Number(button.dataset.sessionId);
    const username = document.getElementById("username").value.trim();
    if (!sessionId || !username) {
        return;
    }

    const response = await fetch(`/api/chat/sessions/?username=${encodeURIComponent(username)}`);
    const sessions = await response.json();
    const match = sessions.find((session) => session.id === sessionId);
    if (!match) {
        return;
    }

    setSessionSummary(match);
    renderTranscript(match.messages || []);
    renderSessions(sessions);
});

newChatButton.addEventListener("click", () => {
    setSessionSummary(null);
    setSafetySummary(null);
    renderTranscript([]);
    document.getElementById("message").value = "";
    chatStatus.textContent = "New chat ready.";
});

loadSessionsButton.addEventListener("click", loadSessions);
loadResourcesButton.addEventListener("click", loadResources);
loadFlaggedButton.addEventListener("click", loadFlaggedMessages);
showMoodPanelButton.addEventListener("click", () => {
    openDrawer();
    moodPanel.scrollIntoView({ behavior: "smooth", block: "start" });
});

openLoginButton.addEventListener("click", () => openAuthPanel("login"));
openLoginTopButton.addEventListener("click", () => openAuthPanel("login"));
openRegisterButton.addEventListener("click", () => openAuthPanel("register"));
closeAuthModalButton.addEventListener("click", closeAuthPanel);
closeDrawerButton.addEventListener("click", closeDrawer);
logoutButton.addEventListener("click", async () => {
    try {
        await postJson("/api/users/logout/");
    } finally {
        setActiveUser(null);
        setSessionSummary(null);
        setSafetySummary(null);
        renderSessions([]);
        renderTranscript([]);
        responseCard.classList.add("hidden");
        flaggedList.className = "flagged-list empty-state";
        flaggedList.textContent = "Support staff can load flagged conversations here after login.";
        closeAuthPanel();
    }
});

authModal.addEventListener("click", (event) => {
    if (event.target === authModal) {
        closeAuthPanel();
    }
});

utilityDrawer.addEventListener("click", (event) => {
    if (event.target === utilityDrawer) {
        closeDrawer();
    }
});

setActiveUser(null);
setSessionSummary(null);
setSafetySummary(null);
toggleChatEmpty(true);
loadCurrentUser();
