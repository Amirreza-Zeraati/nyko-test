"""Questionnaire flow routes."""

from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Any
import logging

from app.models.questionnaire import QuestionPage
from app.services.session_manager import session_manager
from app.knowledge_base.questionnaire_builder import QuestionnaireBuilder

logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize questionnaire builder with error handling
try:
    questionnaire_builder = QuestionnaireBuilder()
    logger.info(f"QuestionnaireBuilder initialized with {questionnaire_builder.get_total_pages()} pages")
except Exception as e:
    logger.error(f"Failed to initialize QuestionnaireBuilder: {e}")
    raise

@router.get("/questionnaire/page/{page_number}", response_model=QuestionPage)
async def get_questionnaire_page(
    page_number: int,
    session_id: str = Query(...)
):
    """Get a specific page of the questionnaire."""
    logger.info(f"Loading page {page_number} for session {session_id}")
    
    # Validate session
    try:
        session_data = session_manager.get_session(session_id)
        if not session_data:
            logger.warning(f"Session not found: {session_id}")
            raise HTTPException(status_code=404, detail="Session not found. Please restart.")
        
        logger.info(f"Session found: {session_data.session_id}")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving session: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Session error: {str(e)}")
    
    # Get page content
    try:
        page = questionnaire_builder.get_page(page_number)
        logger.info(f"Page {page_number} loaded successfully with {len(page.questions)} questions")
        
        # Update session current page
        session_data.current_page = page_number
        session_manager.save_session(session_id, session_data)
        
        return page
        
    except ValueError as e:
        logger.error(f"Invalid page number {page_number}: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error loading page {page_number}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error loading page: {str(e)}")

@router.post("/questionnaire/submit")
async def submit_questionnaire(
    session_id: str = Query(...),
    responses: Dict[str, Any] = None
):
    """Submit all questionnaire responses."""
    logger.info(f"Submitting questionnaire for session {session_id}")
    
    if responses is None:
        responses = {}
    
    # Validate session
    session_data = session_manager.get_session(session_id)
    if not session_data:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Store all responses
    session_data.responses.update(responses)
    session_data.completed = True
    session_manager.save_session(session_id, session_data)
    
    logger.info(f"Questionnaire completed for session {session_id}")
    
    return {
        "success": True,
        "message": "Questionnaire completed"
    }

@router.get("/questionnaire/progress")
async def get_progress(session_id: str = Query(...)):
    """Get questionnaire completion progress."""
    session_data = session_manager.get_session(session_id)
    if not session_data:
        raise HTTPException(status_code=404, detail="Session not found")
    
    total_pages = questionnaire_builder.get_total_pages()
    
    return {
        "current_page": session_data.current_page,
        "total_pages": total_pages,
        "progress_percentage": (session_data.current_page / total_pages) * 100,
        "completed": session_data.completed
    }
