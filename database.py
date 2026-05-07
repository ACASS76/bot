from pymongo import MongoClient
from config import MONGO_URI, DEFAULT_AFFILIATE_LINK

client = MongoClient(MONGO_URI)
db = client["bot_1win_db"]
users_collection = db["users"]
settings_collection = db["settings"]

def init_db():
    if not settings_collection.find_one({"_id": "affiliate_link"}):
        settings_collection.insert_one({"_id": "affiliate_link", "url": DEFAULT_AFFILIATE_LINK})

def get_affiliate_link():
    doc = settings_collection.find_one({"_id": "affiliate_link"})
    return doc["url"] if doc else DEFAULT_AFFILIATE_LINK

def set_affiliate_link(new_url):
    settings_collection.update_one({"_id": "affiliate_link"}, {"$set": {"url": new_url}}, upsert=True)

def get_user(user_id):
    return users_collection.find_one({"user_id": user_id})

def save_user(user_id, username):
    users_collection.update_one(
        {"user_id": user_id},
        {"$set": {"user_id": user_id, "username": username}},
        upsert=True
    )

def update_user_status(user_id, status):
    users_collection.update_one(
        {"user_id": user_id},
        {"$set": {"status": status}}
    )