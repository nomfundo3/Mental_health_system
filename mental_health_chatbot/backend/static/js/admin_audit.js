const refreshAuditLogsButton = document.getElementById("refresh-audit-logs");
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

function escapeHtml(value = "") {
    return String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#39;");
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
        auditLogList.innerHTML = '<div class="empty-card">Could not load audit logs. Confirm you are signed in as a superuser.</div>';
    } finally {
        refreshAuditLogsButton.disabled = false;
    }
}

refreshAuditLogsButton?.addEventListener("click", loadAuditLogs);

loadAuditLogs();
