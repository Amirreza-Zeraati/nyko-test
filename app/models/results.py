"""Evaluation result models."""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from enum import Enum

class ScaleScores(BaseModel):
    """Validated scale scores."""
    asrs_total: Optional[float] = None
    asrs_part_a: Optional[float] = None
    asrs_interpretation: Optional[str] = None
    phq9_total: Optional[float] = None
    phq9_severity: Optional[str] = None
    gad7_total: Optional[float] = None
    gad7_severity: Optional[str] = None

class DiagnosticLikelihood(BaseModel):
    """Probabilistic assessment for a specific condition."""
    likelihood: float
    confidence: str
    key_factors: List[str]
    clinical_interpretation: str

class ClinicalRecommendation(BaseModel):
    """Actionable clinical recommendation."""
    priority: str
    category: str
    title: str
    description: str
    rationale: str

class EvaluationResult(BaseModel):
    """Complete evaluation result matching ExpertSystem output."""
    scale_scores: ScaleScores
    adhd_likelihood: DiagnosticLikelihood
    depression_likelihood: DiagnosticLikelihood
    anxiety_likelihood: DiagnosticLikelihood
    primary_pattern: str
    pattern_description: str
    clinical_reasoning: str
    recommendations: List[ClinicalRecommendation]
    disclaimer: str
    session_id: Optional[str] = None
    timestamp: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "primary_pattern": "adhd_predominant",
                "pattern_description": "Symptoms consistent with ADHD",
                "recommendations": []
            }
        }
