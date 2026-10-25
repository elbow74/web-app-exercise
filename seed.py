"""Insert sample posts for development."""

from datetime import datetime
from db import db

db.posts.insert_many(
    [
        {
            "username": "alex",
            "image_path": "uploads/sample1.jpg",
            "caption": "Thrifted jacket with black jeans",
            "buy_links": [
                "https://www.example.com/jacket",
                "https://www.example.com/jeans",
            ],
            "hashtags": ["vintage", "thrift"],
            "liked_by": [],
            "created_at": datetime.utcnow(),
        },
        {
            "username": "sam",
            "image_path": "uploads/sample2.jpg",
            "caption": "Streetwear fit for class",
            "buy_links": [
                "https://www.example.com/jacket",
                "https://www.example.com/jeans",
            ],
            "hashtags": ["streetwear"],
            "liked_by": [],
            "created_at": datetime.utcnow(),
        },
    ]
)
print("Inserted sample posts")
