"""Clinical reasoning rules and heuristics for differential diagnosis.

This module encodes expert clinical knowledge that goes beyond
the formal DSM-5-TR criteria, including:
- Common diagnostic pitfalls
- Pattern recognition heuristics
- Contextual interpretation guidelines
- Differential diagnosis decision trees
"""

from typing import Dict, List, Any, Tuple
from enum import Enum

class DiagnosticPattern(Enum):
    """Common diagnostic presentation patterns."""
    ADHD_PREDOMINANT = "adhd_predominant"
    DEPRESSION_PREDOMINANT = "depression_predominant"
    ANXIETY_PREDOMINANT = "anxiety_predominant"
    ADHD_WITH_DEPRESSION = "adhd_with_depression"
    ADHD_WITH_ANXIETY = "adhd_with_anxiety"
    DEPRESSION_WITH_ANXIETY = "depression_with_anxiety"
    COMPLEX_COMORBID = "complex_comorbid"
    UNCLEAR_SUBCLINICAL = "unclear_subclinical"

class ClinicalRules:
    """
    Expert clinical reasoning rules for ADHD differential diagnosis.
    
    These rules synthesize knowledge from:
    - Clinical practice guidelines (APA, NICE, CADDRA)
    - Peer-reviewed research on differential diagnosis
    - Expert clinician decision-making patterns
    - Common misdiagnosis scenarios
    """
    
    @staticmethod
    def evaluate_childhood_onset(responses: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate childhood onset - CRITICAL for ADHD diagnosis.
        
        Clinical reasoning:
        - True ADHD: symptoms present before age 12, often earlier
        - Depression/anxiety: typically onset in adolescence/adulthood
        - Retrospective bias: adults may not recall childhood accurately
        - Collateral information (report cards, parent input) valuable
        
        Red flags suggesting NOT primary ADHD:
        - Clear symptom onset after age 12
        - No childhood difficulties reported
        - Sudden onset related to life stressor
        """
        childhood_symptoms = responses.get("childhood_symptoms", 0)
        age_of_onset = responses.get("symptom_onset_age", 18)
        childhood_impairment = responses.get("childhood_impairment", 0)
        
        # Scoring
        onset_score = 0
        confidence = "low"
        interpretation = ""
        
        if age_of_onset <= 7:
            onset_score = 3.0  # Strong evidence for ADHD
            confidence = "high"
            interpretation = "Early childhood onset strongly supports ADHD"
        elif age_of_onset <= 12:
            onset_score = 2.0  # Meets DSM criterion
            confidence = "moderate"
            interpretation = "Childhood onset consistent with ADHD"
        elif age_of_onset <= 17:
            onset_score = 0.5  # Possible, but raises questions
            confidence = "low"
            interpretation = "Adolescent onset less typical for ADHD; consider mood/anxiety"
        else:
            onset_score = 0.0  # Does NOT meet ADHD criterion B
            confidence = "high"
            interpretation = "Adult onset rules out primary ADHD; likely depression/anxiety"
        
        # Adjust for reported childhood impairment
        if childhood_impairment >= 3:
            onset_score += 0.5
        
        return {
            "onset_score": onset_score,
            "confidence": confidence,
            "interpretation": interpretation,
            "criterion_b_met": age_of_onset <= 12,
            "clinical_note": "Criterion B (childhood onset) is REQUIRED for ADHD diagnosis"
        }
    
    @staticmethod
    def evaluate_cross_situational_impairment(
        responses: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Evaluate cross-situational impairment (DSM Criterion C).
        
        Clinical reasoning:
        - True ADHD: symptoms in multiple contexts (work, home, social)
        - Situational issues: symptoms limited to one context (e.g., only at work)
        - Environmental factors: toxic workplace, abusive relationship
        
        Key questions:
        - Problems at work AND home?
        - Difficulties in relationships?
        - Consistent pattern across life domains?
        """
        work_impairment = responses.get("work_impairment", 0)
        home_impairment = responses.get("home_impairment", 0)
        social_impairment = responses.get("social_impairment", 0)
        relationship_impairment = responses.get("relationship_impairment", 0)
        
        # Count contexts with significant impairment (score >= 2)
        impairment_contexts = sum([
            1 for score in [work_impairment, home_impairment, 
                          social_impairment, relationship_impairment]
            if score >= 2
        ])
        
        criterion_c_met = impairment_contexts >= 2
        
        if impairment_contexts >= 3:
            interpretation = "Pervasive impairment across multiple contexts supports ADHD"
            confidence = "high"
        elif impairment_contexts == 2:
            interpretation = "Cross-situational impairment meets diagnostic threshold"
            confidence = "moderate"
        elif impairment_contexts == 1:
            interpretation = "Single-context impairment suggests situational stress, not ADHD"
            confidence = "moderate"
        else:
            interpretation = "Minimal reported impairment; subclinical presentation"
            confidence = "high"
        
        return {
            "impairment_contexts": impairment_contexts,
            "criterion_c_met": criterion_c_met,
            "interpretation": interpretation,
            "confidence": confidence
        }
    
    @staticmethod
    def differentiate_adhd_vs_depression(
        responses: Dict[str, Any],
        asrs_score: float,
        phq9_score: float
    ) -> Dict[str, Any]:
        """
        Core differential diagnosis: ADHD vs Depression.
        
        Overlapping symptoms:
        - Difficulty concentrating
        - Forgetfulness
        - Task completion issues
        - Fatigue/low motivation
        
        Key differentiators:
        
        ADHD indicators:
        - Lifelong pattern (not episodic)
        - Difficulty focusing even on enjoyable tasks
        - Restlessness, fidgeting
        - Impulsivity, interrupt others
        - Symptoms consistent regardless of mood
        
        Depression indicators:
        - Episodic (symptoms wax/wane)
        - Anhedonia (loss of pleasure)
        - Pervasive sadness, hopelessness
        - Guilt, worthlessness
        - Concentration improves when mood lifts
        - Suicidal thoughts
        
        Clinical pearl:
        "Can you focus when you're interested?"
        - ADHD: Still struggles even with interesting content
        - Depression: Can focus better on interesting things, but lacks interest
        """
        # Extract key differentiating responses
        lifelong_pattern = responses.get("lifelong_symptoms", 0)
        episodic_pattern = responses.get("episodic_symptoms", 0)
        anhedonia = responses.get("anhedonia", 0)
        sadness = responses.get("depressed_mood", 0)
        restlessness = responses.get("restlessness", 0)
        mood_impact_on_concentration = responses.get(
            "concentration_worse_when_sad", 0
        )
        
        # Scoring logic
        adhd_weight = 0.0
        depression_weight = 0.0
        
        # Temporal pattern is HIGHLY diagnostic
        if lifelong_pattern >= 3:
            adhd_weight += 2.0
        if episodic_pattern >= 3:
            depression_weight += 2.0
        
        # Core mood symptoms
        if anhedonia >= 3 or sadness >= 3:
            depression_weight += 1.5
        
        # Hyperactivity/restlessness (more specific to ADHD in absence of anxiety)
        anxiety_score = responses.get("anxiety_level", 0)
        if restlessness >= 3 and anxiety_score < 2:
            adhd_weight += 1.2
        
        # Mood-dependent concentration
        if mood_impact_on_concentration >= 3:
            depression_weight += 1.0
            adhd_weight -= 0.5
        
        # Scale scores
        if asrs_score > phq9_score * 1.5:
            adhd_weight += 1.0
        elif phq9_score > asrs_score * 1.5:
            depression_weight += 1.0
        
        # Determine primary diagnosis
        if adhd_weight > depression_weight * 1.3:
            primary = "ADHD"
            confidence = "moderate" if depression_weight > 2 else "high"
        elif depression_weight > adhd_weight * 1.3:
            primary = "Depression"
            confidence = "moderate" if adhd_weight > 2 else "high"
        else:
            primary = "Comorbid"
            confidence = "moderate"
        
        return {
            "primary_diagnosis": primary,
            "adhd_weight": adhd_weight,
            "depression_weight": depression_weight,
            "confidence": confidence,
            "clinical_reasoning": {
                "temporal_pattern": "lifelong" if lifelong_pattern >= 3 else "episodic",
                "mood_symptoms_present": anhedonia >= 2 or sadness >= 2,
                "concentration_mood_linked": mood_impact_on_concentration >= 2
            }
        }
    
    @staticmethod
    def differentiate_adhd_vs_anxiety(
        responses: Dict[str, Any],
        asrs_score: float,
        gad7_score: float
    ) -> Dict[str, Any]:
        """
        Differential diagnosis: ADHD vs Anxiety.
        
        Overlapping symptoms:
        - Difficulty concentrating
        - Restlessness
        - Sleep problems
        - Irritability
        
        Key differentiators:
        
        ADHD indicators:
        - Mind wanders to random, unrelated thoughts
        - Restlessness feels good (need to move)
        - Impulsivity across contexts
        - Childhood onset
        
        Anxiety indicators:
        - Mind occupied by specific worries
        - Restlessness feels uncomfortable (nervous energy)
        - Avoidance behaviors
        - Physical symptoms (muscle tension, racing heart)
        - May have clear triggers or onset
        
        Clinical pearl:
        "When your mind wanders, where does it go?"
        - ADHD: Random, unrelated thoughts ("squirrel!")
        - Anxiety: Worries, catastrophic thinking, rumination
        """
        worry_content = responses.get("mind_full_of_worries", 0)
        random_thoughts = responses.get("mind_random_thoughts", 0)
        physical_anxiety = responses.get("physical_anxiety_symptoms", 0)
        impulsivity = responses.get("impulsivity_score", 0)
        avoidance = responses.get("avoidance_behaviors", 0)
        
        adhd_weight = 0.0
        anxiety_weight = 0.0
        
        # Thought pattern is highly diagnostic
        if random_thoughts >= 3:
            adhd_weight += 1.5
        if worry_content >= 3:
            anxiety_weight += 1.5
        
        # Physical anxiety symptoms
        if physical_anxiety >= 3:
            anxiety_weight += 1.2
        
        # Impulsivity (more specific to ADHD)
        if impulsivity >= 3:
            adhd_weight += 1.3
        
        # Avoidance (more specific to anxiety)
        if avoidance >= 3:
            anxiety_weight += 1.0
        
        # Scale scores
        if asrs_score > gad7_score * 1.5:
            adhd_weight += 1.0
        elif gad7_score > asrs_score * 1.5:
            anxiety_weight += 1.0
        
        if adhd_weight > anxiety_weight * 1.3:
            primary = "ADHD"
            confidence = "moderate" if anxiety_weight > 2 else "high"
        elif anxiety_weight > adhd_weight * 1.3:
            primary = "Anxiety"
            confidence = "moderate" if adhd_weight > 2 else "high"
        else:
            primary = "Comorbid"
            confidence = "moderate"
        
        return {
            "primary_diagnosis": primary,
            "adhd_weight": adhd_weight,
            "anxiety_weight": anxiety_weight,
            "confidence": confidence,
            "clinical_reasoning": {
                "thought_pattern": "random" if random_thoughts >= 3 else "worry-focused",
                "physical_symptoms": physical_anxiety >= 2,
                "impulsivity_present": impulsivity >= 2
            }
        }
    
    @staticmethod
    def determine_diagnostic_pattern(
        adhd_likelihood: float,
        depression_likelihood: float,
        anxiety_likelihood: float,
        thresholds: Dict[str, float] = None
    ) -> Tuple[DiagnosticPattern, str]:
        """
        Determine overall diagnostic pattern using expert heuristics.
        
        Thresholds are based on clinical experience:
        - High threshold: Strong evidence (>0.7)
        - Moderate threshold: Clinically significant (>0.5)
        - Low threshold: Subclinical (>0.3)
        """
        if thresholds is None:
            thresholds = {"high": 0.7, "moderate": 0.5, "low": 0.3}
        
        high = thresholds["high"]
        mod = thresholds["moderate"]
        
        # Count conditions meeting thresholds
        high_conditions = sum([
            adhd_likelihood >= high,
            depression_likelihood >= high,
            anxiety_likelihood >= high
        ])
        
        mod_conditions = sum([
            adhd_likelihood >= mod,
            depression_likelihood >= mod,
            anxiety_likelihood >= mod
        ])
        
        # Pattern recognition
        if high_conditions >= 3:
            return (DiagnosticPattern.COMPLEX_COMORBID, 
                   "Complex comorbid presentation requiring comprehensive evaluation")
        
        if adhd_likelihood >= high:
            if depression_likelihood >= mod:
                return (DiagnosticPattern.ADHD_WITH_DEPRESSION,
                       "ADHD with comorbid depressive symptoms")
            elif anxiety_likelihood >= mod:
                return (DiagnosticPattern.ADHD_WITH_ANXIETY,
                       "ADHD with comorbid anxiety")
            else:
                return (DiagnosticPattern.ADHD_PREDOMINANT,
                       "ADHD presentation without significant comorbidity")
        
        if depression_likelihood >= high:
            if anxiety_likelihood >= mod:
                return (DiagnosticPattern.DEPRESSION_WITH_ANXIETY,
                       "Depression with comorbid anxiety")
            else:
                return (DiagnosticPattern.DEPRESSION_PREDOMINANT,
                       "Primary depressive disorder")
        
        if anxiety_likelihood >= high:
            return (DiagnosticPattern.ANXIETY_PREDOMINANT,
                   "Primary anxiety disorder")
        
        if mod_conditions >= 2:
            # Determine which two are highest
            if adhd_likelihood >= mod and depression_likelihood >= mod:
                return (DiagnosticPattern.ADHD_WITH_DEPRESSION,
                       "Possible ADHD and depression - further evaluation needed")
            elif adhd_likelihood >= mod and anxiety_likelihood >= mod:
                return (DiagnosticPattern.ADHD_WITH_ANXIETY,
                       "Possible ADHD and anxiety - further evaluation needed")
            else:
                return (DiagnosticPattern.DEPRESSION_WITH_ANXIETY,
                       "Possible depression and anxiety")
        
        if adhd_likelihood >= mod:
            return (DiagnosticPattern.ADHD_PREDOMINANT,
                   "Possible ADHD - clinical evaluation recommended")
        
        if depression_likelihood >= mod:
            return (DiagnosticPattern.DEPRESSION_PREDOMINANT,
                   "Possible depression - clinical evaluation recommended")
        
        if anxiety_likelihood >= mod:
            return (DiagnosticPattern.ANXIETY_PREDOMINANT,
                   "Possible anxiety - clinical evaluation recommended")
        
        return (DiagnosticPattern.UNCLEAR_SUBCLINICAL,
               "Subclinical symptoms - monitoring may be appropriate")
