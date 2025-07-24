from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from passlib.context import CryptContext
import os
import uuid
import shutil
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from models import UserCreate, UserOut, UserProfile, ProfileUpdate, LoginResponse, ChatMessage, AIResponse, PersonalityInsight
from pydantic import BaseModel
from database import db_service
from llm_service import llm_service
from simple_llm_service import simple_llm_service

# Simple test message model
class TestChatMessage(BaseModel):
    message: str
    user_context: Optional[dict] = None

app = FastAPI()

# Create uploads directory if it doesn't exist
UPLOADS_DIR = Path("uploads")
UPLOADS_DIR.mkdir(exist_ok=True)

# Mount static files for serving uploaded images
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Authentication helper
def get_current_user(token: str = Depends(oauth2_scheme)):
    user = db_service.get_user_by_email(token)  # Using email as token for now
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user

@app.post("/register", response_model=UserOut)
def register(user: UserCreate):
    try:
        hashed_password = pwd_context.hash(user.password)
        user_id = db_service.create_user(user.email, hashed_password)
        return {"id": user_id, "email": user.email, "profile": None}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/login", response_model=LoginResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = db_service.get_user_by_email(form_data.username)
    if not user or not pwd_context.verify(form_data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Get user profile
    profile = db_service.get_profile(user["_id"])
    
    return {
        "access_token": user["email"],
        "token_type": "bearer",
        "user": {
            "id": user["_id"],
            "email": user["email"],
            "profile": profile
        }
    }

@app.get("/profile", response_model=UserProfile)
def get_profile(current_user: dict = Depends(get_current_user)):
    profile = db_service.get_profile(current_user["_id"])
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@app.post("/profile", response_model=UserProfile)
def create_profile(profile_data: UserProfile, current_user: dict = Depends(get_current_user)):
    # Check if profile already exists
    existing_profile = db_service.get_profile(current_user["_id"])
    if existing_profile:
        raise HTTPException(status_code=400, detail="Profile already exists")
    
    # Set the user_id in the profile data
    profile_dict = profile_data.dict()
    profile_dict["user_id"] = current_user["_id"]
    
    profile_id = db_service.create_profile(current_user["_id"], profile_dict)
    created_profile = db_service.get_profile(current_user["_id"])
    return created_profile

@app.put("/profile", response_model=UserProfile)
def update_profile(update_data: ProfileUpdate, current_user: dict = Depends(get_current_user)):
    # Remove None values
    update_dict = {k: v for k, v in update_data.dict().items() if v is not None}
    
    if not update_dict:
        raise HTTPException(status_code=400, detail="No valid fields to update")
    
    success = db_service.update_profile(current_user["_id"], update_dict)
    if not success:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    return db_service.get_profile(current_user["_id"])

@app.post("/profile/photos")
def upload_photo(
    file: UploadFile = File(...),
    caption: str = "",
    current_user: dict = Depends(get_current_user)
):
    # Generate unique filename
    file_extension = Path(file.filename).suffix if file.filename else ".jpg"
    photo_id = str(uuid.uuid4())
    filename = f"{photo_id}{file_extension}"
    file_path = UPLOADS_DIR / filename
    
    # Save file locally
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
    
    # Generate URL for the uploaded file
    photo_url = f"http://192.168.1.8:8001/uploads/{filename}"
    
    photo_data = {
        "id": photo_id,
        "url": photo_url,
        "caption": caption,
        "ai_suggestion": f"AI suggested caption for {file.filename}",
        "order": 0,  # Will be calculated based on existing photos
        "is_primary": False
    }
    
    db_service.add_photo(current_user["_id"], photo_data)
    return {"photo_id": photo_id, "url": photo_url}

@app.get("/profile/photos")
def get_photos(current_user: dict = Depends(get_current_user)):
    photos = db_service.get_user_photos(current_user["_id"])
    return {"photos": photos}

@app.put("/profile/photos/{photo_id}")
def update_photo_caption(
    photo_id: str,
    caption: str,
    current_user: dict = Depends(get_current_user)
):
    success = db_service.update_photo(photo_id, {"caption": caption})
    if not success:
        raise HTTPException(status_code=404, detail="Photo not found")
    return {"message": "Photo caption updated"}

@app.delete("/profile/photos/{photo_id}")
def delete_photo(photo_id: str, current_user: dict = Depends(get_current_user)):
    print(f"Attempting to delete photo with ID: {photo_id}")
    print(f"User ID: {current_user['_id']}")
    
    # Check if photo exists and belongs to user
    photos = db_service.get_user_photos(current_user["_id"])
    photo_ids = [photo.get("_id") for photo in photos]
    print(f"User's photo IDs: {photo_ids}")
    
    success = db_service.delete_photo(photo_id)
    if not success:
        raise HTTPException(status_code=404, detail="Photo not found")
    return {"message": "Photo deleted"}

@app.get("/admin/update-photo-urls")
def update_photo_urls():
    """Update existing photo URLs to use localhost (admin endpoint)"""
    try:
        db_service.update_photo_urls_to_localhost()
        return {"message": "Photo URLs updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update photo URLs: {str(e)}")

@app.post("/chat/ai", response_model=AIResponse)
def chat_with_ai(
    chat_message: ChatMessage,
    current_user: dict = Depends(get_current_user)
):
    """
    Chat with AI using RAG-based LLM to gather personality insights and relationship preferences
    """
    try:
        # Get user's chat history for context
        chat_history = db_service.get_user_chat_history(current_user["_id"])
        
        # Get user's profile for additional context
        user_profile = db_service.get_profile(current_user["_id"])
        user_context = {
            "user_id": current_user["_id"],
            "email": current_user["email"],
            "has_profile": user_profile is not None,
            "profile_name": user_profile.get("name") if user_profile else None,
            "conversation_count": len(chat_history)
        }

        # Use Gemini LLM service
        if llm_service is not None:
            ai_response = llm_service.generate_response(
                user_message=chat_message.message,
                conversation_history=chat_history,
                user_context=user_context
            )
        else:
            raise HTTPException(status_code=500, detail="Gemini AI service not available. Please check your API key and package installation.")
        
        # Save the user message to chat history
        db_service.save_chat_message(
            user_id=current_user["_id"],
            message=chat_message.message,
            sender="user"
        )
        
        # Save the AI response to chat history
        db_service.save_chat_message(
            user_id=current_user["_id"],
            message=ai_response["message"],
            sender="ai",
            insights=ai_response.get("personality_insights", {})
        )
        
        # Update personality insights if new ones are found
        if ai_response.get("personality_insights"):
            db_service.save_personality_insights(
                user_id=current_user["_id"],
                insights=ai_response["personality_insights"]
            )
        
        return AIResponse(
            message=ai_response["message"],
            personality_insights=ai_response.get("personality_insights"),
            follow_up_questions=ai_response.get("follow_up_questions", []),
            conversation_context=ai_response.get("conversation_context", {})
        )
        
    except Exception as e:
        print(f"AI chat error: {e}")
        raise HTTPException(status_code=500, detail=f"AI chat error: {str(e)}")

@app.get("/chat/history")
def get_chat_history(current_user: dict = Depends(get_current_user)):
    """
    Get user's chat history with AI
    """
    try:
        history = db_service.get_user_chat_history(current_user["_id"])
        return {"chat_history": history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get chat history: {str(e)}")

@app.get("/chat/personality-summary")
def get_personality_summary(current_user: dict = Depends(get_current_user)):
    """
    Get comprehensive personality summary from chat history
    """
    try:
        chat_history = db_service.get_user_chat_history(current_user["_id"])
        if not chat_history:
            raise HTTPException(status_code=404, detail="No chat history found")
        
        summary = llm_service.analyze_conversation_summary(chat_history)
        return {"personality_summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate personality summary: {str(e)}")

@app.get("/")
def root():
    return {"message": "Dating app backend is running!"}

@app.post("/chat/ai/test", response_model=AIResponse)
def chat_with_ai_test(chat_message: TestChatMessage):
    """
    Test endpoint for AI chat without authentication
    """
    try:
        # Prepare user context
        user_context = {
            "user_id": "test_user", 
            "conversation_count": 0
        }
        
        # Add user profile data if provided
        if chat_message.user_context:
            user_context.update(chat_message.user_context)
        
        # Use Gemini LLM service
        if llm_service is not None:
            ai_response = llm_service.generate_response(
                user_message=chat_message.message,
                conversation_history=[],
                user_context=user_context
            )
            return AIResponse(**ai_response)
        else:
            raise HTTPException(status_code=500, detail="Gemini AI service not available. Please check your API key and package installation.")
        
    except Exception as e:
        print(f"Error in AI chat test: {e}")
        raise HTTPException(status_code=500, detail=f"AI chat error: {str(e)}")

@app.on_event("shutdown")
def shutdown_event():
    db_service.close() 