# mongo_db.py - MongoDB operations
from pymongo import MongoClient
from datetime import datetime, timedelta
from typing import Dict, Optional

class MongoDB:
    def __init__(self, mongo_uri: str):
        self.client = MongoClient(mongo_uri)
        self.db = self.client.telegram_movie_bot
        
    def add_interaction(self, user_id: int, username: str, chat_id: int, chat_type: str, chat_title: Optional[str]):
        """Track user and chat interactions"""
        # Update or create user
        self.db.users.update_one(
            {'user_id': user_id},
            {
                '$setOnInsert': {
                    'user_id': user_id,
                    'username': username,
                    'first_seen': datetime.now(),
                    'last_seen': datetime.now()
                },
                '$set': {'last_seen': datetime.now()},
                '$inc': {'request_count': 0}
            },
            upsert=True
        )
        
        # For groups/channels
        if chat_type != 'private':
            self.db.groups.update_one(
                {'chat_id': chat_id},
                {
                    '$setOnInsert': {
                        'chat_id': chat_id,
                        'title': chat_title,
                        'type': chat_type,
                        'first_seen': datetime.now()
                    },
                    '$set': {'last_active': datetime.now()}
                },
                upsert=True
            )

    def increment_request(self, user_id: int):
        """Increment user's request count"""
        self.db.users.update_one(
            {'user_id': user_id},
            {
                '$inc': {'request_count': 1},
                '$set': {'last_seen': datetime.now()}
            }
        )

    def get_stats(self) -> Dict:
        """Get comprehensive bot statistics"""
        now = datetime.now()
        return {
            'total_users': self.db.users.count_documents({}),
            'total_groups': self.db.groups.count_documents({}),
            'total_requests': sum(user['request_count'] for user in self.db.users.find({}, {'request_count': 1})),
            'active_last_24h': self.db.users.count_documents({
                'last_seen': {'$gte': now - timedelta(hours=24)}
            }),
            'timestamp': now.strftime("%Y-%m-%d %H:%M:%S")
        }

    def close(self):
        """Close MongoDB connection"""
        self.client.close()
