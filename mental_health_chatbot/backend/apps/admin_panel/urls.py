from django.urls import path

from .views import AdminDashboardView, FlaggedMessagesView, AuditLogsView, audit_logs_page
urlpatterns = [
    path("dashboard/", AdminDashboardView.as_view(), name="admin-dashboard"),
    path("flagged-messages/", FlaggedMessagesView.as_view(), name="flagged-messages"),
    path("audit-logs/", AuditLogsView.as_view(), name="audit-logs"),
    path("audit-logs-page/", audit_logs_page, name="audit-logs-page"),
]
