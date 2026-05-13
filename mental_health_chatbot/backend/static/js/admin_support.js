const refreshButton = document.getElementById("refresh-dashboard");
const showAuditLogsButton = document.getElementById("show-audit-logs");
const refreshAuditLogsButton = document.getElementById("refresh-audit-logs");
const dashboardHealth = document.getElementById("dashboard-health");
const dashboardUpdated = document.getElementById("dashboard-updated");

const metricUsers = document.getElementById("metric-users");
const metricSessions = document.getElementById("metric-sessions");
const metricMessages = document.getElementById("metric-messages");
const metricMoodCheckins = document.getElementById("metric-mood-checkins");
const metricFlaggedMessages = document.getElementById("metric-flagged-messages");
const metricEscalatedSessions = document.getElementById("metric-escalated-sessions");
const metricActiveSessions = document.getElementById("metric-active-sessions");
const metricFallbackMessages = document.getElementById("metric-fallback-messages");

const heroUnreviewed = document.getElementById("hero-unreviewed");
const heroAverageStress = document.getElementById("hero-average-stress");

const statusBreakdown = document.getElementById("status-breakdown");
const riskBreakdown = document.getElementById("risk-breakdown");
const moodBreakdown = document.getElementById("mood-breakdown");
const insightList = document.getElementById("insight-list");
const flaggedQueue = document.getElementById("flagged-queue");
const recentSessions = document.getElementById("recent-sessions");
const recentCheckins = document.getElementById("recent-checkins");
const auditSection = document.getElementById("audit-section");
const auditLogList = document.getElementById("audit-log-list");

function formatDate(value) {
    if (!value) {
        return "No date";
    }

    return new Intl.DateTimeFormat("en-ZA", {
        dateStyle: "medium",
        timeStyle: "short",
    }).format(new Date(value));
}

function toTitleCase(value) {
    return value
        .replace(/_/g, " ")
        .replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function escapeHtml(value = "") {
    return String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#39;");
}

function renderBreakdown(container, data) {
    const entries = Object.entries(data || {});
    if (!entries.length) {
        container.innerHTML = '<div class="empty-card">No data available yet.</div>';
        return;
    }

    container.innerHTML = entries.map(([label, value]) => `
        <div class="breakdown-row">
            <span>${toTitleCase(label)}</span>
            <strong class="breakdown-value">${value}</strong>
        </div>
    `).join("");
}

function renderInsights(payload) {
    const items = [
        {
            title: "Unreviewed flagged queue",
            body: `${payload.insights.unreviewed_flagged} flagged messages still need review.`,
        },
        {
            title: "High-risk conversation load",
            body: `${payload.insights.high_risk_messages} user messages have reached high risk.`,
        },
        {
            title: "Support-ready resources",
            body: `${payload.insights.support_resources} resources are active for support teams.`,
        },
        {
            title: "Reviewed flagged cases",
            body: `${payload.totals.reviewed_flagged} flagged messages have already been reviewed.`,
        },
    ];

    insightList.innerHTML = items.map((item) => `
        <div class="insight-item">
            <strong>${item.title}</strong>
            <p>${item.body}</p>
        </div>
    `).join("");
}

function renderFlaggedQueue(items) {
    if (!items.length) {
        flaggedQueue.innerHTML = '<div class="empty-card">No flagged conversations are waiting right now.</div>';
        return;
    }

    flaggedQueue.innerHTML = items.map((item) => `
        <article class="queue-item">
            <div class="queue-head">
                <div>
                    <strong>${item.username} | ${item.session_title}</strong>
                    <div class="queue-meta">Session #${item.session_id} | ${formatDate(item.created_at)}</div>
                </div>
                <span class="queue-risk ${item.risk_level}">${item.risk_level.toUpperCase()}</span>
            </div>
            <p>${item.content}</p>
            <div class="queue-meta">Sentiment: ${item.sentiment}. Categories: ${(item.detected_categories || []).join(", ") || "general"}.</div>
        </article>
    `).join("");
}

function renderRecentSessions(items) {
    if (!items.length) {
        recentSessions.innerHTML = '<div class="empty-card">No sessions have been created yet.</div>';
        return;
    }

    recentSessions.innerHTML = items.map((item) => `
        <article class="stack-item">
            <div class="stack-head">
                <div>
                    <strong>${item.title}</strong>
                    <div class="stack-meta">${item.username} | ${formatDate(item.updated_at)}</div>
                </div>
                <span class="stack-pill">${item.status}</span>
            </div>
            <p>Risk: ${item.last_risk_level}. Messages: ${item.message_count}.</p>
        </article>
    `).join("");
}

function renderRecentCheckins(items) {
    if (!items.length) {
        recentCheckins.innerHTML = '<div class="empty-card">No mood check-ins have been submitted yet.</div>';
        return;
    }

    recentCheckins.innerHTML = items.map((item) => `
        <article class="stack-item">
            <div class="stack-head">
                <div>
                    <strong>${toTitleCase(item.mood)}</strong>
                    <div class="stack-meta">${item.username} | ${formatDate(item.created_at)}</div>
                </div>
                <span class="stack-pill">Stress ${item.stress_level}/5</span>
            </div>
            <p>${item.notes || "No note was added for this mood check-in."}</p>
        </article>
    `).join("");
}

function renderAuditLogs(items) {
    if (!items.length) {
        auditLogList.innerHTML = '<div class="empty-card">No audit activity has been recorded yet.</div>';
        return;
    }

    auditLogList.innerHTML = items.map((item) => `
        <article class="audit-item">
            <div class="audit-head">
                <div>
                    <strong>${escapeHtml(item.username)} | ${escapeHtml(item.session_title)}</strong>
                    <div class="audit-meta">${formatDate(item.created_at)} | Session #${item.session_id} | ${escapeHtml(item.role)}</div>
                </div>
                <span class="queue-risk ${escapeHtml(item.risk_level)}">${escapeHtml(item.risk_level.toUpperCase())}</span>
            </div>
            <p>${escapeHtml(item.content || "No content was recorded.")}</p>
            <div class="audit-meta">
                Sentiment: ${escapeHtml(item.sentiment)}. Source: ${escapeHtml(item.source)}. Flagged: ${item.flagged ? "yes" : "no"}.
            </div>
        </article>
    `).join("");
}

function renderDashboard(payload) {
    metricUsers.textContent = payload.totals.users;
    metricSessions.textContent = payload.totals.sessions;
    metricMessages.textContent = payload.totals.messages;
    metricMoodCheckins.textContent = payload.totals.mood_checkins;
    metricFlaggedMessages.textContent = payload.totals.flagged_messages;
    metricEscalatedSessions.textContent = payload.totals.escalated_sessions;
    metricActiveSessions.textContent = payload.totals.active_sessions;
    metricFallbackMessages.textContent = payload.totals.fallback_messages;

    heroUnreviewed.textContent = payload.insights.unreviewed_flagged;
    heroAverageStress.textContent = Number(payload.insights.average_stress_level || 0).toFixed(1);

    renderBreakdown(statusBreakdown, payload.breakdowns.session_statuses);
    renderBreakdown(riskBreakdown, payload.breakdowns.risk_levels);
    renderBreakdown(moodBreakdown, payload.breakdowns.moods);
    renderInsights(payload);
    renderFlaggedQueue(payload.latest_flagged || []);
    renderRecentSessions(payload.recent_sessions || []);
    renderRecentCheckins(payload.recent_mood_checkins || []);

    dashboardHealth.textContent = "Dashboard is live and ready";
    dashboardUpdated.textContent = `Last refreshed ${formatDate(new Date().toISOString())}`;
}

async function loadDashboard() {
    dashboardHealth.textContent = "Refreshing support data...";
    dashboardUpdated.textContent = "Loading latest activity.";
    refreshButton.disabled = true;

    try {
        const response = await fetch("/api/admin-panel/dashboard/", {
            credentials: "same-origin",
        });
        if (!response.ok) {
            throw new Error(`Request failed with status ${response.status}`);
        }

        const payload = await response.json();
        renderDashboard(payload);
    } catch (error) {
        dashboardHealth.textContent = "Could not load admin dashboard";
        dashboardUpdated.textContent = "Please refresh or confirm you are signed in as support/admin.";
    } finally {
        refreshButton.disabled = false;
    }
}

async function loadAuditLogs() {
    auditLogList.innerHTML = '<div class="empty-card">Loading audit logs.</div>';
    refreshAuditLogsButton.disabled = true;

    try {
        const response = await fetch("/api/admin-panel/audit-logs/", {
            credentials: "same-origin",
        });
        if (!response.ok) {
            throw new Error(`Request failed with status ${response.status}`);
        }

        const payload = await response.json();
        renderAuditLogs(payload.audit_logs || []);
    } catch (error) {
        auditLogList.innerHTML = '<div class="empty-card">Could not load audit logs. Confirm you are signed in as admin/support.</div>';
    } finally {
        refreshAuditLogsButton.disabled = false;
    }
}

refreshButton.addEventListener("click", loadDashboard);
showAuditLogsButton?.addEventListener("click", () => {
    auditSection?.scrollIntoView({ behavior: "smooth", block: "start" });
});
refreshAuditLogsButton?.addEventListener("click", loadAuditLogs);

loadDashboard();
loadAuditLogs();

if (window.location.hash === "#audit-section") {
    auditSection?.scrollIntoView({ behavior: "smooth", block: "start" });
}
