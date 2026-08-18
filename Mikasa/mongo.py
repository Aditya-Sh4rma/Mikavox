from pymongo import AsyncMongoClient

from config import MONGO_URL

_client = AsyncMongoClient(MONGO_URL)
_db = _client["mikasa"]

users_col = _db["users"]
groups_col = _db["groups"]


async def add_user(user_id: int) -> bool:
    existing = await users_col.find_one({"user_id": user_id})
    if existing:
        return False
    await users_col.insert_one({"user_id": user_id})
    return True


async def total_users() -> int:
    return await users_col.count_documents({})


async def add_group(chat_id: int, title: str = "") -> bool:
    existing = await groups_col.find_one({"chat_id": chat_id})
    if existing:
        return False
    await groups_col.insert_one({"chat_id": chat_id, "title": title})
    return True


async def remove_group(chat_id: int) -> None:
    await groups_col.delete_one({"chat_id": chat_id})


async def total_groups() -> int:
    return await groups_col.count_documents({})


async def all_user_ids() -> list[int]:
    cursor = users_col.find({}, {"user_id": 1, "_id": 0})
    return [doc["user_id"] async for doc in cursor]


async def all_group_ids() -> list[int]:
    cursor = groups_col.find({}, {"chat_id": 1, "_id": 0})
    return [doc["chat_id"] async for doc in cursor]
