"""Evaluation and result generation routes."""

from fastapi import APIRouter, HTTPException, Request
from fastapi.templating import Jinja2Templates
from datetime import datetime

from app.services.session_manager import SessionManager
from app.services.expert_system import ExpertSystem
from app.services.scoring import ScoringService
from app.models.results import EvaluationResult

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
session_manager = SessionManager()
expert_system = ExpertSystem()
scoring_service = ScoringService()

@router.get("/evaluation/result")
async def get_result_page(session_id: str, request: Request):
    """Render result viewing page."""
    # Validate session
    session_data = await session_manager.get_session(session_id)
    if not session_data:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if not session_data.completed:
        raise HTTPException(
            status_code=400,
            detail="Questionnaire not completed"
        )
    
    return templates.TemplateResponse(
        "result.html",
        {"request": request, "session_id": session_id}
    )

@router.post("/evaluation/analyze")
async def analyze_responses(session_id: str) -> EvaluationResult:
    """
    Perform expert system evaluation of user responses.
    
    This endpoint:
    1. Retrieves all user responses from session
    2. Calculates validated scale scores (ASRS, PHQ-9, GAD-7)
    3. Applies expert clinical reasoning rules
    4. Performs differential diagnosis
    5. Generates clinical reasoning explanation
    6. Provides recommendations
    
    The expert system uses:
    - DSM-5-TR diagnostic criteria
    - Clinical heuristics from experienced practitioners
    - Pattern matching against known diagnostic profiles
    - Contextual and developmental analysis
    """
    # Validate session
    session_data = await session_manager.get_session(session_id)
    if not session_data:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if not session_data.completed:
        raise HTTPException(
            status_code=400,
            detail="Questionnaire not completed"
        )
    
    try:
        # Calculate scale scores
        scale_scores = scoring_service.calculate_all_scores(
            session_data.responses
        )
        
        # Run expert system evaluation
        result = expert_system.evaluate(
            responses=session_data.responses,
            scale_scores=scale_scores,
            user_info=session_data.user_info
        )
        
        # Add metadata
        result.session_id = session_id
        result.timestamp = datetime.utcnow().isoformat()
        
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Evaluation failed: {str(e)}"
        )

@router.get("/evaluation/pdf/{session_id}")
async def generate_pdf_report(session_id: str):
    """
    Generate a PDF report of the evaluation (future enhancement).
    """
    raise HTTPException(
        status_code=501,
        detail="PDF generation not yet implemented"
    )
