
"""Test the MongoDB connection and list available collections."""

import os

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import PyMongoError

load_dotenv()

client = MongoClient(
    os.getenv("MONGO_URI"),
    serverSelectionTimeoutMS=5000,
)

try:
    client.admin.command("ping")
    print("connected")

    db = client[os.getenv("MONGO_DBNAME")]
    print("Collections:", db.list_collection_names())

except PyMongoError as error:
    print("not connected", error)

finally:
    client.close()
