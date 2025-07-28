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
        # Create missing collections for chat functionality
        self.chat_messages = self.db["chat_messages"]
        self.personality_insights = self.db["personality_insights"]
        
        # Create indexes for better performance
        self._create_indexes()
    
    def _convert_objectid_to_str(self, doc: Dict) -> Dict:
        """Convert ObjectId to string in MongoDB document"""
        if doc and "_id" in doc:
            doc["_id"] = str(doc["_id"])
        return doc
    
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
        
        # Chat messages collection indexes
        self.chat_messages.create_index([("user_id", ASCENDING)])
        self.chat_messages.create_index([("timestamp", ASCENDING)])
        
        # Personality insights collection indexes
        self.personality_insights.create_index([("user_id", ASCENDING)], unique=True)
    
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
        user = self.users.find_one({"email": email})
        return self._convert_objectid_to_str(user) if user else None
    
    def get_user_by_id(self, user_id: str) -> Optional[Dict]:
        """Get user by ID"""
        user = self.users.find_one({"_id": user_id})
        return self._convert_objectid_to_str(user) if user else None
    
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
        """Get user profile with photos and prompts"""
        profile = self.profiles.find_one({"user_id": user_id})
        if not profile:
            return None
        
        # Convert ObjectId to string
        profile = self._convert_objectid_to_str(profile)
        
        # Get user photos
        photos = self.get_user_photos(user_id)
        photos = [self._convert_objectid_to_str(photo) for photo in photos]
        
        # Get user prompts
        prompts = self.get_user_prompts(user_id)
        prompts = [self._convert_objectid_to_str(prompt) for prompt in prompts]
        
        # Add photos and prompts to profile
        profile["photos"] = photos
        profile["prompts"] = prompts
        
        return profile
    
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
        import os
        from pathlib import Path
        
        # Try to delete by _id first, then by id field
        photo = self.photos.find_one({"_id": photo_id})
        if not photo:
            # If not found by _id, try by id field
            photo = self.photos.find_one({"id": photo_id})
        
        if photo:
            # Delete the physical file
            try:
                # Extract filename from URL or use photo_id
                filename = f"{photo.get('id', photo_id)}.jpg"
                file_path = Path("uploads") / filename
                
                if file_path.exists():
                    os.remove(file_path)
                    print(f"Deleted physical file: {file_path}")
            except Exception as e:
                print(f"Error deleting physical file: {e}")
            
            # Delete from database
            result = self.photos.delete_one({"_id": photo["_id"]})
            return result.deleted_count > 0
        
        return False
    
    def get_user_photos(self, user_id: str) -> List[Dict]:
        """Get all photos for a user, ordered by order field"""
        photos = list(self.photos.find(
            {"user_id": user_id}
        ).sort("order", ASCENDING))
        
        # Convert ObjectIds to strings
        return [self._convert_objectid_to_str(photo) for photo in photos]
    
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
        prompts = list(self.prompts.find(
            {"user_id": user_id}
        ).sort("order", ASCENDING))
        
        # Convert ObjectIds to strings
        return [self._convert_objectid_to_str(prompt) for prompt in prompts]
    
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

    def update_photo_urls_to_localhost(self):
        """Update existing photo URLs to use localhost instead of placeholder URLs"""
        try:
            # Find all photos with placeholder URLs
            placeholder_photos = self.photos.find({
                "url": {"$regex": "^https://storage\\.example\\.com/"}
            })
            
            for photo in placeholder_photos:
                # Extract the photo ID from the placeholder URL
                photo_id = photo["id"]
                # Create new localhost URL
                new_url = f"http://localhost:8001/uploads/{photo_id}.jpg"
                
                # Update the photo URL
                self.photos.update_one(
                    {"_id": photo["_id"]},
                    {"$set": {"url": new_url}}
                )
                print(f"Updated photo {photo_id} URL to {new_url}")
                
        except Exception as e:
            print(f"Error updating photo URLs: {e}")

    def save_chat_message(self, user_id: str, message: str, sender: str, insights: Optional[Dict] = None) -> str:
        """Save a chat message to the database"""
        message_id = str(uuid.uuid4())
        message_doc = {
            "_id": message_id,
            "user_id": user_id,
            "message": message,
            "sender": sender,  # 'user' or 'ai'
            "insights": insights or {},
            "timestamp": datetime.utcnow()
        }
        
        self.chat_messages.insert_one(message_doc)
        return message_id

    def get_user_chat_history(self, user_id: str, limit: int = 50) -> List[Dict]:
        """Get user's chat history with AI"""
        messages = list(self.chat_messages.find(
            {"user_id": user_id}
        ).sort("timestamp", ASCENDING).limit(limit))
        return [self._convert_objectid_to_str(message) for message in messages]

    def save_personality_insights(self, user_id: str, insights: Dict) -> str:
        """Save personality insights for a user"""
        insight_id = str(uuid.uuid4())
        insight_doc = {
            "_id": insight_id,
            "user_id": user_id,
            "insights": insights,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        # Update existing insights or create new ones
        existing = self.personality_insights.find_one({"user_id": user_id})
        if existing:
            self.personality_insights.update_one(
                {"user_id": user_id},
                {"$set": {"insights": insights, "updated_at": datetime.utcnow()}}
            )
            return existing["_id"]
        else:
            self.personality_insights.insert_one(insight_doc)
            return insight_id

    def get_personality_insights(self, user_id: str) -> Optional[Dict]:
        """Get personality insights for a user"""
        insights = self.personality_insights.find_one({"user_id": user_id})
        if insights:
            return self._convert_objectid_to_str(insights)
        return None

    # Delete methods for account deletion
    def delete_user_profile(self, user_id: str) -> bool:
        """Delete user profile from profiles collection"""
        result = self.profiles.delete_one({"user_id": user_id})
        return result.deleted_count > 0

    def delete_user_photos(self, user_id: str) -> int:
        """Delete all user photos from photos collection"""
        result = self.photos.delete_many({"user_id": user_id})
        return result.deleted_count

    def delete_user_prompts(self, user_id: str) -> int:
        """Delete all user prompts from prompts collection"""
        result = self.prompts.delete_many({"user_id": user_id})
        return result.deleted_count

    def delete_user(self, user_id: str) -> bool:
        """Delete user from users collection"""
        result = self.users.delete_one({"_id": user_id})
        return result.deleted_count > 0

    def delete_user_chat_messages(self, user_id: str) -> int:
        """Delete all user chat messages"""
        result = self.chat_messages.delete_many({"user_id": user_id})
        return result.deleted_count

    def delete_user_personality_insights(self, user_id: str) -> bool:
        """Delete user personality insights"""
        result = self.personality_insights.delete_one({"user_id": user_id})
        return result.deleted_count > 0

    def delete_all_user_data(self, user_id: str) -> Dict[str, int]:
        """Delete all user data from all collections"""
        results = {
            "profile_deleted": 0,
            "photos_deleted": 0,
            "prompts_deleted": 0,
            "user_deleted": 0,
            "chat_messages_deleted": 0,
            "personality_insights_deleted": 0
        }
        
        # Delete profile
        if self.delete_user_profile(user_id):
            results["profile_deleted"] = 1
        
        # Delete photos
        results["photos_deleted"] = self.delete_user_photos(user_id)
        
        # Delete prompts
        results["prompts_deleted"] = self.delete_user_prompts(user_id)
        
        # Delete chat messages
        results["chat_messages_deleted"] = self.delete_user_chat_messages(user_id)
        
        # Delete personality insights
        if self.delete_user_personality_insights(user_id):
            results["personality_insights_deleted"] = 1
        
        # Delete user (do this last)
        if self.delete_user(user_id):
            results["user_deleted"] = 1
        
        return results

# Global database instance
db_service = DatabaseService() 