"""
app/tools/business_tools.py
─────────────────────────────
LangChain tools for enterprise business actions.
Each tool maps to a real helpdesk operation backed by the mock DB.

Tools:
  - create_ticket       → raise a new support ticket
  - get_ticket_status   → check an existing ticket
  - list_open_tickets   → view all open tickets
  - get_employee_info   → look up an employee
  - generate_report     → management summary report
"""

import uuid
from datetime import datetime
from langchain_core.tools import tool
from app.db.mock_db import tickets_db, employees_db


@tool
def create_ticket(title: str, description: str, priority: str = "medium") -> str:
    """
    Create a new support ticket in the system.

    Args:
        title:       Short summary of the issue (max 80 chars)
        description: Full description of the problem
        priority:    Urgency level — low | medium | high
    """
    priority = priority.lower()
    if priority not in ("low", "medium", "high"):
        priority = "medium"

    ticket_id = f"TKT-{str(uuid.uuid4())[:8].upper()}"

    tickets_db[ticket_id] = {
        "id":          ticket_id,
        "title":       title,
        "description": description,
        "priority":    priority,
        "status":      "open",
        "created_at":  datetime.now().isoformat(),
    }

    return (
        f"  Ticket Created Successfully\n"
        f"  ID          : {ticket_id}\n"
        f"  Title       : {title}\n"
        f"  Description : {description}\n"
        f"  Priority    : {priority.upper()}\n"
        f"  Status      : OPEN\n"
        f"  Created At  : {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    )


@tool
def get_ticket_status(ticket_id: str) -> str:
    """
    Retrieve the current status of a support ticket by its ID.

    Args:
        ticket_id: The ticket ID (e.g. TKT-A1B2C3D4)
    """
    ticket = tickets_db.get(ticket_id.upper())

    if not ticket:
        return (
            f"❌ No ticket found with ID '{ticket_id}'.\n"
            f"   Please verify the ID and try again."
        )

    return (
        f"  Ticket Details\n"
        f"  ID          : {ticket['id']}\n"
        f"  Title       : {ticket['title']}\n"
        f"  Description : {ticket['description']}\n"
        f"  Priority    : {ticket['priority'].upper()}\n"
        f"  Status      : {ticket['status'].upper()}\n"
        f"  Created At  : {ticket['created_at']}"
    )


@tool
def list_open_tickets() -> str:
    """
    List all currently open support tickets in the system.
    Returns ticket IDs, titles, and priorities.
    """
    open_tickets = [t for t in tickets_db.values() if t["status"] == "open"]

    if not open_tickets:
        return "No open tickets — all issues are resolved!"

    lines = [f"Open Tickets — {len(open_tickets)} found:\n"]
    for t in open_tickets:
        lines.append(
            f"  • [{t['priority'].upper():<6}] {t['id']}  |  {t['title']}"
        )
    return "\n".join(lines)


@tool
def get_employee_info(employee_id: str) -> str:
    """
    Fetch profile information for an employee by their ID.

    Args:
        employee_id: Employee ID (e.g. E001, E002, E003, E004, E005)
    """
    emp = employees_db.get(employee_id.upper())

    if not emp:
        available = ", ".join(employees_db.keys())
        return (
            f"No employee found with ID '{employee_id}'.\n"
            f"   Available IDs: {available}"
        )

    return (
        f"👤 Employee Profile\n"
        f"  ID         : {employee_id.upper()}\n"
        f"  Name       : {emp['name']}\n"
        f"  Department : {emp['dept']}\n"
        f"  Email      : {emp['email']}\n"
        f"  Status     : {emp['status']}"
    )


@tool
def generate_report() -> str:
    """
    Generate a summary report of all support tickets in the system.
    Includes counts by status and priority, plus a full ticket listing.
    """
    if not tickets_db:
        return "Report: No tickets have been created yet."

    all_tickets   = list(tickets_db.values())
    open_tickets  = [t for t in all_tickets if t["status"] == "open"]
    high_priority = [t for t in open_tickets if t["priority"] == "high"]
    med_priority  = [t for t in open_tickets if t["priority"] == "medium"]
    low_priority  = [t for t in open_tickets if t["priority"] == "low"]

    lines = [
        f"Support Ticket Report — {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"{'─' * 45}",
        f"  Total Tickets    : {len(all_tickets)}",
        f"  Open             : {len(open_tickets)}",
        f"  ├─ High Priority : {len(high_priority)}",
        f"  ├─ Medium        : {len(med_priority)}",
        f"  └─ Low           : {len(low_priority)}",
        f"{'─' * 45}",
        f"  Open Ticket Breakdown:",
    ]

    if open_tickets:
        for t in open_tickets:
            lines.append(f"    [{t['priority'].upper():<6}] {t['id']}  —  {t['title']}")
    else:
        lines.append("    No open tickets.")

    return "\n".join(lines)


# Export all tools as a list for agent registration
ALL_TOOLS = [
    create_ticket,
    get_ticket_status,
    list_open_tickets,
    get_employee_info,
    generate_report,
]