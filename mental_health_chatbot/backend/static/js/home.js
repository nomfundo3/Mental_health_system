const chatForm = document.getElementById("chat-form");
const moodForm = document.getElementById("mood-form");
const resourcesButton = document.getElementById("load-resources");

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

    if (!response.ok) {
        throw new Error(`Request failed with status ${response.status}`);
    }

    return response.json();
}

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
