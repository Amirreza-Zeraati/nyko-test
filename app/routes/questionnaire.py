"""Questionnaire flow routes."""

from fastapi import APIRouter, HTTPException, Request, Body
from fastapi.templating import Jinja2Templates
from typing import Dict, Any

from app.models.questionnaire import QuestionnaireResponse, QuestionPage
from app.services.session_manager import SessionManager
from app.knowledge_base.questionnaire_builder import QuestionnaireBuilder

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
session_manager = SessionManager()
questionnaire_builder = QuestionnaireBuilder()

@router.get("/questionnaire/page/{page_number}")
async def get_questionnaire_page(
    page_number: int,
    session_id: str,
    request: Request
) -> QuestionPage:
    """
    Get a specific page of the questionnaire.
    
    The questionnaire is divided into multiple pages:
    - Page 1: Childhood/developmental history (ADHD onset)
    - Page 2: Current inattention symptoms (ADHD/Depression overlap)
    - Page 3: Hyperactivity/impulsivity symptoms (ADHD specific)
    - Page 4: Mood symptoms (Depression screening)
    - Page 5: Anxiety symptoms (Anxiety screening)
    - Page 6: Executive function and contextual factors
    - Page 7: Functional impairment assessment
    """
    # Validate session
    session_data = await session_manager.get_session(session_id)
    if not session_data:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Get page content
    try:
        page = questionnaire_builder.get_page(page_number)
        
        # Update session current page
        session_data.current_page = page_number
        await session_manager.save_session(session_id, session_data)
        
        return page
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/questionnaire/page/{page_number}")
async def submit_page_responses(
    page_number: int,
    session_id: str,
    responses: Dict[str, Any] = Body(...)
):
    """
    Submit responses for a questionnaire page.
    
    Responses are stored in the session for later evaluation.
    Each question_id maps to the user's answer.
    """
    # Validate session
    session_data = await session_manager.get_session(session_id)
    if not session_data:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Store responses
    for question_id, answer in responses.items():
        session_data.responses[question_id] = answer
    
    session_data.current_page = page_number
    await session_manager.save_session(session_id, session_data)
    
    # Determine next step
    total_pages = questionnaire_builder.get_total_pages()
    
    if page_number < total_pages:
        return {
            "success": True,
            "next_page": page_number + 1,
            "progress": (page_number / total_pages) * 100
        }
    else:
        # Mark as completed
        session_data.completed = True
        await session_manager.save_session(session_id, session_data)
        
        return {
            "success": True,
            "completed": True,
            "next_step": "/api/evaluation/result"
        }

@router.get("/questionnaire/progress/{session_id}")
async def get_progress(session_id: str):
    """Get questionnaire completion progress."""
    session_data = await session_manager.get_session(session_id)
    if not session_data:
        raise HTTPException(status_code=404, detail="Session not found")
    
    total_pages = questionnaire_builder.get_total_pages()
    
    return {
        "current_page": session_data.current_page,
        "total_pages": total_pages,
        "progress_percentage": (session_data.current_page / total_pages) * 100,
        "completed": session_data.completed
    }
