"""DSM-5-TR diagnostic criteria for ADHD and common differential diagnoses.

This module encodes evidence-based diagnostic criteria as structured data
for use in the expert system's rule-based reasoning engine.
"""

from typing import Dict, List, Any
from dataclasses import dataclass

@dataclass
class DiagnosticCriterion:
    """Represents a single diagnostic criterion."""
    id: str
    description: str
    weight: float = 1.0
    required: bool = False

class DSM5Criteria:
    """
    DSM-5-TR Diagnostic Criteria Repository.
    
    Based on:
    - American Psychiatric Association. (2022). Diagnostic and Statistical
      Manual of Mental Disorders (5th ed., text rev.).
    - CDC ADHD Diagnostic Guidelines
    - WHO ICD-11 Diagnostic Criteria
    """
    
    def __init__(self):
        self.adhd_inattention = self._init_adhd_inattention()
        self.adhd_hyperactivity = self._init_adhd_hyperactivity()
        self.adhd_general_criteria = self._init_adhd_general()
        self.depression_criteria = self._init_depression()
        self.anxiety_criteria = self._init_anxiety()
    
    def _init_adhd_inattention(self) -> List[DiagnosticCriterion]:
        """ADHD Criterion A1: Inattention symptoms."""
        return [
            DiagnosticCriterion(
                id="adhd_inatt_1",
                description="Fails to give close attention to details or makes careless mistakes",
                weight=1.0
            ),
            DiagnosticCriterion(
                id="adhd_inatt_2",
                description="Difficulty sustaining attention in tasks or play activities",
                weight=1.2  # Highly characteristic of ADHD
            ),
            DiagnosticCriterion(
                id="adhd_inatt_3",
                description="Does not seem to listen when spoken to directly",
                weight=0.9
            ),
            DiagnosticCriterion(
                id="adhd_inatt_4",
                description="Does not follow through on instructions, fails to finish tasks",
                weight=1.0
            ),
            DiagnosticCriterion(
                id="adhd_inatt_5",
                description="Difficulty organizing tasks and activities",
                weight=1.1
            ),
            DiagnosticCriterion(
                id="adhd_inatt_6",
                description="Avoids or dislikes tasks requiring sustained mental effort",
                weight=1.2
            ),
            DiagnosticCriterion(
                id="adhd_inatt_7",
                description="Loses things necessary for tasks or activities",
                weight=1.0
            ),
            DiagnosticCriterion(
                id="adhd_inatt_8",
                description="Easily distracted by extraneous stimuli",
                weight=1.3  # Very characteristic
            ),
            DiagnosticCriterion(
                id="adhd_inatt_9",
                description="Forgetful in daily activities",
                weight=1.0
            ),
        ]
    
    def _init_adhd_hyperactivity(self) -> List[DiagnosticCriterion]:
        """ADHD Criterion A2: Hyperactivity-Impulsivity symptoms."""
        return [
            DiagnosticCriterion(
                id="adhd_hyper_1",
                description="Fidgets with hands or feet or squirms in seat",
                weight=1.0
            ),
            DiagnosticCriterion(
                id="adhd_hyper_2",
                description="Leaves seat in situations when remaining seated is expected",
                weight=1.1
            ),
            DiagnosticCriterion(
                id="adhd_hyper_3",
                description="Feels restless (in adults)",
                weight=1.2
            ),
            DiagnosticCriterion(
                id="adhd_hyper_4",
                description="Unable to engage in leisure activities quietly",
                weight=0.9
            ),
            DiagnosticCriterion(
                id="adhd_hyper_5",
                description="Is 'on the go' or acts as if 'driven by a motor'",
                weight=1.3  # Highly characteristic
            ),
            DiagnosticCriterion(
                id="adhd_hyper_6",
                description="Talks excessively",
                weight=0.8
            ),
            DiagnosticCriterion(
                id="adhd_hyper_7",
                description="Blurts out answers before questions completed",
                weight=1.1
            ),
            DiagnosticCriterion(
                id="adhd_hyper_8",
                description="Difficulty waiting turn",
                weight=1.0
            ),
            DiagnosticCriterion(
                id="adhd_hyper_9",
                description="Interrupts or intrudes on others",
                weight=1.0
            ),
        ]
    
    def _init_adhd_general(self) -> Dict[str, Any]:
        """
        ADHD General Criteria (B, C, D, E).
        
        Critical for differential diagnosis:
        - Childhood onset distinguishes from mood/anxiety disorders
        - Cross-situational impairment rules out context-specific issues
        - Functional impairment threshold
        """
        return {
            "criterion_b": {
                "description": "Several symptoms present before age 12",
                "required": True,
                "clinical_note": "This is CRITICAL for ADHD diagnosis. Symptoms starting in adulthood suggest depression/anxiety."
            },
            "criterion_c": {
                "description": "Symptoms present in 2+ settings (home, work, school, social)",
                "required": True,
                "clinical_note": "Single-context symptoms suggest situational stress rather than ADHD."
            },
            "criterion_d": {
                "description": "Clear evidence of interference with functioning",
                "required": True,
                "clinical_note": "Mild symptoms without impairment don't meet diagnostic threshold."
            },
            "criterion_e": {
                "description": "Symptoms not better explained by another mental disorder",
                "required": True,
                "clinical_note": "This is where differential diagnosis is essential."
            },
            "symptom_threshold": {
                "adults": 5,  # 5+ symptoms in either domain for adults (17+)
                "children": 6,  # 6+ symptoms for children/adolescents
                "note": "For adults, 5+ symptoms of inattention OR hyperactivity-impulsivity"
            }
        }
    
    def _init_depression(self) -> Dict[str, Any]:
        """
        Major Depressive Disorder criteria relevant to differential diagnosis.
        
        Key differentiators from ADHD:
        - Episodic vs chronic/lifelong pattern
        - Mood symptoms (anhedonia, sadness, guilt)
        - Vegetative symptoms (sleep, appetite, energy)
        - Suicidal ideation
        - Cognitive symptoms are mood-congruent
        """
        return {
            "core_symptoms": [
                {
                    "id": "dep_mood",
                    "description": "Depressed mood most of the day, nearly every day",
                    "weight": 1.5,
                    "differentiator": "Primary mood disturbance distinguishes from ADHD"
                },
                {
                    "id": "dep_anhedonia",
                    "description": "Markedly diminished interest or pleasure in activities",
                    "weight": 1.5,
                    "differentiator": "Loss of interest vs ADHD's boredom with unstimulating tasks"
                },
            ],
            "additional_symptoms": [
                "Weight/appetite changes",
                "Insomnia or hypersomnia",
                "Psychomotor agitation or retardation",
                "Fatigue or loss of energy",
                "Feelings of worthlessness or guilt",
                "Diminished concentration (secondary to mood)",
                "Recurrent thoughts of death"
            ],
            "temporal_pattern": {
                "description": "Episodic - symptoms present for at least 2 weeks",
                "differentiator": "ADHD is chronic/lifelong; depression is episodic"
            },
            "clinical_notes": [
                "Depression-related inattention improves when mood lifts",
                "ADHD inattention is persistent regardless of mood",
                "Depression typically has later onset (teens/adulthood)",
                "Depression may develop secondary to ADHD-related failures"
            ]
        }
    
    def _init_anxiety(self) -> Dict[str, Any]:
        """
        Generalized Anxiety Disorder and anxiety-related attentional issues.
        
        Key differentiators from ADHD:
        - Worry-driven vs primary attentional deficit
        - Context-dependent (anxiety-provoking situations)
        - Physiological anxiety symptoms
        - Cognitive symptoms tied to worry content
        """
        return {
            "core_features": [
                {
                    "id": "anx_worry",
                    "description": "Excessive worry about multiple topics",
                    "weight": 1.5,
                    "differentiator": "Primary worry vs ADHD's racing thoughts"
                },
                {
                    "id": "anx_control",
                    "description": "Difficulty controlling the worry",
                    "weight": 1.4
                },
            ],
            "associated_symptoms": [
                "Restlessness or feeling on edge",
                "Being easily fatigued",
                "Difficulty concentrating (due to worry)",
                "Irritability",
                "Muscle tension",
                "Sleep disturbance"
            ],
            "differentiators": [
                "Anxiety-driven inattention: mind is occupied by worries",
                "ADHD inattention: mind wanders to unrelated, non-anxious thoughts",
                "Anxiety restlessness: feels like nervous energy, tension",
                "ADHD restlessness: need for movement, fidgeting, feels good to move",
                "Anxiety onset often tied to stressors; ADHD is lifelong"
            ],
            "clinical_notes": [
                "High comorbidity: 50%+ of adults with ADHD have anxiety",
                "Anxiety may be secondary to ADHD-related difficulties",
                "ADHD may worsen anxiety through executive dysfunction",
                "Treatment approach differs based on primary vs secondary"
            ]
        }
    
    def get_symptom_count_threshold(self, age: int) -> int:
        """Get required symptom count based on age."""
        return 5 if age >= 17 else 6
    
    def get_criterion_by_id(self, criterion_id: str) -> DiagnosticCriterion:
        """Retrieve a specific diagnostic criterion."""
        all_criteria = (self.adhd_inattention + 
                       self.adhd_hyperactivity)
        for criterion in all_criteria:
            if criterion.id == criterion_id:
                return criterion
        raise ValueError(f"Criterion {criterion_id} not found")
