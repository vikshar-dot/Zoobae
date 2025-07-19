from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
import os
import uuid
from datetime import datetime

from models import UserCreate, UserOut, UserProfile, ProfileUpdate, LoginResponse
from database import db_service

app = FastAPI()

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
    # For now, we'll just store the file info
    # In production, you'd upload to cloud storage (AWS S3, etc.)
    photo_id = str(uuid.uuid4())
    
    photo_data = {
        "id": photo_id,
        "url": f"https://storage.example.com/{photo_id}",  # Placeholder URL
        "caption": caption,
        "ai_suggestion": f"AI suggested caption for {file.filename}",
        "order": 0,  # Will be calculated based on existing photos
        "is_primary": False
    }
    
    db_service.add_photo(current_user["_id"], photo_data)
    return {"photo_id": photo_id, "url": photo_data["url"]}

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
    success = db_service.delete_photo(photo_id)
    if not success:
        raise HTTPException(status_code=404, detail="Photo not found")
    return {"message": "Photo deleted"}

@app.get("/")
def root():
    return {"message": "Dating app backend is running!"}

@app.on_event("shutdown")
def shutdown_event():
    db_service.close() 