import pandas as pd

historical_tickets = [
    {
        "ticket_id": "T001",
        "issue": "User cannot login, getting 'Invalid credentials' error",
        "category": "Authentication",
        "solution": "Password reset required. Guide user to reset password via forgot password link.",
        "resolved": True
    },
    {
        "ticket_id": "T002",
        "issue": "Application loading very slowly, timeout errors",
        "category": "Performance",
        "solution": "Clear browser cache and cookies. If persists, check if VPN is causing latency.",
        "resolved": True
    },
    {
        "ticket_id": "T003",
        "issue": "Cannot access dashboard, showing 'Access Denied'",
        "category": "Authorization",
        "solution": "User permissions need to be updated. Add user to 'Dashboard_Users' group in admin panel.",
        "resolved": True
    },
    {
        "ticket_id": "T004",
        "issue": "Getting error 'Session expired' after 5 minutes",
        "category": "Authentication",
        "solution": "Session timeout configuration issue. Update session timeout to 30 minutes in config file.",
        "resolved": True
    },
    {
        "ticket_id": "T005",
        "issue": "Reports not generating, stuck at 'Processing'",
        "category": "Reports",
        "solution": "Background job queue is stuck. Restart the report service and clear job queue.",
        "resolved": True
    },
    {
        "ticket_id": "T006",
        "issue": "User account locked after multiple failed login attempts",
        "category": "Authentication",
        "solution": "Account auto-locked for security. Unlock account in admin panel and ask user to reset password.",
        "resolved": True
    },
    {
        "ticket_id": "T007",
        "issue": "Data export to Excel not working, download fails",
        "category": "Export",
        "solution": "Export module memory limit exceeded. Reduce date range or apply filters to limit data size.",
        "resolved": True
    },
    {
        "ticket_id": "T008",
        "issue": "Email notifications not being received",
        "category": "Notifications",
        "solution": "Check spam folder first. If not there, verify email address in user profile and check SMTP logs.",
        "resolved": True
    },
    {
        "ticket_id": "T009",
        "issue": "Mobile app crashes on startup",
        "category": "Mobile",
        "solution": "Clear app cache/data or reinstall app. If persists, escalate to L3 for app version compatibility check.",
        "resolved": True
    },
    {
        "ticket_id": "T010",
        "issue": "Cannot upload files, getting 'File too large' error",
        "category": "Upload",
        "solution": "File size limit is 10MB. Compress file or split into smaller parts. For higher limit, submit change request.",
        "resolved": True
    }
]

df = pd.DataFrame(historical_tickets)
df.to_excel("data/historical_tickets.xlsx", index=False)
print(f"Created {len(historical_tickets)} sample tickets in data/historical_tickets.xlsx")


