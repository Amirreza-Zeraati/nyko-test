"""User registration route."""

from fastapi import APIRouter, HTTPException
import uuid
from datetime import datetime
import logging

from app.models.user_models import UserInfo, SessionData
from app.services.session_manager import session_manager

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/registration/start")
async def register_user(user_info: UserInfo):
    """Register a new user and create a session."""
    try:
        # Generate unique session ID
        session_id = str(uuid.uuid4())
        logger.info(f"Creating new session: {session_id}")
        
        # Create session data
        session_data = SessionData(
            session_id=session_id,
            user_info=user_info,
            current_page=0,
            responses={},
            completed=False,
            created_at=datetime.utcnow().isoformat(),
            started_at=datetime.utcnow(),
            last_activity=datetime.utcnow()
        )
        
        # Store session (no await - synchronous now)
        session_manager.save_session(session_id, session_data)
        logger.info(f"Session {session_id} created successfully")
        
        return {
            "success": True,
            "session_id": session_id,
            "message": "Registration successful"
        }
        
    except Exception as e:
        logger.error(f"Registration failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Registration failed: {str(e)}"
        )
