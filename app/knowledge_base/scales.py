"""Validated clinical assessment scales and instruments.

This module defines the structure and interpretation of:
- ASRS v1.1 (Adult ADHD Self-Report Scale)
- DIVA-5 (Diagnostic Interview for ADHD in adults)
- PHQ-9 (Depression screening)
- GAD-7 (Anxiety screening)
"""

from typing import Dict, List, Any
from dataclasses import dataclass

@dataclass
class ScaleQuestion:
    """Represents a single question in a validated scale."""
    id: str
    text: str
    scale_name: str
    subscale: str = ""
    reverse_scored: bool = False
    
class ClinicalScales:
    """
    Validated clinical assessment scales for ADHD screening.
    
    These scales are standardized instruments with established
    psychometric properties (reliability, validity, sensitivity, specificity).
    """
    
    @staticmethod
    def get_asrs_questions() -> List[ScaleQuestion]:
        """
        ASRS v1.1 (Adult ADHD Self-Report Scale).
        
        Developed by WHO and validated in multiple studies.
        18 questions based directly on DSM criteria.
        
        Part A (questions 1-6): Screening - highly predictive
        Part B (questions 7-18): Full symptom assessment
        
        Response scale: 0=Never, 1=Rarely, 2=Sometimes, 3=Often, 4=Very Often
        
        Reference:
        Kessler RC, et al. (2005). The World Health Organization Adult ADHD
        Self-Report Scale (ASRS). Psychological Medicine, 35(2), 245-256.
        """
        part_a = [
            ScaleQuestion(
                id="asrs_1",
                text="How often do you have trouble wrapping up the final details of a project, once the challenging parts have been done?",
                scale_name="ASRS",
                subscale="Part A"
            ),
            ScaleQuestion(
                id="asrs_2",
                text="How often do you have difficulty getting things in order when you have to do a task that requires organization?",
                scale_name="ASRS",
                subscale="Part A"
            ),
            ScaleQuestion(
                id="asrs_3",
                text="How often do you have problems remembering appointments or obligations?",
                scale_name="ASRS",
                subscale="Part A"
            ),
            ScaleQuestion(
                id="asrs_4",
                text="When you have a task that requires a lot of thought, how often do you avoid or delay getting started?",
                scale_name="ASRS",
                subscale="Part A"
            ),
            ScaleQuestion(
                id="asrs_5",
                text="How often do you fidget or squirm with your hands or feet when you have to sit down for a long time?",
                scale_name="ASRS",
                subscale="Part A"
            ),
            ScaleQuestion(
                id="asrs_6",
                text="How often do you feel overly active and compelled to do things, like you were driven by a motor?",
                scale_name="ASRS",
                subscale="Part A"
            ),
        ]
        
        part_b = [
            ScaleQuestion(
                id="asrs_7",
                text="How often do you make careless mistakes when you have to work on a boring or difficult project?",
                scale_name="ASRS",
                subscale="Part B"
            ),
            ScaleQuestion(
                id="asrs_8",
                text="How often do you have difficulty keeping your attention when you are doing boring or repetitive work?",
                scale_name="ASRS",
                subscale="Part B"
            ),
            ScaleQuestion(
                id="asrs_9",
                text="How often do you have difficulty concentrating on what people say to you, even when they are speaking to you directly?",
                scale_name="ASRS",
                subscale="Part B"
            ),
            ScaleQuestion(
                id="asrs_10",
                text="How often do you misplace or have difficulty finding things at home or at work?",
                scale_name="ASRS",
                subscale="Part B"
            ),
            ScaleQuestion(
                id="asrs_11",
                text="How often are you distracted by activity or noise around you?",
                scale_name="ASRS",
                subscale="Part B"
            ),
            ScaleQuestion(
                id="asrs_12",
                text="How often do you leave your seat in meetings or other situations in which you are expected to remain seated?",
                scale_name="ASRS",
                subscale="Part B"
            ),
            ScaleQuestion(
                id="asrs_13",
                text="How often do you feel restless or fidgety?",
                scale_name="ASRS",
                subscale="Part B"
            ),
            ScaleQuestion(
                id="asrs_14",
                text="How often do you have difficulty unwinding and relaxing when you have time to yourself?",
                scale_name="ASRS",
                subscale="Part B"
            ),
            ScaleQuestion(
                id="asrs_15",
                text="How often do you find yourself talking too much when you are in social situations?",
                scale_name="ASRS",
                subscale="Part B"
            ),
            ScaleQuestion(
                id="asrs_16",
                text="When you're in a conversation, how often do you find yourself finishing the sentences of the people you are talking to, before they can finish them themselves?",
                scale_name="ASRS",
                subscale="Part B"
            ),
            ScaleQuestion(
                id="asrs_17",
                text="How often do you have difficulty waiting your turn in situations when turn taking is required?",
                scale_name="ASRS",
                subscale="Part B"
            ),
            ScaleQuestion(
                id="asrs_18",
                text="How often do you interrupt others when they are busy?",
                scale_name="ASRS",
                subscale="Part B"
            ),
        ]
        
        return part_a + part_b
    
    @staticmethod
    def get_phq9_questions() -> List[ScaleQuestion]:
        """
        PHQ-9 (Patient Health Questionnaire - 9).
        
        Gold standard depression screening tool.
        9 questions based on DSM-5 MDD criteria.
        
        Response scale: 0=Not at all, 1=Several days, 2=More than half the days,
                       3=Nearly every day
        
        Scoring:
        - 0-4: Minimal depression
        - 5-9: Mild depression
        - 10-14: Moderate depression
        - 15-19: Moderately severe depression
        - 20-27: Severe depression
        
        Reference:
        Kroenke K, et al. (2001). The PHQ-9: validity of a brief depression
        severity measure. J Gen Intern Med, 16(9), 606-613.
        """
        questions = [
            "Little interest or pleasure in doing things",
            "Feeling down, depressed, or hopeless",
            "Trouble falling or staying asleep, or sleeping too much",
            "Feeling tired or having little energy",
            "Poor appetite or overeating",
            "Feeling bad about yourself - or that you are a failure or have let yourself or your family down",
            "Trouble concentrating on things, such as reading the newspaper or watching television",
            "Moving or speaking so slowly that other people could have noticed. Or the opposite - being so fidgety or restless that you have been moving around a lot more than usual",
            "Thoughts that you would be better off dead, or of hurting yourself"
        ]
        
        return [
            ScaleQuestion(
                id=f"phq9_{i+1}",
                text=questions[i],
                scale_name="PHQ-9"
            )
            for i in range(9)
        ]
    
    @staticmethod
    def get_gad7_questions() -> List[ScaleQuestion]:
        """
        GAD-7 (Generalized Anxiety Disorder - 7).
        
        Validated anxiety screening tool.
        7 questions assessing anxiety symptoms.
        
        Response scale: 0=Not at all, 1=Several days, 2=More than half the days,
                       3=Nearly every day
        
        Scoring:
        - 0-4: Minimal anxiety
        - 5-9: Mild anxiety
        - 10-14: Moderate anxiety
        - 15-21: Severe anxiety
        
        Reference:
        Spitzer RL, et al. (2006). A brief measure for assessing generalized
        anxiety disorder: the GAD-7. Arch Intern Med, 166(10), 1092-1097.
        """
        questions = [
            "Feeling nervous, anxious, or on edge",
            "Not being able to stop or control worrying",
            "Worrying too much about different things",
            "Trouble relaxing",
            "Being so restless that it's hard to sit still",
            "Becoming easily annoyed or irritable",
            "Feeling afraid, as if something awful might happen"
        ]
        
        return [
            ScaleQuestion(
                id=f"gad7_{i+1}",
                text=questions[i],
                scale_name="GAD-7"
            )
            for i in range(7)
        ]
    
    @staticmethod
    def get_developmental_history_questions() -> List[Dict[str, Any]]:
        """
        Developmental and childhood history questions.
        
        Critical for ADHD diagnosis (Criterion B: childhood onset).
        These questions help differentiate ADHD from adult-onset mood/anxiety disorders.
        """
        return [
            {
                "id": "childhood_symptoms",
                "text": "Did you have significant attention, hyperactivity, or impulsivity problems as a child (before age 12)?",
                "type": "likert",
                "scale": "0=Not at all, 4=Very much",
                "clinical_importance": "REQUIRED for ADHD diagnosis"
            },
            {
                "id": "symptom_onset_age",
                "text": "At what age did you first notice these difficulties?",
                "type": "numeric",
                "range": [0, 100],
                "clinical_importance": "Onset before age 12 required for ADHD"
            },
            {
                "id": "childhood_impairment",
                "text": "How much did these problems affect your school performance or behavior as a child?",
                "type": "likert",
                "scale": "0=Not at all, 4=Severely",
                "clinical_importance": "Functional impairment is required"
            },
            {
                "id": "report_card_comments",
                "text": "Did teachers comment on report cards about attention problems, not listening, not finishing work, or being disruptive?",
                "type": "boolean",
                "clinical_importance": "Collateral information supports diagnosis"
            }
        ]
    
    @staticmethod
    def get_functional_impairment_questions() -> List[Dict[str, Any]]:
        """
        Cross-situational functional impairment assessment.
        
        DSM Criterion C and D: symptoms in multiple settings + impairment.
        """
        return [
            {
                "id": "work_impairment",
                "text": "How much do these symptoms interfere with your work or academic performance?",
                "type": "likert",
                "scale": "0=Not at all, 4=Severely"
            },
            {
                "id": "home_impairment",
                "text": "How much do these symptoms interfere with managing household responsibilities?",
                "type": "likert",
                "scale": "0=Not at all, 4=Severely"
            },
            {
                "id": "social_impairment",
                "text": "How much do these symptoms interfere with your social life or friendships?",
                "type": "likert",
                "scale": "0=Not at all, 4=Severely"
            },
            {
                "id": "relationship_impairment",
                "text": "How much do these symptoms affect your close relationships?",
                "type": "likert",
                "scale": "0=Not at all, 4=Severely"
            }
        ]
