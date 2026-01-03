"""Questionnaire data structures."""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum

class QuestionType(str, Enum):
    """Question types."""
    SINGLE_CHOICE = "single_choice"
    MULTIPLE_CHOICE = "multiple_choice"
    LIKERT_SCALE = "likert_scale"
    TEXT = "text"
    YES_NO = "yes_no"

class QuestionCategory(str, Enum):
    """Clinical domains."""
    ADHD_INATTENTION = "adhd_inattention"
    ADHD_HYPERACTIVITY = "adhd_hyperactivity"
    ADHD_CHILDHOOD = "adhd_childhood"
    DEPRESSION = "depression"
    ANXIETY = "anxiety"
    EXECUTIVE_FUNCTION = "executive_function"
    CONTEXTUAL = "contextual"
    FUNCTIONAL_IMPAIRMENT = "functional_impairment"

class Question(BaseModel):
    """Individual question structure."""
    id: str
    category: QuestionCategory
    question_type: QuestionType
    text: str
    description: Optional[str] = None
    options: Optional[List[str]] = None
    scale_min: Optional[int] = None
    scale_max: Optional[int] = None
    scale_labels: Optional[Dict[int, str]] = None
    required: bool = True
    clinical_weight: float = 1.0  # Expert-assigned importance

class QuestionnaireResponse(BaseModel):
    """User response to questionnaire."""
    question_id: str
    answer: Any
    page_number: int

class QuestionPage(BaseModel):
    """A page of questions in the multi-page flow."""
    page_number: int
    title: str
    description: Optional[str] = None
    questions: List[Question]
    progress_percentage: int
