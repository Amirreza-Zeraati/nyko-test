"""Evaluation result models."""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from enum import Enum

class DiagnosticCategory(str, Enum):
    """Primary diagnostic categories."""
    ADHD_PREDOMINANTLY_INATTENTIVE = "adhd_predominantly_inattentive"
    ADHD_PREDOMINANTLY_HYPERACTIVE = "adhd_predominantly_hyperactive"
    ADHD_COMBINED = "adhd_combined"
    DEPRESSION_PRIMARY = "depression_primary"
    ANXIETY_PRIMARY = "anxiety_primary"
    COMORBID_ADHD_DEPRESSION = "comorbid_adhd_depression"
    COMORBID_ADHD_ANXIETY = "comorbid_adhd_anxiety"
    COMPLEX_COMORBIDITY = "complex_comorbidity"
    SUBCLINICAL = "subclinical"
    INCONCLUSIVE = "inconclusive"

class ConfidenceLevel(str, Enum):
    """Confidence in diagnostic assessment."""
    HIGH = "high"
    MODERATE = "moderate"
    LOW = "low"
    VERY_LOW = "very_low"

class DiagnosticProfile(BaseModel):
    """Individual diagnostic profile with probability."""
    category: DiagnosticCategory
    probability: float = Field(..., ge=0.0, le=1.0)
    confidence: ConfidenceLevel
    supporting_evidence: List[str]
    contradicting_evidence: List[str]

class ClinicalReasoning(BaseModel):
    """Expert system reasoning explanation."""
    primary_pattern: str
    differential_considerations: List[str]
    key_discriminating_features: List[str]
    developmental_context: Optional[str] = None
    chronicity_analysis: Optional[str] = None
    functional_impact: Optional[str] = None
    red_flags: List[str] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)

class ScaleScores(BaseModel):
    """Validated scale scores."""
    asrs_total: Optional[float] = None
    asrs_part_a: Optional[float] = None
    asrs_interpretation: Optional[str] = None
    phq9_total: Optional[float] = None
    phq9_severity: Optional[str] = None
    gad7_total: Optional[float] = None
    gad7_severity: Optional[str] = None

class EvaluationResult(BaseModel):
    """Complete evaluation result."""
    session_id: str
    primary_diagnosis: DiagnosticProfile
    differential_diagnoses: List[DiagnosticProfile]
    clinical_reasoning: ClinicalReasoning
    scale_scores: ScaleScores
    recommendations: List[str]
    disclaimer: str
    timestamp: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "abc123",
                "primary_diagnosis": {
                    "category": "adhd_combined",
                    "probability": 0.78,
                    "confidence": "moderate",
                    "supporting_evidence": ["Childhood onset symptoms"],
                    "contradicting_evidence": []
                }
            }
        }
