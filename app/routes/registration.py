"""User registration route."""

from fastapi import APIRouter, HTTPException
import uuid
from datetime import datetime

from app.models.user_models import UserInfo, SessionData
from app.services.session_manager import SessionManager

router = APIRouter()
session_manager = SessionManager()

@router.post("/registration/start")
async def register_user(user_info: UserInfo):
    """Register a new user and create a session."""
    try:
        # Generate unique session ID
        session_id = str(uuid.uuid4())
        
        # Create session data
        session_data = SessionData(
            session_id=session_id,
            user_info=user_info,
            current_page=0,
            responses={},
            completed=False,
            created_at=datetime.utcnow().isoformat()
        )
        
        # Store session
        await session_manager.save_session(session_id, session_data)
        
        return {
            "success": True,
            "session_id": session_id,
            "message": "Registration successful"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Registration failed: {str(e)}"
        )
