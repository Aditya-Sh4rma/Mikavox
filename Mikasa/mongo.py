"""
Mikasa/mongo.py
Poora database yahan se handle hota hai — do collections:
  users  -> jitne users ne bot ko private mein /start kiya
  groups -> jitne groups mein bot add hua hai (abhi tak remove nahi hua)

Baaki files (plugins) sirf yahan diye functions ko call karengi,
kahin bhi direct MongoDB query nahi likhni.
"""

from motor.motor_asyncio import AsyncIOMotorClient

from config import MONGO_URL

_client = AsyncIOMotorClient(MONGO_URL)
_db = _client["mikasa"]

users_col = _db["users"]
groups_col = _db["groups"]


# =============================
# USERS (private /start)
# =============================
async def add_user(user_id: int) -> bool:
    """Naya user save karta hai agar pehle se nahi hai.
    Returns True agar yeh pehli baar tha (naya user), False agar already tha."""
    existing = await users_col.find_one({"user_id": user_id})
    if existing:
        return False
    await users_col.insert_one({"user_id": user_id})
    return True


async def total_users() -> int:
    return await users_col.count_documents({})


# =============================
# GROUPS (bot add/remove)
# =============================
async def add_group(chat_id: int, title: str = "") -> bool:
    """Naya group save karta hai. Returns True agar naya add hua."""
    existing = await groups_col.find_one({"chat_id": chat_id})
    if existing:
        return False
    await groups_col.insert_one({"chat_id": chat_id, "title": title})
    return True


async def remove_group(chat_id: int) -> None:
    """Bot group se remove/kick hone par entry delete karta hai."""
    await groups_col.delete_one({"chat_id": chat_id})


async def total_groups() -> int:
    return await groups_col.count_documents({})


async def all_user_ids() -> list[int]:
    """Broadcast ke liye — sab user IDs ek list mein."""
    cursor = users_col.find({}, {"user_id": 1, "_id": 0})
    return [doc["user_id"] async for doc in cursor]


async def all_group_ids() -> list[int]:
    """Broadcast ke liye — sab group chat IDs ek list mein."""
    cursor = groups_col.find({}, {"chat_id": 1, "_id": 0})
    return [doc["chat_id"] async for doc in cursor]
