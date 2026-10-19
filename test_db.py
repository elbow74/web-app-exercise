import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"), serverSelectionTimeoutMS=5000)

try:
    client.admin.command("ping")
    print("connected")

    db = client[os.getenv("MONGO_DBNAME")]
    print("Collections:", db.list_collection_names())
except Exception as e:
    print("not connected", e)