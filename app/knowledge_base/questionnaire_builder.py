"""Questionnaire builder service.

Constructs the multi-page questionnaire from knowledge base components.
Orchestrates the flow of questions for the frontend.
"""

from typing import List, Dict, Any
from app.models.questionnaire import QuestionPage, Question, QuestionType, QuestionCategory
from app.knowledge_base.scales import ClinicalScales

class QuestionnaireBuilder:
    """
    Builds and organizes questionnaire pages.
    """
    
    def __init__(self):
        self.scales = ClinicalScales()
        self.pages = self._build_pages()
    
    def _build_pages(self) -> Dict[int, QuestionPage]:
        """Construct all questionnaire pages."""
        pages = {}
        
        # Page 1: Developmental History
        dev_questions = [
            self._to_question_model(q, QuestionCategory.ADHD_CHILDHOOD) 
            for q in self.scales.get_developmental_history_questions()
        ]
        pages[1] = QuestionPage(
            page_number=1,
            title="Developmental History",
            description="ADHD is a developmental condition. These questions ask about your childhood experiences.",
            questions=dev_questions,
            progress_percentage=14
        )
        
        # Page 2: ASRS Part A (Screening)
        asrs_questions = self.scales.get_asrs_questions()
        part_a = [
            self._scale_q_to_model(q, QuestionCategory.ADHD_INATTENTION) 
            for q in asrs_questions if q.subscale == "Part A"
        ]
        pages[2] = QuestionPage(
            page_number=2,
            title="Attention & Focus",
            description="These questions ask about common difficulties with attention and organization.",
            questions=part_a,
            progress_percentage=28
        )
        
        # Page 3: ASRS Part B (Additional Symptoms)
        part_b = [
            self._scale_q_to_model(q, QuestionCategory.ADHD_HYPERACTIVITY) 
            for q in asrs_questions if q.subscale == "Part B"
        ]
        pages[3] = QuestionPage(
            page_number=3,
            title="Activity & Impulsivity",
            description="These questions ask about hyperactivity, restlessness, and impulsivity.",
            questions=part_b,
            progress_percentage=42
        )
        
        # Page 4: PHQ-9 (Depression)
        phq9 = [
            self._scale_q_to_model(q, QuestionCategory.DEPRESSION) 
            for q in self.scales.get_phq9_questions()
        ]
        pages[4] = QuestionPage(
            page_number=4,
            title="Mood Assessment",
            description="Difficulties with focus can sometimes be related to mood. Please answer based on the last 2 weeks.",
            questions=phq9,
            progress_percentage=57
        )
        
        # Page 5: GAD-7 (Anxiety)
        gad7 = [
            self._scale_q_to_model(q, QuestionCategory.ANXIETY) 
            for q in self.scales.get_gad7_questions()
        ]
        pages[5] = QuestionPage(
            page_number=5,
            title="Anxiety Assessment",
            description="Anxiety can also affect concentration. Please answer based on the last 2 weeks.",
            questions=gad7,
            progress_percentage=71
        )
        
        # Page 6: Functional Impairment
        impairment = [
            self._to_question_model(q, QuestionCategory.FUNCTIONAL_IMPAIRMENT) 
            for q in self.scales.get_functional_impairment_questions()
        ]
        pages[6] = QuestionPage(
            page_number=6,
            title="Impact on Daily Life",
            description="These questions help us understand how symptoms affect your daily functioning.",
            questions=impairment,
            progress_percentage=85
        )
        
        # Page 7: Differential Diagnosis
        diff_diag = self._get_differential_diagnosis_questions()
        pages[7] = QuestionPage(
            page_number=7,
            title="Detailed Patterns",
            description="These final questions help distinguish between different causes of your symptoms.",
            questions=diff_diag,
            progress_percentage=100
        )
        
        return pages
    
    def _to_question_model(self, data: Dict[str, Any], category: QuestionCategory) -> Question:
        """Convert dictionary to Question model."""
        q_type = data.get("type", "likert")
        model_type = QuestionType.LIKERT_SCALE
        
        if q_type == "numeric":
            model_type = QuestionType.TEXT  # Using TEXT for numeric input for simplicity in this version
        elif q_type == "boolean":
            model_type = QuestionType.YES_NO
            
        return Question(
            id=data["id"],
            category=category,
            question_type=model_type,
            text=data["text"],
            options=data.get("options", []),
            required=True
        )

    def _scale_q_to_model(self, scale_q, category: QuestionCategory) -> Question:
        """Convert ScaleQuestion object to Question model."""
        return Question(
            id=scale_q.id,
            category=category,
            question_type=QuestionType.LIKERT_SCALE,
            text=scale_q.text,
            required=True
        )

    def _get_differential_diagnosis_questions(self) -> List[Question]:
        """Questions specifically for differential diagnosis logic."""
        questions_data = [
            {
                "id": "lifelong_symptoms",
                "text": "Have these difficulties been present for as long as you can remember (lifelong)?",
                "category": QuestionCategory.ADHD_CHILDHOOD
            },
            {
                "id": "episodic_symptoms",
                "text": "Do your symptoms come and go in episodes (weeks or months of feeling bad, then feeling normal)?",
                "category": QuestionCategory.DEPRESSION
            },
            {
                "id": "concentration_worse_when_sad",
                "text": "Is your concentration significantly worse ONLY when you are feeling down or depressed?",
                "category": QuestionCategory.DEPRESSION
            },
            {
                "id": "mind_random_thoughts",
                "text": "When your mind wanders, does it jump to random, unrelated thoughts (e.g., 'squirrel!', 'did I leave the stove on?')?",
                "category": QuestionCategory.ADHD_INATTENTION
            },
            {
                "id": "mind_full_of_worries",
                "text": "When your mind wanders, is it usually filled with specific worries about the future or bad things happening?",
                "category": QuestionCategory.ANXIETY
            },
            {
                "id": "restlessness",
                "text": "Does moving around or fidgeting make you feel better/calmer?",
                "category": QuestionCategory.ADHD_HYPERACTIVITY
            },
            {
                "id": "physical_anxiety_symptoms",
                "text": "Do you often feel physical tension, racing heart, or 'butterflies' in your stomach?",
                "category": QuestionCategory.ANXIETY
            }
        ]
        
        return [
            Question(
                id=q["id"],
                category=q["category"],
                question_type=QuestionType.LIKERT_SCALE,
                text=q["text"],
                required=True
            )
            for q in questions_data
        ]

    def get_page(self, page_number: int) -> QuestionPage:
        """Retrieve a specific page."""
        if page_number not in self.pages:
            raise ValueError(f"Page {page_number} does not exist")
        return self.pages[page_number]
    
    def get_total_pages(self) -> int:
        """Get total number of pages."""
        return len(self.pages)
