import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DBNAME = os.getenv("MONGO_DBNAME")

if not MONGO_URI or not MONGO_DBNAME:
    raise RuntimeError("MONGO_URI and MONGO_DBNAME must be set in .env")

client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
db = client[MONGO_DBNAME]
