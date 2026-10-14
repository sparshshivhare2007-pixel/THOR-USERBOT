import time
from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URL, DB_NAME

client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]

users    = db.users
hosted   = db.hosted
sessions = db.sessions


async def save_user(user):
    await users.update_one(
        {"user_id": user.id},
        {"$set": {
            "name": user.first_name,
            "username": user.username,
            "joined_at": time.time(),
        }},
        upsert=True
    )

async def save_hosted(user_id, session, owner, pid):
    await hosted.update_one(
        {"user_id": user_id},
        {"$set": {
            "session": session,
            "owner": owner,
            "pid": pid,
            "started_at": time.time(),
        }},
        upsert=True
    )

async def get_hosted(user_id):
    return await hosted.find_one({"user_id": user_id})

async def delete_hosted(user_id):
    await hosted.delete_one({"user_id": user_id})

async def set_stage(user_id, stage):
    await sessions.update_one(
        {"user_id": user_id},
        {"$set": {"stage": stage}},
        upsert=True
    )

async def get_stage(user_id):
    doc = await sessions.find_one({"user_id": user_id})
    return doc.get("stage") if doc else None

async def clear_stage(user_id):
    await sessions.delete_one({"user_id": user_id})
