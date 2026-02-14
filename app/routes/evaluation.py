"""Evaluation and result generation routes."""

from fastapi import APIRouter, HTTPException, Query
from datetime import datetime
import logging

from app.services.session_manager import session_manager
from app.services.expert_system import ExpertSystem
from app.services.scoring import ScoringService
from app.models.results import EvaluationResult

logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize services
try:
    expert_system = ExpertSystem()
    scoring_service = ScoringService()
    logger.info("Expert system and scoring service initialized")
except Exception as e:
    logger.error(f"Failed to initialize evaluation services: {e}", exc_info=True)
    raise

@router.post("/evaluation/analyze")
async def analyze_responses(session_id: str = Query(...)) -> EvaluationResult:
    """
    Perform expert system evaluation of user responses.
    
    This endpoint:
    1. Retrieves all user responses from session
    2. Calculates validated scale scores (ASRS, PHQ-9, GAD-7)
    3. Applies expert clinical reasoning rules
    4. Performs differential diagnosis
    5. Generates clinical reasoning explanation
    6. Provides recommendations
    """
    logger.info(f"Starting analysis for session {session_id}")
    
    # Validate session
    try:
        session_data = session_manager.get_session(session_id)
        if not session_data:
            logger.warning(f"Session not found: {session_id}")
            raise HTTPException(status_code=404, detail="Session not found")
        
        logger.info(f"Session found with {len(session_data.responses)} responses")
        
        if not session_data.completed:
            logger.warning(f"Questionnaire not completed for session {session_id}")
            raise HTTPException(
                status_code=400,
                detail="Questionnaire not completed"
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving session: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Session error: {str(e)}")
    
    try:
        # Calculate scale scores
        logger.info("Calculating scale scores")
        scale_scores = scoring_service.calculate_all_scores(
            session_data.responses
        )
        logger.info(f"Scale scores calculated: ASRS={scale_scores.asrs_part_a}, PHQ9={scale_scores.phq9_total}, GAD7={scale_scores.gad7_total}")
        
        # Run expert system evaluation
        logger.info("Running expert system evaluation")
        user_info_dict = session_data.user_info.model_dump() if session_data.user_info else {}
        
        result = expert_system.evaluate(
            responses=session_data.responses,
            scale_scores=scale_scores,
            user_info=user_info_dict
        )
        logger.info(f"Evaluation complete: Pattern={result.primary_pattern}")
        
        # Add metadata
        result.session_id = session_id
        result.timestamp = datetime.utcnow().isoformat()
        
        return result
        
    except Exception as e:
        logger.error(f"Evaluation failed for session {session_id}: {e}", exc_info=True)
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
