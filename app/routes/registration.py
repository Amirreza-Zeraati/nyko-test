"""User registration route."""

from fastapi import APIRouter, HTTPException, Request
from fastapi.templating import Jinja2Templates
import uuid

from app.models.user_models import UserInfo, SessionData
from app.services.session_manager import SessionManager

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
session_manager = SessionManager()

@router.get("/register")
async def get_registration_page(request: Request):
    """Render registration form."""
    return templates.TemplateResponse(
        "registration.html",
        {"request": request}
    )

@router.post("/register")
async def register_user(user_info: UserInfo):
    """
    Register a new user and create a session.
    
    This endpoint:
    1. Validates user information
    2. Creates a unique session ID
    3. Initializes session data
    4. Returns session ID for tracking
    """
    try:
        # Generate unique session ID
        session_id = str(uuid.uuid4())
        
        # Create session data
        session_data = SessionData(
            session_id=session_id,
            user_info=user_info,
            current_page=0
        )
        
        # Store session
        await session_manager.save_session(session_id, session_data)
        
        return {
            "success": True,
            "session_id": session_id,
            "message": "Registration successful",
            "next_step": "/api/questionnaire/page/1"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Registration failed: {str(e)}"
        )
