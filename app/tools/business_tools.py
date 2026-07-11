"""
app/tools/business_tools.py
─────────────────────────────
LangChain tools — SYNCHRONOUS using PyMongo.
Sync is required because LangChain agent runs in a sync context.

Tools:
  - create_ticket       → insert ticket into MongoDB
  - get_ticket_status   → find ticket by ID
  - list_open_tickets   → find all open tickets
  - get_employee_info   → find employee by ID
  - generate_report     → aggregate ticket stats
"""

import uuid
from datetime import datetime
from langchain_core.tools import tool
from app.db.database import get_sync_db


@tool
def create_ticket(title: str, description: str, priority: str = "medium") -> str:
    """
    Create a new support ticket in MongoDB.

    Args:
        title:       Short summary of the issue
        description: Full description of the problem
        priority:    Urgency level — low | medium | high
    """
    try:
        priority = priority.lower()
        if priority not in ("low", "medium", "high"):
            priority = "medium"

        ticket_id = f"TKT-{str(uuid.uuid4())[:8].upper()}"
        ticket = {
            "ticket_id":   ticket_id,
            "title":       title,
            "description": description,
            "priority":    priority,
            "status":      "open",
            "created_at":  datetime.utcnow().isoformat(),
        }

        db = get_sync_db()
        db.tickets.insert_one(ticket)

        return (
            f"✅ Ticket Created Successfully\n"
            f"  ID          : {ticket_id}\n"
            f"  Title       : {title}\n"
            f"  Description : {description}\n"
            f"  Priority    : {priority.upper()}\n"
            f"  Status      : OPEN\n"
            f"  Created At  : {datetime.utcnow().strftime('%Y-%m-%d %H:%M')} UTC"
        )
    except Exception as e:
        return f"❌ Failed to create ticket: {str(e)}"


@tool
def get_ticket_status(ticket_id: str) -> str:
    """
    Retrieve the current status of a support ticket by its ID.

    Args:
        ticket_id: The ticket ID (e.g. TKT-A1B2C3D4)
    """
    try:
        db     = get_sync_db()
        ticket = db.tickets.find_one({"ticket_id": ticket_id.upper()}, {"_id": 0})

        if not ticket:
            return f"❌ No ticket found with ID '{ticket_id}'. Please verify the ID."

        return (
            f"📋 Ticket Details\n"
            f"  ID          : {ticket['ticket_id']}\n"
            f"  Title       : {ticket['title']}\n"
            f"  Description : {ticket['description']}\n"
            f"  Priority    : {ticket['priority'].upper()}\n"
            f"  Status      : {ticket['status'].upper()}\n"
            f"  Created At  : {ticket['created_at']}"
        )
    except Exception as e:
        return f"❌ Error fetching ticket: {str(e)}"


@tool
def list_open_tickets() -> str:
    """List all currently open support tickets from MongoDB."""
    try:
        db           = get_sync_db()
        open_tickets = list(db.tickets.find({"status": "open"}, {"_id": 0}))

        if not open_tickets:
            return "✅ No open tickets — all issues are resolved!"

        lines = [f"📋 Open Tickets — {len(open_tickets)} found:\n"]
        for t in open_tickets:
            lines.append(f"  • [{t['priority'].upper():<6}] {t['ticket_id']}  |  {t['title']}")
        return "\n".join(lines)
    except Exception as e:
        return f"❌ Error listing tickets: {str(e)}"


@tool
def get_employee_info(employee_id: str) -> str:
    """
    Fetch profile information for an employee by their ID.

    Args:
        employee_id: Employee ID (e.g. E001, E002, E003, E004, E005)
    """
    try:
        db  = get_sync_db()
        emp = db.employees.find_one({"employee_id": employee_id.upper()}, {"_id": 0})

        if not emp:
            all_emps  = list(db.employees.find({}, {"employee_id": 1, "_id": 0}))
            available = ", ".join([e["employee_id"] for e in all_emps])
            return (
                f"❌ No employee found with ID '{employee_id}'.\n"
                f"   Available IDs: {available}"
            )

        return (
            f"👤 Employee Profile\n"
            f"  ID         : {emp['employee_id']}\n"
            f"  Name       : {emp['name']}\n"
            f"  Department : {emp['dept']}\n"
            f"  Email      : {emp['email']}\n"
            f"  Status     : {emp['status']}"
        )
    except Exception as e:
        return f"❌ Error fetching employee: {str(e)}"


@tool
def generate_report() -> str:
    """
    Generate a summary report of all support tickets from MongoDB.
    """
    try:
        db          = get_sync_db()
        all_tickets = list(db.tickets.find({}, {"_id": 0}))

        if not all_tickets:
            return "📊 Report: No tickets have been created yet."

        open_tickets  = [t for t in all_tickets if t["status"] == "open"]
        high_priority = [t for t in open_tickets if t["priority"] == "high"]
        med_priority  = [t for t in open_tickets if t["priority"] == "medium"]
        low_priority  = [t for t in open_tickets if t["priority"] == "low"]

        lines = [
            f"📊 Support Ticket Report — {datetime.utcnow().strftime('%Y-%m-%d %H:%M')} UTC",
            f"{'─' * 50}",
            f"  Total Tickets    : {len(all_tickets)}",
            f"  Open             : {len(open_tickets)}",
            f"  ├─ High Priority : {len(high_priority)}",
            f"  ├─ Medium        : {len(med_priority)}",
            f"  └─ Low           : {len(low_priority)}",
            f"{'─' * 50}",
            "  Open Ticket Breakdown:",
        ]

        for t in open_tickets:
            lines.append(f"    [{t['priority'].upper():<6}] {t['ticket_id']}  —  {t['title']}")

        return "\n".join(lines)
    except Exception as e:
        return f"❌ Error generating report: {str(e)}"


# Export all tools
ALL_TOOLS = [
    create_ticket,
    get_ticket_status,
    list_open_tickets,
    get_employee_info,
    generate_report,
]