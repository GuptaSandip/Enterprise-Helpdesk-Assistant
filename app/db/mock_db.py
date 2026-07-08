"""
app/db/mock_db.py
──────────────────
In-memory mock database for tickets and employees.
In production this would be replaced with PostgreSQL / MongoDB.
"""

# ── Ticket store (grows at runtime) ──────────────
tickets_db: dict[str, dict] = {}

# ── Employee master data (static seed) ───────────
employees_db: dict[str, dict] = {
    "E001": {
        "name":   "Rahul Sharma",
        "dept":   "Engineering",
        "email":  "rahul@company.com",
        "status": "Active",
    },
    "E002": {
        "name":   "Priya Patel",
        "dept":   "Human Resources",
        "email":  "priya@company.com",
        "status": "Active",
    },
    "E003": {
        "name":   "Arjun Singh",
        "dept":   "Sales",
        "email":  "arjun@company.com",
        "status": "On Leave",
    },
    "E004": {
        "name":   "Sneha Mehta",
        "dept":   "Finance",
        "email":  "sneha@company.com",
        "status": "Active",
    },
    "E005": {
        "name":   "Vikram Nair",
        "dept":   "Operations",
        "email":  "vikram@company.com",
        "status": "Active",
    },
}