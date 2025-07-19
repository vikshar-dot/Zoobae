from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.errors import DuplicateKeyError
from typing import List, Optional, Dict, Any
from datetime import datetime
import os
from bson import ObjectId
import uuid

class DatabaseService:
    def __init__(self):
        MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017/")
        self.client = MongoClient(MONGO_URL)
        self.db = self.client["dating_app"]
        
        # Collections
        self.users = self.db["users"]
        self.profiles = self.db["profiles"]
        self.photos = self.db["photos"]
        self.prompts = self.db["prompts"]
        
        # Create indexes for better performance
        self._create_indexes()
    
    def _create_indexes(self):
        """Create database indexes for optimal performance"""
        # Users collection indexes
        self.users.create_index([("email", ASCENDING)], unique=True)
        self.users.create_index([("created_at", DESCENDING)])
        
        # Profiles collection indexes
        self.profiles.create_index([("user_id", ASCENDING)], unique=True)
        self.profiles.create_index([("verification_status", ASCENDING)])
        self.profiles.create_index([("updated_at", DESCENDING)])
        
        # Photos collection indexes
        self.photos.create_index([("user_id", ASCENDING)])
        self.photos.create_index([("order", ASCENDING)])
        self.photos.create_index([("is_primary", ASCENDING)])
        
        # Prompts collection indexes
        self.prompts.create_index([("user_id", ASCENDING)])
        self.prompts.create_index([("order", ASCENDING)])
    
    def create_user(self, email: str, hashed_password: str) -> str:
        """Create a new user and return user_id"""
        user_id = str(uuid.uuid4())
        user_doc = {
            "_id": user_id,
            "email": email,
            "password": hashed_password,
            "created_at": datetime.utcnow(),
            "is_active": True
        }
        
        try:
            self.users.insert_one(user_doc)
            return user_id
        except DuplicateKeyError:
            raise ValueError("Email already exists")
    
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Get user by email"""
        return self.users.find_one({"email": email})
    
    def get_user_by_id(self, user_id: str) -> Optional[Dict]:
        """Get user by ID"""
        return self.users.find_one({"_id": user_id})
    
    def create_profile(self, user_id: str, profile_data: Dict) -> str:
        """Create a new profile for user"""
        profile_id = str(uuid.uuid4())
        profile_doc = {
            "_id": profile_id,
            "user_id": user_id,
            **profile_data,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        self.profiles.insert_one(profile_doc)
        return profile_id
    
    def update_profile(self, user_id: str, update_data: Dict) -> bool:
        """Update user profile"""
        update_data["updated_at"] = datetime.utcnow()
        result = self.profiles.update_one(
            {"user_id": user_id},
            {"$set": update_data}
        )
        return result.modified_count > 0
    
    def get_profile(self, user_id: str) -> Optional[Dict]:
        """Get user profile"""
        return self.profiles.find_one({"user_id": user_id})
    
    def add_photo(self, user_id: str, photo_data: Dict) -> str:
        """Add a new photo for user"""
        photo_id = str(uuid.uuid4())
        photo_doc = {
            "_id": photo_id,
            "user_id": user_id,
            **photo_data,
            "created_at": datetime.utcnow()
        }
        
        # If this is the first photo, make it primary
        if photo_data.get("is_primary", False):
            self.photos.update_many(
                {"user_id": user_id},
                {"$set": {"is_primary": False}}
            )
        
        self.photos.insert_one(photo_doc)
        return photo_id
    
    def update_photo(self, photo_id: str, update_data: Dict) -> bool:
        """Update photo data"""
        result = self.photos.update_one(
            {"_id": photo_id},
            {"$set": update_data}
        )
        return result.modified_count > 0
    
    def delete_photo(self, photo_id: str) -> bool:
        """Delete a photo"""
        result = self.photos.delete_one({"_id": photo_id})
        return result.deleted_count > 0
    
    def get_user_photos(self, user_id: str) -> List[Dict]:
        """Get all photos for a user, ordered by order field"""
        return list(self.photos.find(
            {"user_id": user_id}
        ).sort("order", ASCENDING))
    
    def add_prompt(self, user_id: str, prompt_data: Dict) -> str:
        """Add a new prompt for user"""
        prompt_id = str(uuid.uuid4())
        prompt_doc = {
            "_id": prompt_id,
            "user_id": user_id,
            **prompt_data,
            "created_at": datetime.utcnow()
        }
        
        self.prompts.insert_one(prompt_doc)
        return prompt_id
    
    def update_prompt(self, prompt_id: str, update_data: Dict) -> bool:
        """Update prompt data"""
        result = self.prompts.update_one(
            {"_id": prompt_id},
            {"$set": update_data}
        )
        return result.modified_count > 0
    
    def get_user_prompts(self, user_id: str) -> List[Dict]:
        """Get all prompts for a user, ordered by order field"""
        return list(self.prompts.find(
            {"user_id": user_id}
        ).sort("order", ASCENDING))
    
    def get_profiles_for_matching(self, limit: int = 50, skip: int = 0) -> List[Dict]:
        """Get profiles for matching algorithm (optimized query)"""
        pipeline = [
            {"$match": {"is_active": True}},
            {"$lookup": {
                "from": "profiles",
                "localField": "_id",
                "foreignField": "user_id",
                "as": "profile"
            }},
            {"$unwind": "$profile"},
            {"$lookup": {
                "from": "photos",
                "localField": "_id",
                "foreignField": "user_id",
                "as": "photos"
            }},
            {"$project": {
                "user_id": "$_id",
                "email": 1,
                "profile": 1,
                "photos": {"$slice": ["$photos", 1]}  # Only get primary photo
            }},
            {"$skip": skip},
            {"$limit": limit}
        ]
        
        return list(self.users.aggregate(pipeline))
    
    def close(self):
        """Close database connection"""
        self.client.close()

# Global database instance
db_service = DatabaseService() 