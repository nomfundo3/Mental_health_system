const registerForm = document.getElementById("register-form");
const loginForm = document.getElementById("login-form");
const chatForm = document.getElementById("chat-form");
const moodForm = document.getElementById("mood-form");
const resourcesButton = document.getElementById("load-resources");

const registerStatus = document.getElementById("register-status");
const registerSuccessCard = document.getElementById("register-success");
const registerSuccessMessage = document.getElementById("register-success-message");
const loginStatus = document.getElementById("login-status");
const loginSuccessCard = document.getElementById("login-success");
const loginSuccessMessage = document.getElementById("login-success-message");
const chatStatus = document.getElementById("chat-status");
const moodStatus = document.getElementById("mood-status");
const resourcesStatus = document.getElementById("resources-status");
const resourcesList = document.getElementById("resources-list");
const responseCard = document.getElementById("chat-response");
const assistantMessage = document.getElementById("assistant-message");
const sentiment = document.getElementById("sentiment");
const riskLevel = document.getElementById("risk-level");

async function postJson(url, payload) {
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

registerForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    registerStatus.textContent = "Creating account...";
    registerSuccessCard.classList.add("hidden");

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
        preferred_language: document.getElementById("register-language").value,
        password,
        confirm_password: confirmPassword,
        consent_accepted: document.getElementById("register-consent").checked,
    };

    try {
        const data = await postJson("/api/users/register/", payload);
        registerStatus.textContent = "Registration successful.";
        registerSuccessMessage.textContent = `${data.user.username} is ready to start using the system.`;
        registerSuccessCard.classList.remove("hidden");
        document.getElementById("username").value = data.user.username;
        registerForm.reset();
    } catch (error) {
        registerStatus.textContent = error.message || "Could not create the account yet.";
    }
});

loginForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    loginStatus.textContent = "Signing you in...";
    loginSuccessCard.classList.add("hidden");

    const payload = {
        username: document.getElementById("login-username").value.trim(),
        password: document.getElementById("login-password").value,
    };

    try {
        const data = await postJson("/api/users/login/", payload);
        loginStatus.textContent = "Login successful.";
        loginSuccessMessage.textContent = `Welcome back, ${data.user.display_name || data.user.username}.`;
        loginSuccessCard.classList.remove("hidden");
        document.getElementById("username").value = data.user.username;
        loginForm.reset();
    } catch (error) {
        loginStatus.textContent = error.message || "Could not log in yet.";
    }
});

chatForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    chatStatus.textContent = "Sending message...";

    const payload = {
        username: document.getElementById("username").value,
        message: document.getElementById("message").value,
    };

    try {
        const data = await postJson("/api/chat/message/", payload);
        const messages = data.session.messages;
        const lastAssistantMessage = [...messages].reverse().find((entry) => entry.role === "assistant");

        assistantMessage.textContent = lastAssistantMessage ? lastAssistantMessage.content : "No response received.";
        sentiment.textContent = data.assessment.sentiment;
        riskLevel.textContent = data.assessment.risk_level;
        responseCard.classList.remove("hidden");
        chatStatus.textContent = "Message sent successfully.";
        chatForm.reset();
    } catch (error) {
        chatStatus.textContent = "Could not send message yet. Please try again.";
    }
});

moodForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    moodStatus.textContent = "Saving check-in...";

    const payload = {
        mood: document.getElementById("mood").value,
        notes: document.getElementById("mood-notes").value,
    };

    try {
        await postJson("/api/chat/mood-checkins/", payload);
        moodStatus.textContent = "Mood check-in saved.";
        moodForm.reset();
    } catch (error) {
        moodStatus.textContent = "Could not save the mood check-in yet.";
    }
});

resourcesButton.addEventListener("click", async () => {
    resourcesStatus.textContent = "Loading resources...";
    resourcesList.innerHTML = "";

    try {
        const response = await fetch("/api/recommendations/");
        if (!response.ok) {
            throw new Error(`Request failed with status ${response.status}`);
        }

        const resources = await response.json();
        resourcesStatus.textContent = resources.length ? "" : "No resources have been added yet.";

        resources.forEach((resource) => {
            const card = document.createElement("article");
            card.className = "resource-item";
            card.innerHTML = `
                <h3>${resource.title}</h3>
                <p>${resource.description}</p>
                <p><strong>Category:</strong> ${resource.category}</p>
                ${resource.url ? `<a href="${resource.url}" target="_blank" rel="noreferrer">Open resource</a>` : ""}
            `;
            resourcesList.appendChild(card);
        });
    } catch (error) {
        resourcesStatus.textContent = "Could not load resources yet.";
    }
});
