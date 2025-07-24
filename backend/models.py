from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class VerificationStatus(str, Enum):
    UNVERIFIED = "unverified"
    VERIFIED = "verified"
    SUPER_VERIFIED = "super-verified"

class Photo(BaseModel):
    id: str
    url: str
    caption: str
    ai_suggestion: str
    order: int
    is_primary: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)

class EssentialDetail(BaseModel):
    key: str  # "age", "height", "home", "drinker", "kids"
    value: str
    is_visible: bool = True

class Prompt(BaseModel):
    question: str
    answer: str
    order: int

class UserProfile(BaseModel):
    user_id: Optional[str] = None
    name: str
    pronouns: str
    verification_status: VerificationStatus = VerificationStatus.UNVERIFIED
    essential_details: List[EssentialDetail]
    prompts: List[Prompt]
    photos: List[Photo]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ProfileUpdate(BaseModel):
    name: Optional[str] = None
    pronouns: Optional[str] = None
    essential_details: Optional[List[EssentialDetail]] = None
    prompts: Optional[List[Prompt]] = None
    photos: Optional[List[Photo]] = None

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: str
    email: EmailStr
    profile: Optional[UserProfile] = None

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserOut

class ChatMessage(BaseModel):
    message: str
    user_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class PersonalityInsight(BaseModel):
    mbti_type: Optional[str] = None
    attachment_style: Optional[str] = None
    personality_traits: List[str] = []
    values: List[str] = []
    interests: List[str] = []
    relationship_goals: Optional[str] = None
    communication_style: Optional[str] = None
    boundaries: List[str] = []
    immediate_needs: List[str] = []

class AIResponse(BaseModel):
    message: str
    personality_insights: Optional[PersonalityInsight] = None
    follow_up_questions: List[str] = []
    conversation_context: Dict[str, Any] = {} 