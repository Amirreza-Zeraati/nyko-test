"""Questionnaire builder service.

Constructs the multi-page questionnaire from knowledge base components.
Orchestrates the flow of questions for the frontend.
"""

from typing import List, Dict, Any
from app.models.questionnaire import QuestionPage, Question
from app.knowledge_base.scales import ClinicalScales

class QuestionnaireBuilder:
    """
    Builds and organizes questionnaire pages.
    
    Structure:
    Page 1: Developmental History (Criterion B)
    Page 2: ASRS Part A (ADHD Screening)
    Page 3: ASRS Part B (Full ADHD Symptoms)
    Page 4: PHQ-9 (Depression Screening)
    Page 5: GAD-7 (Anxiety Screening)
    Page 6: Functional Impairment (Criterion C/D)
    """
    
    def __init__(self):
        self.scales = ClinicalScales()
        self.pages = self._build_pages()
    
    def _build_pages(self) -> Dict[int, QuestionPage]:
        """Construct all questionnaire pages."""
        pages = {}
        
        # Page 1: Developmental History
        dev_questions = [
            self._to_question_model(q) 
            for q in self.scales.get_developmental_history_questions()
        ]
        pages[1] = QuestionPage(
            page_number=1,
            title="Developmental History",
            description="ADHD is a developmental condition. These questions ask about your childhood experiences.",
            questions=dev_questions
        )
        
        # Page 2: ASRS Part A (Screening)
        asrs_questions = self.scales.get_asrs_questions()
        part_a = [self._scale_q_to_model(q) for q in asrs_questions if q.subscale == "Part A"]
        pages[2] = QuestionPage(
            page_number=2,
            title="Attention & Focus",
            description="These questions ask about common difficulties with attention and organization.",
            questions=part_a
        )
        
        # Page 3: ASRS Part B (Additional Symptoms)
        part_b = [self._scale_q_to_model(q) for q in asrs_questions if q.subscale == "Part B"]
        pages[3] = QuestionPage(
            page_number=3,
            title="Activity & Impulsivity",
            description="These questions ask about hyperactivity, restlessness, and impulsivity.",
            questions=part_b
        )
        
        # Page 4: PHQ-9 (Depression)
        phq9 = [self._scale_q_to_model(q) for q in self.scales.get_phq9_questions()]
        pages[4] = QuestionPage(
            page_number=4,
            title="Mood Assessment",
            description="Difficulties with focus can sometimes be related to mood. Please answer based on the last 2 weeks.",
            questions=phq9
        )
        
        # Page 5: GAD-7 (Anxiety)
        gad7 = [self._scale_q_to_model(q) for q in self.scales.get_gad7_questions()]
        pages[5] = QuestionPage(
            page_number=5,
            title="Anxiety Assessment",
            description="Anxiety can also affect concentration. Please answer based on the last 2 weeks.",
            questions=gad7
        )
        
        # Page 6: Functional Impairment
        impairment = [
            self._to_question_model(q) 
            for q in self.scales.get_functional_impairment_questions()
        ]
        pages[6] = QuestionPage(
            page_number=6,
            title="Impact on Daily Life",
            description="These questions help us understand how symptoms affect your daily functioning.",
            questions=impairment
        )
        
        # Page 7: Differential Diagnosis (Clinical Rules Specific)
        diff_diag = self._get_differential_diagnosis_questions()
        pages[7] = QuestionPage(
            page_number=7,
            title="Detailed Patterns",
            description="These final questions help distinguish between different causes of your symptoms.",
            questions=diff_diag
        )
        
        return pages
    
    def _to_question_model(self, data: Dict[str, Any]) -> Question:
        """Convert dictionary to Question model."""
        return Question(
            id=data["id"],
            text=data["text"],
            type=data.get("type", "likert"),
            options=data.get("options", []),
            required=True
        )

    def _scale_q_to_model(self, scale_q) -> Question:
        """Convert ScaleQuestion object to Question model."""
        return Question(
            id=scale_q.id,
            text=scale_q.text,
            type="likert",
            required=True
        )

    def _get_differential_diagnosis_questions(self) -> List[Question]:
        """Questions specifically for differential diagnosis logic."""
        return [
            Question(
                id="lifelong_symptoms",
                text="Have these difficulties been present for as long as you can remember (lifelong)?",
                type="likert",
                required=True
            ),
            Question(
                id="episodic_symptoms",
                text="Do your symptoms come and go in episodes (weeks or months of feeling bad, then feeling normal)?",
                type="likert",
                required=True
            ),
            Question(
                id="concentration_worse_when_sad",
                text="Is your concentration significantly worse ONLY when you are feeling down or depressed?",
                type="likert",
                required=True
            ),
            Question(
                id="mind_random_thoughts",
                text="When your mind wanders, does it jump to random, unrelated thoughts (e.g., 'squirrel!', 'did I leave the stove on?')?",
                type="likert",
                required=True
            ),
            Question(
                id="mind_full_of_worries",
                text="When your mind wanders, is it usually filled with specific worries about the future or bad things happening?",
                type="likert",
                required=True
            ),
            Question(
                id="restlessness",
                text="Does moving around or fidgeting make you feel better/calmer?",
                type="likert",
                required=True
            ),
            Question(
                id="physical_anxiety_symptoms",
                text="Do you often feel physical tension, racing heart, or 'butterflies' in your stomach?",
                type="likert",
                required=True
            )
        ]

    def get_page(self, page_number: int) -> QuestionPage:
        """Retrieve a specific page."""
        if page_number not in self.pages:
            raise ValueError(f"Page {page_number} does not exist")
        return self.pages[page_number]
    
    def get_total_pages(self) -> int:
        """Get total number of pages."""
        return len(self.pages)
