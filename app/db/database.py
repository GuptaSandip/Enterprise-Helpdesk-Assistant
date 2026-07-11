"""
app/db/database.py
───────────────────
MongoDB connection using both:
  - Motor (async) for FastAPI endpoints
  - PyMongo (sync) for LangChain tools (sync context)
"""

import os
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from app.config import settings

# ── Async client (FastAPI) ────────────────────────────────────────────────────
async_client = None
async_db     = None

# ── Sync client (LangChain tools) ─────────────────────────────────────────────
sync_client = None
sync_db     = None


async def connect_db():
    """Connect to MongoDB Atlas (async + sync) and seed employee data."""
    global async_client, async_db, sync_client, sync_db

    # Async client for FastAPI
    async_client = AsyncIOMotorClient(settings.MONGODB_URI)
    async_db     = async_client[settings.MONGODB_DB_NAME]

    # Sync client for LangChain tools
    sync_client  = MongoClient(settings.MONGODB_URI)
    sync_db      = sync_client[settings.MONGODB_DB_NAME]

    print(f"✅ Connected to MongoDB: {settings.MONGODB_DB_NAME}")
    await seed_employees()


async def disconnect_db():
    """Close MongoDB connections."""
    global async_client, sync_client
    if async_client:
        async_client.close()
    if sync_client:
        sync_client.close()
    print("🔌 MongoDB connection closed.")


async def get_db():
    """Return async database instance (for FastAPI routes)."""
    return async_db


def get_sync_db():
    """Return sync database instance (for LangChain tools)."""
    return sync_db


# ── Seed employee data ────────────────────────────────────────────────────────

EMPLOYEE_SEED = [
    {"employee_id": "E001", "name": "Rahul Sharma",  "dept": "Engineering",     "email": "rahul@company.com",  "status": "Active"},
    {"employee_id": "E002", "name": "Priya Patel",   "dept": "Human Resources", "email": "priya@company.com",  "status": "Active"},
    {"employee_id": "E003", "name": "Arjun Singh",   "dept": "Sales",           "email": "arjun@company.com",  "status": "On Leave"},
    {"employee_id": "E004", "name": "Sneha Mehta",   "dept": "Finance",         "email": "sneha@company.com",  "status": "Active"},
    {"employee_id": "E005", "name": "Vikram Nair",   "dept": "Operations",      "email": "vikram@company.com", "status": "Active"},
]


async def seed_employees():
    count = await async_db.employees.count_documents({})
    if count == 0:
        await async_db.employees.insert_many(EMPLOYEE_SEED)
        print(f"✅ Seeded {len(EMPLOYEE_SEED)} employees into MongoDB.")
    else:
        print(f"ℹ️  Employees already seeded ({count} records found).")