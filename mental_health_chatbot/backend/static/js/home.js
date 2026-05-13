const registerForm = document.getElementById("register-form");
const loginForm = document.getElementById("login-form");
const chatForm = document.getElementById("chat-form");
const moodForm = document.getElementById("mood-form");

const registerStatus = document.getElementById("register-status");
const loginStatus = document.getElementById("login-status");
const chatStatus = document.getElementById("chat-status");
const moodStatus = document.getElementById("mood-status");
const resourcesStatus = document.getElementById("resources-status");
const settingsStatus = document.getElementById("settings-status");
const profileStatus = document.getElementById("profile-status");
const historyStatus = document.getElementById("history-status");
const searchStatus = document.getElementById("search-status");

const resourcesList = document.getElementById("resources-list");
const historySessionList = document.getElementById("history-session-list");
const searchSessionList = document.getElementById("search-session-list");
const sessionSearchInput = document.getElementById("session-search");
const chatTranscript = document.getElementById("chat-transcript");
const heroEmpty = document.getElementById("hero-empty");
const flaggedList = document.getElementById("flagged-list");

const activeUser = document.getElementById("active-user");
const activeUserMeta = document.getElementById("active-user-meta");
const activeSessionMeta = document.getElementById("active-session-meta");
const activeSafetyMeta = document.getElementById("active-safety-meta");
const chatTitle = document.getElementById("chat-title");
const topbarUserLabel = document.getElementById("topbar-user-label");
const topbarRoleBadge = document.getElementById("topbar-role-badge");

const factSessionCount = document.getElementById("fact-session-count");
const factSessionCountDrawer = document.getElementById("fact-session-count-drawer");
const factResourceCount = document.getElementById("fact-resource-count");
const factFlaggedCount = document.getElementById("fact-flagged-count");
const flaggedStatCard = document.getElementById("flagged-stat-card");

const stepRegister = document.getElementById("step-register");
const stepLogin = document.getElementById("step-login");
const stepChat = document.getElementById("step-chat");

const newChatButton = document.getElementById("new-chat");
const loadSessionsButton = document.getElementById("load-sessions");
const loadResourcesButton = document.getElementById("load-resources");
const loadFlaggedButton = document.getElementById("load-flagged");
const showMoodPanelButton = document.getElementById("show-mood-panel");
const openSettingsButton = document.getElementById("open-settings");
const openHelpButton = document.getElementById("open-help");
const sidebarHomeButton = document.getElementById("sidebar-home");
const toggleHistoryButton = document.getElementById("toggle-history");

const openLoginButton = document.getElementById("open-login");
const openLoginTopButton = document.getElementById("open-login-top");
const openRegisterButton = document.getElementById("open-register");
const openAdminPanelButton = document.getElementById("open-admin-panel");
const openDashboardButton = document.getElementById("open-dashboard");
const openAuditTrailButton = document.getElementById("open-audit-trail");
const openAccountButton = document.getElementById("open-account");
const accountMenuWrap = document.getElementById("account-menu-wrap");
const accountMenuButton = document.getElementById("account-menu-button");
const accountMenu = document.getElementById("account-menu");
const accountAvatar = document.getElementById("account-avatar");
const accountMenuName = document.getElementById("account-menu-name");
const accountMenuRole = document.getElementById("account-menu-role");
const menuProfileButton = document.getElementById("menu-profile");
const logoutMenuButton = document.getElementById("logout-menu");
const closeAuthModalButton = document.getElementById("close-auth-modal");
const authModal = document.getElementById("auth-modal");
const searchModal = document.getElementById("search-modal");
const closeSearchModalButton = document.getElementById("close-search-modal");
const profileModal = document.getElementById("profile-modal");
const closeProfileModalButton = document.getElementById("close-profile-modal");
const cancelProfileButton = document.getElementById("cancel-profile");
const profileForm = document.getElementById("profile-form");
const profileAvatar = document.getElementById("profile-avatar");
const profileDisplayName = document.getElementById("profile-display-name");
const profileUsername = document.getElementById("profile-username");
const settingsModal = document.getElementById("settings-modal");
const closeSettingsModalButton = document.getElementById("close-settings-modal");
const settingsTabs = Array.from(document.querySelectorAll(".settings-tab"));
const settingsPanes = Array.from(document.querySelectorAll(".settings-pane"));
const settingsModalTitle = document.getElementById("settings-modal-title");
const settingsAccountType = document.getElementById("settings-account-type");
const helpModal = document.getElementById("help-modal");
const closeHelpModalButton = document.getElementById("close-help-modal");
const helpCenterAction = document.getElementById("help-center-action");
const helpResourcesAction = document.getElementById("help-resources-action");
const helpShortcutsAction = document.getElementById("help-shortcuts-action");
const helpDetail = document.getElementById("help-detail");
const loginPanel = document.getElementById("login-panel");
const registerPanel = document.getElementById("register-panel");
const accountSummary = document.getElementById("account-summary");
const logoutButton = document.getElementById("logout-button");
const logoutTopButton = document.getElementById("logout-top");

const guestActions = document.getElementById("guest-actions");
const userActions = document.getElementById("user-actions");
const promoCard = document.getElementById("promo-card");
const promoTitle = document.getElementById("promo-title");
const promoCopy = document.getElementById("promo-copy");
const promoGuestActions = document.getElementById("promo-guest-actions");
const flaggedReviewCard = document.getElementById("flagged-review-card");

const utilityDrawer = document.getElementById("utility-drawer");
const closeDrawerButton = document.getElementById("close-drawer");
const drawerKicker = document.getElementById("drawer-kicker");
const drawerTitle = document.getElementById("drawer-title");
const drawerCopy = document.getElementById("drawer-copy");
const overviewPanel = document.getElementById("overview-panel");
const moodPanel = document.getElementById("mood-panel");
const resourcesPanel = document.getElementById("resources-panel");
const resourceFilterButtons = Array.from(document.querySelectorAll(".resource-filter"));
const textSizeSelect = document.getElementById("text-size-select");
const reduceMotionToggle = document.getElementById("reduce-motion-toggle");
const resetPreferencesButton = document.getElementById("reset-preferences");
const helpStartChatButton = document.getElementById("help-start-chat");
const helpOpenResourcesButton = document.getElementById("help-open-resources");
const messageInput = document.getElementById("message");
const stressLevelInput = document.getElementById("stress-level");
const stressLevelValue = document.getElementById("stress-level-value");

const sidebarButtons = [
    newChatButton,
    loadSessionsButton,
    showMoodPanelButton,
    loadResourcesButton,
    loadFlaggedButton,
    openSettingsButton,
    openHelpButton,
].filter(Boolean);

const preferenceStorageKey = "mental-health-sidebar-preferences";

let currentUser = null;
let currentSessionId = null;
let currentTranscriptMessages = [];
let currentSessions = [];
let currentSearchSessions = [];
let sessionSearchTimeoutId = null;
let guestChatUsage = null;
let isHistoryCollapsed = false;
let currentResourceCategory = "";
const drawerContent = {
    overview: {
        section: overviewPanel,
        button: null,
        kicker: "Overview",
        title: "Student support tools",
        copy: "A quick snapshot of your saved chats, resources, and current support status.",
    },
    mood: {
        section: moodPanel,
        button: showMoodPanelButton,
        kicker: "Mood check-in",
        title: "Save a wellbeing check-in",
        copy: "Capture mood, stress level, and notes for the active support session.",
    },
    resources: {
        section: resourcesPanel,
        button: loadResourcesButton,
        kicker: "Resources",
        title: "Student support resources",
        copy: "Browse crisis, stress, anxiety, and general support guidance.",
    },
    flagged: {
        section: flaggedReviewCard,
        button: loadFlaggedButton,
        kicker: "Flagged review",
        title: "Support review queue",
        copy: "Review high-risk conversations that need human attention.",
    },
};

const fallbackResources = [
    {
        title: "Campus counselling or student wellness office",
        description: "Book a confidential support session through your institution's counselling, wellness, or student affairs office.",
        url: "",
        category: "general",
        is_emergency: false,
    },
    {
        title: "South African Depression and Anxiety Group",
        description: "SADAG offers mental health information, referrals, and helplines for anxiety, depression, trauma, and crisis support.",
        url: "https://www.sadag.org/",
        category: "crisis",
        is_emergency: true,
    },
    {
        title: "Exam stress reset",
        description: "Pause for two minutes, drink water, write the next smallest task, and ask a lecturer, tutor, or classmate for practical help.",
        url: "",
        category: "stress",
        is_emergency: false,
    },
    {
        title: "Grounding for anxiety",
        description: "Try the 5-4-3-2-1 grounding method: name five things you see, four you feel, three you hear, two you smell, and one you taste.",
        url: "",
        category: "anxiety",
        is_emergency: false,
    },
];

function resetSessionSearchResults(message = "Start typing to search your saved chats.") {
    currentSearchSessions = [];
    if (searchSessionList) {
        searchSessionList.className = "session-list modal-session-list empty-state";
        searchSessionList.textContent = currentUser ? message : "Log in to search saved chats.";
    }
    if (searchStatus) {
        searchStatus.textContent = "";
    }
}

function setChatStatus(message = "", isError = false) {
    if (!chatStatus) {
        return;
    }

    chatStatus.textContent = message;
    chatStatus.classList.toggle("hidden", !message);
    chatStatus.classList.toggle("error-text", Boolean(message && isError));
}

function setHistoryStatus(message = "", isError = false) {
    if (!historyStatus) {
        return;
    }

    historyStatus.textContent = message;
    historyStatus.classList.toggle("hidden", !message || isHistoryCollapsed);
    historyStatus.classList.toggle("error-text", Boolean(message && isError));
}

function updateGuestChatStatus() {
    if (currentUser || !guestChatUsage) {
        return;
    }

    const remaining = Number(guestChatUsage.tokens_remaining ?? 0);
    setChatStatus(`Guest mode: about ${remaining} tokens left. Log in to save chats.`, false);
}

function isSupportUser(user = currentUser) {
    return Boolean(user && ["admin", "support"].includes(user.role));
}

function getCookie(name) {
    const cookieString = document.cookie || "";
    const cookies = cookieString.split(";").map((cookie) => cookie.trim());
    const match = cookies.find((cookie) => cookie.startsWith(`${name}=`));
    return match ? decodeURIComponent(match.split("=").slice(1).join("=")) : "";
}

function getCsrfToken() {
    const cookieToken = getCookie("csrftoken");
    if (cookieToken) {
        return cookieToken;
    }

    const metaToken = document.querySelector('meta[name="csrf-token"]')?.getAttribute("content") || "";
    return metaToken === "NOTPROVIDED" ? "" : metaToken;
}

function getFlaggedDefaultMessage(user = currentUser) {
    if (!user) {
        return "Support staff can load flagged conversations here after login.";
    }

    if (isSupportUser(user)) {
        return "Flagged conversations will appear here after you load them.";
    }

    return "Flagged review is only available to support staff.";
}

function setStepState(step, state) {
    if (!step) {
        return;
    }

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

function setActiveSidebarButton(activeButton) {
    sidebarButtons.forEach((button) => {
        button.classList.toggle("active-nav", button === activeButton);
    });
}

function shouldReduceMotion() {
    return Boolean(reduceMotionToggle?.checked);
}

function openAuthPanel(mode) {
    if (!authModal || !loginPanel || !registerPanel || !accountSummary) {
        return;
    }

    const resolvedMode = currentUser && mode === "account" ? "account" : mode;
    authModal.classList.remove("hidden");
    loginPanel.classList.toggle("hidden", resolvedMode !== "login");
    registerPanel.classList.toggle("hidden", resolvedMode !== "register");
    accountSummary.classList.toggle("hidden", resolvedMode !== "account");
}

function closeAuthPanel() {
    authModal?.classList.add("hidden");
}

function openSearchModal() {
    if (!searchModal) {
        return;
    }

    searchModal.classList.remove("hidden");
    resetSessionSearchResults();
    requestAnimationFrame(() => {
        sessionSearchInput?.focus();
        sessionSearchInput?.select();
    });
}

function closeSearchModal() {
    searchModal?.classList.add("hidden");
}

function closeAccountMenu() {
    accountMenu?.classList.add("hidden");
    accountMenuButton?.setAttribute("aria-expanded", "false");
}

function toggleAccountMenu() {
    if (!accountMenu || !accountMenuButton) {
        return;
    }
    const willOpen = accountMenu.classList.contains("hidden");
    accountMenu.classList.toggle("hidden", !willOpen);
    accountMenuButton.setAttribute("aria-expanded", String(willOpen));
}

function openProfileModal() {
    if (!currentUser || !profileModal) {
        openAuthPanel("login");
        return;
    }
    closeAccountMenu();
    profileDisplayName.value = currentUser.display_name || "";
    profileUsername.value = currentUser.username || "";
    if (profileStatus) {
        profileStatus.textContent = "";
    }
    profileModal.classList.remove("hidden");
}

function closeProfileModal() {
    profileModal?.classList.add("hidden");
}

function openSettingsModal(activeTab = "general") {
    closeAccountMenu();
    settingsModal?.classList.remove("hidden");
    showSettingsTab(activeTab);
}

function closeSettingsModal() {
    settingsModal?.classList.add("hidden");
}

function showSettingsTab(tabName = "general") {
    settingsTabs.forEach((tab) => {
        tab.classList.toggle("active", tab.dataset.settingsTab === tabName);
    });
    settingsPanes.forEach((pane) => {
        pane.classList.toggle("hidden", pane.dataset.settingsPane !== tabName);
    });
    if (settingsModalTitle) {
        settingsModalTitle.textContent = tabName.charAt(0).toUpperCase() + tabName.slice(1);
    }
}

function openHelpModal(detail = "") {
    closeAccountMenu();
    if (helpDetail && detail) {
        helpDetail.textContent = detail;
    }
    helpModal?.classList.remove("hidden");
}

function closeHelpModal() {
    helpModal?.classList.add("hidden");
}

function openDrawer() {
    utilityDrawer?.classList.remove("hidden");
}

function closeDrawer() {
    utilityDrawer?.classList.add("hidden");
}

function openDrawerSection(viewKey = "overview") {
    const content = drawerContent[viewKey] || drawerContent.overview;
    openDrawer();

    Object.values(drawerContent).forEach((item) => {
        item.section?.classList.toggle("hidden", item.section !== content.section);
    });

    if (drawerKicker) {
        drawerKicker.textContent = content.kicker;
    }
    if (drawerTitle) {
        drawerTitle.textContent = content.title;
    }
    if (drawerCopy) {
        drawerCopy.textContent = content.copy;
    }
    if (content.button) {
        setActiveSidebarButton(content.button);
    }

    utilityDrawer?.setAttribute("data-view", viewKey);
}

function toggleChatEmpty(isEmpty) {
    heroEmpty?.classList.toggle("hidden", !isEmpty);
    chatTranscript?.classList.toggle("hidden", isEmpty);
}

function getUserInitials(user) {
    const label = (user?.display_name || user?.username || "Mental Health").trim();
    const words = label.split(/\s+/).filter(Boolean);
    if (words.length >= 2) {
        return `${words[0][0]}${words[1][0]}`.toUpperCase();
    }
    return label.slice(0, 2).toUpperCase();
}

function updateAuthChrome(user) {
    const isAuthenticated = Boolean(user);
    const accountName = user ? user.display_name || user.username : "Guest";
    const initials = getUserInitials(user);

    guestActions?.classList.toggle("hidden", isAuthenticated);
    userActions?.classList.toggle("hidden", !isAuthenticated);
    promoCard?.classList.toggle("hidden", isAuthenticated);
    accountMenuWrap?.classList.toggle("hidden", !isAuthenticated);
    promoGuestActions?.classList.toggle("hidden", isAuthenticated);
    openAdminPanelButton?.classList.toggle("hidden", !isSupportUser(user));

    if (topbarRoleBadge) {
        if (user && user.role) {
            topbarRoleBadge.textContent = user.role.charAt(0).toUpperCase() + user.role.slice(1);
            topbarRoleBadge.classList.remove("hidden");
        } else {
            topbarRoleBadge.classList.add("hidden");
        }
    }

    if (topbarUserLabel) {
        topbarUserLabel.textContent = accountName;
    }
    if (accountAvatar) {
        accountAvatar.textContent = initials;
    }
    if (profileAvatar) {
        profileAvatar.textContent = initials;
    }
    if (accountMenuName) {
        accountMenuName.textContent = accountName;
    }
    if (accountMenuRole) {
        accountMenuRole.textContent = user?.role ? user.role : "Student";
    }
    if (settingsAccountType) {
        settingsAccountType.textContent = user?.role ? user.role : "Student";
    }
    if (promoTitle) {
        promoTitle.textContent = isAuthenticated ? `Welcome, ${accountName}` : "Get support tailored to you";
    }
    if (promoCopy) {
        promoCopy.textContent = isAuthenticated
            ? "Your saved chats, mood check-ins, and support resources are ready when you are."
            : "You can start chatting right away as a guest, or log in to save chats, mood check-ins, and support resources.";
    }
}

function updateSupportChrome(user) {
    const canReviewFlagged = isSupportUser(user);

    loadFlaggedButton?.classList.toggle("hidden", !canReviewFlagged);
    openDashboardButton?.classList.toggle("hidden", !canReviewFlagged);
    openAuditTrailButton?.classList.toggle("hidden", !canReviewFlagged);
    flaggedReviewCard?.classList.toggle("hidden", !canReviewFlagged);
    flaggedStatCard?.classList.toggle("hidden", !canReviewFlagged);

    if (!canReviewFlagged && factFlaggedCount) {
        factFlaggedCount.textContent = "0";
    }

    if (flaggedList) {
        flaggedList.className = "flagged-list empty-state";
        flaggedList.textContent = getFlaggedDefaultMessage(user);
    }
}

function setActiveUser(user) {
    currentUser = user;

    const usernameInput = document.getElementById("username");
    if (usernameInput) {
        usernameInput.value = user ? user.username : "";
    }

    if (activeUser) {
        activeUser.textContent = user ? user.display_name || user.username : "Guest";
    }
    if (activeUserMeta) {
        activeUserMeta.textContent = user
            ? `${user.username} is signed in and ready to continue.`
            : "You can start chatting now, or log in to save your progress.";
    }
    if (chatTitle) {
        chatTitle.textContent = user
            ? `Welcome back, ${user.display_name || user.username}`
            : "What's on your mind today?";
    }

    updateAuthChrome(user);
    updateSupportChrome(user);
    updateOrderedFlow();

    if (user) {
        setChatStatus("");
    } else {
        updateGuestChatStatus();
    }
}

function setSessionSummary(session) {
    const messages = Array.isArray(session?.messages) ? session.messages : [];
    currentSessionId = session ? session.id : null;

    if (activeSessionMeta) {
        activeSessionMeta.textContent = session
            ? `${session.status} conversation with ${messages.length} saved messages.`
            : "A calmer, structured assistant for student wellbeing.";
    }

    updateOrderedFlow();
}

function setSafetySummary(assessment) {
    const categories = Array.isArray(assessment?.resource_categories)
        ? assessment.resource_categories
        : [];

    if (activeSafetyMeta) {
        activeSafetyMeta.textContent = assessment
            ? `Sentiment: ${assessment.sentiment}. Categories: ${categories.join(", ")}.`
            : "Risk detection updates after each message.";
    }
}

function escapeHtml(value = "") {
    return String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#39;");
}

function scrollTranscriptToBottom() {
    if (!chatTranscript || chatTranscript.classList.contains("hidden")) {
        return;
    }

    chatTranscript.scrollTop = chatTranscript.scrollHeight;
}

function renderTranscript(messages = []) {
    const safeMessages = Array.isArray(messages) ? messages : [];
    currentTranscriptMessages = safeMessages;

    if (!safeMessages.length) {
        chatTranscript.innerHTML = "";
        toggleChatEmpty(true);
        return;
    }

    toggleChatEmpty(false);

    chatTranscript.innerHTML = safeMessages.map((entry) => {
        const source = entry.source ? entry.source.replace("_", " ") : "system";
        const content = escapeHtml(entry.content || "").replace(/\n/g, "<br>");
        const isGenerating = Boolean(entry.isGenerating);
        const bodyMarkup = isGenerating
            ? `
                <div class="message-streaming" aria-live="polite">
                    <div class="typing-indicator" aria-hidden="true">
                        <span></span>
                        <span></span>
                        <span></span>
                    </div>
                    <span class="message-streaming-label">Generating a response...</span>
                </div>
            `
            : `<p>${content}</p>`;

        return `
            <article class="message-row ${entry.role} ${isGenerating ? "generating" : ""}">
                <div class="avatar">${entry.role === "assistant" ? "S" : "Y"}</div>
                <div class="message-body">
                    <p class="message-role">${entry.role === "assistant" ? "Mental Health Assistant" : "You"}</p>
                    ${bodyMarkup}
                    <span class="message-meta">${entry.risk_level} risk | ${source}</span>
                </div>
            </article>
        `;
    }).join("");

    scrollTranscriptToBottom();
}

function buildSessionMarkup(sessions = []) {
    return sessions.map((session) => `
        <button type="button" data-session-id="${session.id}" class="session-item ${Number(session.id) === currentSessionId ? "active" : ""}">
            <strong>${escapeHtml(session.title || "Support chat")}</strong>
            <span>${escapeHtml(session.last_risk_level || "low")} risk</span>
        </button>
    `).join("");
}

function getSessionTimestamp(session) {
    const value = session?.updated_at || session?.last_message_at || session?.created_at;
    const timestamp = Date.parse(value);
    return Number.isNaN(timestamp) ? 0 : timestamp;
}

function sortRecentSessions(sessions = []) {
    return [...sessions].sort((first, second) => getSessionTimestamp(second) - getSessionTimestamp(first));
}

function setHistoryCollapsed(isCollapsed) {
    isHistoryCollapsed = isCollapsed;
    toggleHistoryButton?.setAttribute("aria-expanded", String(!isCollapsed));
    toggleHistoryButton?.classList.toggle("collapsed", isCollapsed);
    historySessionList?.classList.toggle("hidden", isCollapsed);
    historyStatus?.classList.toggle("hidden", isCollapsed || !historyStatus.textContent);
}

function renderHistorySessions(sessions = []) {
    const safeSessions = sortRecentSessions(Array.isArray(sessions) ? sessions : []);
    currentSessions = safeSessions;

    if (factSessionCount) {
        factSessionCount.textContent = safeSessions.length;
    }
    if (factSessionCountDrawer) {
        factSessionCountDrawer.textContent = safeSessions.length;
    }

    if (!safeSessions.length) {
        if (!currentUser) {
            historySessionList.className = "session-list history-session-list empty-state";
            historySessionList.textContent = "Log in to browse saved chats.";
        } else {
            historySessionList.className = "session-list history-session-list empty-state";
            historySessionList.textContent = "No saved chats yet. Start a conversation and it will appear here.";
        }
        setHistoryCollapsed(isHistoryCollapsed);
        return;
    }

    historySessionList.className = "session-list history-session-list";
    historySessionList.innerHTML = buildSessionMarkup(safeSessions);
    setHistoryCollapsed(isHistoryCollapsed);
}

function renderSearchSessions(sessions = []) {
    const safeSessions = Array.isArray(sessions) ? sessions : [];
    const searchTerm = sessionSearchInput?.value.trim() || "";
    currentSearchSessions = safeSessions;

    if (!safeSessions.length) {
        searchSessionList.className = "session-list modal-session-list empty-state";
        if (!currentUser) {
            searchSessionList.textContent = "Log in to search saved chats.";
        } else if (!searchTerm) {
            searchSessionList.textContent = "Start typing to search your saved chats.";
        } else {
            searchSessionList.textContent = `No chats found for "${searchTerm}".`;
        }
        return;
    }

    searchSessionList.className = "session-list modal-session-list";
    searchSessionList.innerHTML = buildSessionMarkup(safeSessions);
}

async function loadHistorySessions() {
    if (!currentUser) {
        setHistoryStatus("");
        renderHistorySessions([]);
        return;
    }

    setHistoryStatus("Loading chats...");

    try {
        const response = await fetch("/api/chat/sessions/", {
            credentials: "same-origin",
        });

        if (!response.ok) {
            throw new Error(`Request failed with status ${response.status}`);
        }

        const sessions = await response.json();
        setHistoryStatus("");
        renderHistorySessions(sessions);
    } catch (error) {
        console.error("Load history error:", error);
        setHistoryStatus("Could not load chats yet.", true);
    }
}

function renderResources(resources = []) {
    const safeResources = Array.isArray(resources) ? resources : [];

    if (factResourceCount) {
        factResourceCount.textContent = safeResources.length;
    }
    resourcesList.innerHTML = "";

    if (!safeResources.length) {
        resourcesList.className = "resource-list empty-state";
        resourcesList.textContent = "No resources found for this category.";
        return;
    }

    resourcesList.className = "resource-list";
    safeResources.forEach((resource) => {
        const card = document.createElement("article");
        card.className = `resource-item ${resource.is_emergency ? "emergency" : ""}`;
        card.innerHTML = `
            <p class="resource-tag">${escapeHtml(resource.category || "general")}</p>
            <h3>${escapeHtml(resource.title || "Support resource")}</h3>
            <p>${escapeHtml(resource.description || "")}</p>
            ${resource.url ? `<a href="${resource.url}" target="_blank" rel="noreferrer">Open resource</a>` : ""}
        `;
        resourcesList.appendChild(card);
    });
}

function renderFlagged(flagged = []) {
    const safeFlagged = Array.isArray(flagged) ? flagged : [];

    if (factFlaggedCount) {
        factFlaggedCount.textContent = safeFlagged.length;
    }

    if (!safeFlagged.length) {
        flaggedList.className = "flagged-list empty-state";
        flaggedList.textContent = "No flagged conversations were returned.";
        return;
    }

    flaggedList.className = "flagged-list";
    flaggedList.innerHTML = safeFlagged.map((item) => `
        <article class="flagged-item">
            <h3>Session #${item.session_id}</h3>
            <p>${escapeHtml(item.content || "")}</p>
            <span>${escapeHtml(item.risk_level || "low")} risk | ${escapeHtml(item.sentiment || "neutral")} sentiment</span>
        </article>
    `).join("");
}

async function postJson(url, payload = {}) {
    return sendJson(url, payload, "POST");
}

async function patchJson(url, payload = {}) {
    return sendJson(url, payload, "PATCH");
}

async function sendJson(url, payload = {}, method = "POST") {
    const csrfToken = getCsrfToken();
    const response = await fetch(url, {
        method,
        headers: {
            "Content-Type": "application/json",
            ...(csrfToken ? { "X-CSRFToken": csrfToken } : {}),
        },
        credentials: "same-origin",
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
        const response = await fetch("/api/users/me/", {
            credentials: "same-origin",
        });

        if (!response.ok) {
            return;
        }

        const payload = await response.json();
        guestChatUsage = payload.guest_chat || null;
        if (payload.authenticated && payload.user) {
            setActiveUser(payload.user);
            await loadHistorySessions();
            return;
        }

        setActiveUser(null);
    } catch (error) {
        console.error("Could not load current user:", error);
    }
}

async function loadSessions() {
    const searchTerm = sessionSearchInput?.value.trim() || "";

    if (!currentUser) {
        resetSessionSearchResults("Log in to search saved chats.");
        if (searchStatus) {
            searchStatus.textContent = "Log in to search saved chats.";
        }
        renderSearchSessions([]);
        return;
    }

    if (!searchTerm) {
        resetSessionSearchResults();
        return;
    }

    if (searchStatus) {
        searchStatus.textContent = "Searching chats...";
    }

    try {
        const query = new URLSearchParams();
        query.set("search", searchTerm);

        const response = await fetch(`/api/chat/sessions/?${query.toString()}`, {
            credentials: "same-origin",
        });

        if (!response.ok) {
            throw new Error(`Request failed with status ${response.status}`);
        }

        const sessions = await response.json();
        if (searchStatus) {
            searchStatus.textContent = sessions.length ? "" : `No chats found for "${searchTerm}".`;
        }
        renderSearchSessions(sessions);
    } catch (error) {
        console.error("Load sessions error:", error);
        if (searchStatus) {
            searchStatus.textContent = "Could not search chats yet.";
        }
    }
}

async function loadResources(category = currentResourceCategory) {
    currentResourceCategory = category || "";
    resourceFilterButtons.forEach((button) => {
        button.classList.toggle("active", button.dataset.category === currentResourceCategory);
    });
    resourcesStatus.textContent = "Loading resources...";

    try {
        const query = new URLSearchParams();
        if (currentResourceCategory) {
            query.set("category", currentResourceCategory);
        }
        const url = query.toString() ? `/api/recommendations/?${query.toString()}` : "/api/recommendations/";
        const response = await fetch(url, {
            credentials: "same-origin",
        });

        if (!response.ok) {
            throw new Error(`Request failed with status ${response.status}`);
        }

        let resources = await response.json();
        if (!resources.length) {
            resources = fallbackResources.filter((resource) => (
                !currentResourceCategory || resource.category === currentResourceCategory
            ));
            resourcesStatus.textContent = resources.length
                ? "Showing built-in demo resources. Seed the database to manage this list."
                : "No resources found for this category.";
        } else {
            resourcesStatus.textContent = "";
        }
        renderResources(resources);
    } catch (error) {
        console.error("Load resources error:", error);
        const resources = fallbackResources.filter((resource) => (
            !currentResourceCategory || resource.category === currentResourceCategory
        ));
        resourcesStatus.textContent = "Could not reach the resource API, so built-in demo resources are shown.";
        renderResources(resources);
    }
}

async function loadFlaggedMessages() {
    if (!isSupportUser()) {
        flaggedList.className = "flagged-list empty-state";
        flaggedList.textContent = getFlaggedDefaultMessage();
        return;
    }

    flaggedList.className = "flagged-list empty-state";
    flaggedList.textContent = "Loading flagged cases...";

    try {
        const response = await fetch("/api/admin-panel/flagged-messages/", {
            credentials: "same-origin",
        });

        if (!response.ok) {
            throw new Error(`Request failed with status ${response.status}`);
        }

        const payload = await response.json();
        renderFlagged(payload.flagged_messages || []);
    } catch (error) {
        console.error("Load flagged error:", error);
        flaggedList.textContent = "Support login is required to view flagged cases.";
    }
}

function showMoodSection() {
    openDrawerSection("mood");
    if (!currentUser) {
        moodStatus.textContent = "Log in to save a mood check-in.";
    } else if (moodStatus) {
        moodStatus.textContent = currentSessionId
            ? "This check-in will attach to the current chat."
            : "This check-in will save to your account.";
    }
}

async function showSessionHistory() {
    setActiveSidebarButton(loadSessionsButton);
    openSearchModal();
}

async function showResourcesSection() {
    openDrawerSection("resources");
    await loadResources();
}

async function showFlaggedSection() {
    openDrawerSection("flagged");
    await loadFlaggedMessages();
}

function showSettingsSection() {
    openSettingsModal("general");
    if (settingsStatus) {
        settingsStatus.textContent = "";
    }
}

function showHelpSection() {
    openHelpModal();
}

function getDefaultPreferences() {
    return {
        textSize: "comfortable",
        reduceMotion: false,
    };
}

function loadStoredPreferences() {
    try {
        const raw = localStorage.getItem(preferenceStorageKey);
        return raw ? { ...getDefaultPreferences(), ...JSON.parse(raw) } : getDefaultPreferences();
    } catch (error) {
        return getDefaultPreferences();
    }
}

function saveStoredPreferences(preferences) {
    localStorage.setItem(preferenceStorageKey, JSON.stringify(preferences));
}

function applyPreferences(preferences, statusMessage = "") {
    const fontSizeMap = {
        compact: "15px",
        comfortable: "16px",
        large: "18px",
    };

    document.body.dataset.textSize = preferences.textSize;
    document.documentElement.style.fontSize = fontSizeMap[preferences.textSize] || fontSizeMap.comfortable;
    document.body.classList.toggle("reduce-motion", preferences.reduceMotion);

    if (textSizeSelect) {
        textSizeSelect.value = preferences.textSize;
    }
    if (reduceMotionToggle) {
        reduceMotionToggle.checked = preferences.reduceMotion;
    }
    if (settingsStatus) {
        settingsStatus.textContent = statusMessage;
    }
}

function savePreferences(statusMessage = "Preferences saved.") {
    const preferences = {
        textSize: textSizeSelect?.value || "comfortable",
        reduceMotion: Boolean(reduceMotionToggle?.checked),
    };
    saveStoredPreferences(preferences);
    applyPreferences(preferences, statusMessage);
}

function resetWorkspace(statusMessage = "") {
    setSessionSummary(null);
    setSafetySummary(null);
    renderTranscript([]);
    const messageInput = document.getElementById("message");
    if (messageInput) {
        messageInput.value = "";
    }
    setChatStatus(statusMessage);
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
        console.error("Register error:", error);
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
        guestChatUsage = null;
        setActiveUser(data.user);
        closeAuthPanel();
        await loadHistorySessions();
    } catch (error) {
        console.error("Login error:", error);
        loginStatus.textContent = error.message || "Could not log in yet.";
    }
});

chatForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const messageText = messageInput.value.trim();

    if (!messageText) {
        setChatStatus("Type a message first.", true);
        return;
    }

    const payload = { message: messageText };
    if (currentSessionId) {
        payload.session_id = currentSessionId;
    }

    const baseTranscriptMessages = [...currentTranscriptMessages];

    try {
        setChatStatus("");
        const optimisticMessages = [
            ...baseTranscriptMessages,
            {
                role: "user",
                content: payload.message,
                risk_level: "pending",
                source: "user",
            },
            {
                role: "assistant",
                content: "",
                risk_level: "generating",
                source: "ai_service",
                isGenerating: true,
            },
        ];

        renderTranscript(optimisticMessages);
        messageInput.value = "";

        const response = await fetch("/api/chat/message/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCsrfToken(),
            },
            credentials: "same-origin",
            body: JSON.stringify(payload),
        });

        if (!response.ok) {
            const errorPayload = await response.json().catch(() => ({}));
            if (errorPayload.guest_chat) {
                guestChatUsage = errorPayload.guest_chat;
            }
            throw new Error(errorPayload.detail || `Request failed with status ${response.status}`);
        }
        if (!response.body) {
            throw new Error("Streaming is not available because the response body is missing.");
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = "";
        let finalData = null;
        let streamedAssistantContent = "";

        while (true) {
            const { done, value } = await reader.read();

            if (value) {
                buffer += decoder.decode(value, { stream: true });
            }

            const lines = buffer.split("\n");
            buffer = lines.pop() || "";

            for (const line of lines) {
                const cleanLine = line.trim();
                if (!cleanLine) {
                    continue;
                }

                try {
                    const chunk = JSON.parse(cleanLine);

                    if (chunk.type === "content") {
                        streamedAssistantContent += chunk.data;
                        optimisticMessages[optimisticMessages.length - 1].content = streamedAssistantContent;
                        optimisticMessages[optimisticMessages.length - 1].risk_level = "streaming";
                        optimisticMessages[optimisticMessages.length - 1].isGenerating = false;
                        renderTranscript(optimisticMessages);
                    }

                    if (chunk.type === "complete") {
                        finalData = chunk;
                    }
                } catch (error) {
                    console.error("Could not parse stream chunk:", error, cleanLine);
                }
            }

            if (done) {
                break;
            }
        }

        if (buffer.trim()) {
            try {
                const chunk = JSON.parse(buffer.trim());
                if (chunk.type === "complete") {
                    finalData = chunk;
                }
            } catch (error) {
                console.error("Could not parse final stream chunk:", error, buffer);
            }
        }

        if (!finalData || !finalData.session) {
            throw new Error("Response received but final session data is missing.");
        }

        setSessionSummary(finalData.session);
        setSafetySummary(finalData.assessment);
        guestChatUsage = finalData.guest_chat || guestChatUsage;
        renderTranscript(Array.isArray(finalData.session.messages) ? finalData.session.messages : []);
        renderResources(finalData.resources || []);
        if (!currentUser && guestChatUsage) {
            updateGuestChatStatus();
        } else if (finalData.response_source && finalData.response_source !== "ai_service") {
            setChatStatus("Fallback support guidance was used for this reply.", false);
        } else {
            setChatStatus("");
        }

        if (currentUser) {
            await loadHistorySessions();
        }
    } catch (error) {
        console.error("Chat error:", error);
        setChatStatus(error.message || "Could not send message yet.", true);
        messageInput.value = payload.message;
        renderTranscript(baseTranscriptMessages);
    }
});

messageInput?.addEventListener("keydown", (event) => {
    if (event.key !== "Enter" || event.shiftKey) {
        return;
    }

    event.preventDefault();
    chatForm?.requestSubmit();
});

moodForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    moodStatus.textContent = "Saving check-in...";

    if (!currentUser) {
        moodStatus.textContent = "Please log in before saving a mood check-in.";
        openAuthPanel("login");
        return;
    }

    const payload = {
        mood: document.getElementById("mood").value,
        notes: document.getElementById("mood-notes").value,
        stress_level: Number(document.getElementById("stress-level").value),
    };

    if (currentSessionId) {
        payload.session_id = currentSessionId;
    }

    try {
        await postJson("/api/chat/mood-checkins/", payload);
        moodStatus.textContent = currentSessionId
            ? "Mood check-in saved to this chat session."
            : "Mood check-in saved to your account.";
        moodForm.reset();
        document.getElementById("stress-level").value = "3";
        if (stressLevelValue) {
            stressLevelValue.textContent = "3";
        }
    } catch (error) {
        console.error("Mood check-in error:", error);
        moodStatus.textContent = error.message || "Could not save the mood check-in yet.";
    }
});

function updateSessionCollections(session) {
    if (!session) {
        return;
    }

    const mergeSession = (sessions) => {
        const withoutSession = sessions.filter((item) => Number(item.id) !== Number(session.id));
        return sortRecentSessions([session, ...withoutSession]);
    };

    const updatedHistorySessions = mergeSession(currentSessions);
    const updatedSearchSessions = currentSearchSessions.length ? mergeSession(currentSearchSessions) : [];
    renderHistorySessions(updatedHistorySessions);
    renderSearchSessions(updatedSearchSessions);
}

function handleSessionListClick(listElement, shouldCloseSearch = false) {
    listElement?.addEventListener("click", async (event) => {
        const button = event.target.closest(".session-item");
        if (!button || !currentUser) {
            return;
        }

        const sessionId = Number(button.dataset.sessionId);
        if (!sessionId) {
            return;
        }

        try {
            if (shouldCloseSearch) {
                if (searchStatus) {
                    searchStatus.textContent = "Opening saved chat...";
                }
            } else if (historyStatus) {
                setHistoryStatus("Opening saved chat...");
            }

            const response = await fetch(`/api/chat/sessions/${sessionId}/`, {
                credentials: "same-origin",
            });

            if (!response.ok) {
                throw new Error(`Request failed with status ${response.status}`);
            }

            const session = await response.json();
            if (shouldCloseSearch) {
                if (searchStatus) {
                    searchStatus.textContent = "";
                }
            } else if (historyStatus) {
                setHistoryStatus("");
            }
            setSessionSummary(session);
            renderTranscript(Array.isArray(session.messages) ? session.messages : []);
            updateSessionCollections(session);
            setActiveSidebarButton(loadSessionsButton);
            if (shouldCloseSearch) {
                closeSearchModal();
            }
        } catch (error) {
            console.error("Open session error:", error);
            const message = error.message || "Could not open that saved chat yet.";
            if (shouldCloseSearch) {
                if (searchStatus) {
                    searchStatus.textContent = message;
                }
            } else if (historyStatus) {
                setHistoryStatus(message, true);
            }
        }
    });
}

handleSessionListClick(historySessionList, false);
handleSessionListClick(searchSessionList, true);
toggleHistoryButton?.addEventListener("click", () => {
    setHistoryCollapsed(!isHistoryCollapsed);
});

function handleNewChat(statusMessage = "New chat ready.") {
    closeDrawer();
    setActiveSidebarButton(newChatButton);
    if (sessionSearchInput) {
        sessionSearchInput.value = "";
    }
    resetSessionSearchResults();
    resetWorkspace(statusMessage);
}

newChatButton.addEventListener("click", () => handleNewChat("New chat ready."));
sidebarHomeButton?.addEventListener("click", () => handleNewChat(""));

loadSessionsButton.addEventListener("click", showSessionHistory);
sessionSearchInput?.addEventListener("input", () => {
    if (sessionSearchTimeoutId) {
        clearTimeout(sessionSearchTimeoutId);
    }

    sessionSearchTimeoutId = window.setTimeout(() => {
        loadSessions();
    }, 250);
});
sessionSearchInput?.addEventListener("search", () => {
    if (sessionSearchTimeoutId) {
        clearTimeout(sessionSearchTimeoutId);
    }
    loadSessions();
});
loadResourcesButton.addEventListener("click", showResourcesSection);
loadFlaggedButton.addEventListener("click", showFlaggedSection);
showMoodPanelButton.addEventListener("click", showMoodSection);
openSettingsButton.addEventListener("click", showSettingsSection);
openHelpButton.addEventListener("click", showHelpSection);

openLoginButton.addEventListener("click", () => openAuthPanel("login"));
openLoginTopButton.addEventListener("click", () => openAuthPanel("login"));
openRegisterButton.addEventListener("click", () => openAuthPanel("register"));
openAdminPanelButton?.addEventListener("click", () => {
    window.location.href = "/admin-support/";
});

openDashboardButton?.addEventListener("click", () => {
    window.location.href = "/admin-support/";
});

openAuditTrailButton?.addEventListener("click", () => {
    window.location.href = "/admin-support/#audit-section";
});
openAccountButton?.addEventListener("click", () => openAuthPanel("account"));
accountMenuButton?.addEventListener("click", toggleAccountMenu);
menuProfileButton?.addEventListener("click", openProfileModal);
closeAuthModalButton.addEventListener("click", closeAuthPanel);
closeSearchModalButton?.addEventListener("click", closeSearchModal);
closeProfileModalButton?.addEventListener("click", closeProfileModal);
cancelProfileButton?.addEventListener("click", closeProfileModal);
closeSettingsModalButton?.addEventListener("click", closeSettingsModal);
closeHelpModalButton?.addEventListener("click", closeHelpModal);
closeDrawerButton.addEventListener("click", closeDrawer);

profileForm?.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (!currentUser) {
        openAuthPanel("login");
        return;
    }
    if (profileStatus) {
        profileStatus.textContent = "Saving profile...";
    }
    try {
        const updatedUser = await patchJson("/api/users/profile/", {
            display_name: profileDisplayName.value.trim(),
            username: profileUsername.value.trim(),
        });
        setActiveUser(updatedUser);
        if (profileStatus) {
            profileStatus.textContent = "Profile saved.";
        }
        window.setTimeout(closeProfileModal, 450);
    } catch (error) {
        if (profileStatus) {
            profileStatus.textContent = error.message || "Could not save profile yet.";
        }
    }
});

textSizeSelect?.addEventListener("change", () => savePreferences());
reduceMotionToggle?.addEventListener("change", () => savePreferences());
settingsTabs.forEach((tab) => {
    tab.addEventListener("click", () => showSettingsTab(tab.dataset.settingsTab || "general"));
});
stressLevelInput?.addEventListener("input", () => {
    if (stressLevelValue) {
        stressLevelValue.textContent = stressLevelInput.value;
    }
});
resourceFilterButtons.forEach((button) => {
    button.addEventListener("click", () => {
        loadResources(button.dataset.category || "");
    });
});
resetPreferencesButton?.addEventListener("click", () => {
    const defaults = getDefaultPreferences();
    saveStoredPreferences(defaults);
    applyPreferences(defaults, "Preferences reset.");
});
helpStartChatButton?.addEventListener("click", () => handleNewChat("New chat ready."));
helpOpenResourcesButton?.addEventListener("click", showResourcesSection);
helpResourcesAction?.addEventListener("click", () => {
    closeHelpModal();
    showResourcesSection();
});
helpCenterAction?.addEventListener("click", () => {
    openHelpModal("Use New chat for a fresh conversation, Search chats for saved sessions, Mood check-in for wellbeing tracking, and Resources for support links.");
});
helpShortcutsAction?.addEventListener("click", () => {
    openHelpModal("Demo flow: register or log in, send a message, open Mood check-in, save a check-in, filter Resources, then reload a saved chat from Recent chats.");
});

async function handleLogout() {
    try {
        await postJson("/api/users/logout/");
    } finally {
        setActiveUser(null);
        guestChatUsage = null;
        if (sessionSearchInput) {
            sessionSearchInput.value = "";
        }
        currentSessions = [];
        currentSearchSessions = [];
        resetSessionSearchResults("Log in to search saved chats.");
        renderHistorySessions([]);
        resetWorkspace("You have logged out.");
        setActiveSidebarButton(newChatButton);
        closeAuthPanel();
        closeDrawer();
        closeAccountMenu();
        closeProfileModal();
        closeSettingsModal();
        closeHelpModal();
    }
}

logoutButton?.addEventListener("click", handleLogout);
logoutTopButton?.addEventListener("click", handleLogout);
logoutMenuButton?.addEventListener("click", handleLogout);

authModal?.addEventListener("click", (event) => {
    if (event.target === authModal) {
        closeAuthPanel();
    }
});

searchModal?.addEventListener("click", (event) => {
    if (event.target === searchModal) {
        closeSearchModal();
    }
});

profileModal?.addEventListener("click", (event) => {
    if (event.target === profileModal) {
        closeProfileModal();
    }
});

settingsModal?.addEventListener("click", (event) => {
    if (event.target === settingsModal) {
        closeSettingsModal();
    }
});

helpModal?.addEventListener("click", (event) => {
    if (event.target === helpModal) {
        closeHelpModal();
    }
});

utilityDrawer?.addEventListener("click", (event) => {
    if (event.target === utilityDrawer) {
        closeDrawer();
    }
});

document.addEventListener("click", (event) => {
    if (!accountMenuWrap?.contains(event.target)) {
        closeAccountMenu();
    }
});

document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
        closeSearchModal();
        closeProfileModal();
        closeSettingsModal();
        closeHelpModal();
        closeAccountMenu();
    }
});

async function initializeApp() {
    applyPreferences(loadStoredPreferences());
    setActiveUser(null);
    setSessionSummary(null);
    setSafetySummary(null);
    setChatStatus("");
    if (sessionSearchInput) {
        sessionSearchInput.value = "";
    }
    toggleChatEmpty(true);
    setActiveSidebarButton(newChatButton);
    await loadCurrentUser();
}

initializeApp();
