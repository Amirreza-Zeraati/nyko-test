"""User data models."""

from pydantic import BaseModel, Field, field_validator
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum

class Gender(str, Enum):
    """Gender options."""
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    PREFER_NOT_TO_SAY = "prefer_not_to_say"

class UserInfo(BaseModel):
    """User registration information."""
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    age: int = Field(..., ge=13, le=100)  # Adolescents and adults
    gender: Optional[Gender] = None
    email: Optional[str] = Field(None, pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    
    @field_validator('first_name', 'last_name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate name fields."""
        if not v.strip():
            raise ValueError("Name cannot be empty")
        return v.strip()

class SessionData(BaseModel):
    """User session data stored across questionnaire flow."""
    session_id: str
    user_info: Optional[UserInfo] = None
    responses: Dict[str, Any] = Field(default_factory=dict)
    current_page: int = 0
    created_at: Optional[str] = None
    started_at: Optional[datetime] = None
    last_activity: Optional[datetime] = None
    completed: bool = False
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
