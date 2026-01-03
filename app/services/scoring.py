"""Validated clinical scale scoring service.

Implements:
- ASRS v1.1 (Adult ADHD Self-Report Scale)
- PHQ-9 (Patient Health Questionnaire for Depression)
- GAD-7 (Generalized Anxiety Disorder Scale)
"""

from typing import Dict, Any
from app.models.results import ScaleScores

class ScoringService:
    """
    Calculate scores for validated clinical instruments.
    
    These scales provide quantitative measures but are interpreted
    within the broader clinical context by the expert system.
    """
    
    def calculate_all_scores(self, responses: Dict[str, Any]) -> ScaleScores:
        """Calculate all scale scores from user responses."""
        
        asrs_total, asrs_part_a = self._calculate_asrs(responses)
        phq9_total = self._calculate_phq9(responses)
        gad7_total = self._calculate_gad7(responses)
        
        return ScaleScores(
            asrs_total=asrs_total,
            asrs_part_a=asrs_part_a,
            asrs_interpretation=self._interpret_asrs(asrs_part_a),
            phq9_total=phq9_total,
            phq9_severity=self._interpret_phq9(phq9_total),
            gad7_total=gad7_total,
            gad7_severity=self._interpret_gad7(gad7_total)
        )
    
    def _calculate_asrs(self, responses: Dict[str, Any]) -> tuple[float, float]:
        """
        Calculate ASRS v1.1 scores.
        
        Part A (6 items): Screening questions, highly predictive
        Part B (12 items): Additional symptoms
        
        Scoring: 0-4 scale (Never, Rarely, Sometimes, Often, Very Often)
        Part A threshold: 4+ items scored 2+ indicates likely ADHD
        """
        # ASRS question IDs
        part_a_ids = [
            "asrs_1", "asrs_2", "asrs_3", "asrs_4", "asrs_5", "asrs_6"
        ]
        part_b_ids = [
            f"asrs_{i}" for i in range(7, 19)
        ]
        
        # Calculate Part A score
        part_a_score = 0
        part_a_threshold_met = 0
        
        for qid in part_a_ids:
            value = responses.get(qid, 0)
            part_a_score += value
            if value >= 2:  # "Sometimes" or higher
                part_a_threshold_met += 1
        
        # Calculate total score (Part A + Part B)
        total_score = part_a_score
        for qid in part_b_ids:
            total_score += responses.get(qid, 0)
        
        return total_score, part_a_threshold_met
    
    def _interpret_asrs(self, part_a_score: float) -> str:
        """Interpret ASRS Part A screening result."""
        if part_a_score >= 4:
            return "Highly consistent with ADHD - further evaluation recommended"
        elif part_a_score >= 2:
            return "Possible ADHD - clinical interview needed"
        else:
            return "Below screening threshold"
    
    def _calculate_phq9(self, responses: Dict[str, Any]) -> float:
        """
        Calculate PHQ-9 depression score.
        
        9 items scored 0-3:
        0 = Not at all
        1 = Several days
        2 = More than half the days
        3 = Nearly every day
        
        Range: 0-27
        """
        phq9_ids = [f"phq9_{i}" for i in range(1, 10)]
        return sum(responses.get(qid, 0) for qid in phq9_ids)
    
    def _interpret_phq9(self, score: float) -> str:
        """Interpret PHQ-9 severity."""
        if score >= 20:
            return "Severe depression"
        elif score >= 15:
            return "Moderately severe depression"
        elif score >= 10:
            return "Moderate depression"
        elif score >= 5:
            return "Mild depression"
        else:
            return "Minimal/none"
    
    def _calculate_gad7(self, responses: Dict[str, Any]) -> float:
        """
        Calculate GAD-7 anxiety score.
        
        7 items scored 0-3:
        0 = Not at all
        1 = Several days
        2 = More than half the days
        3 = Nearly every day
        
        Range: 0-21
        """
        gad7_ids = [f"gad7_{i}" for i in range(1, 8)]
        return sum(responses.get(qid, 0) for qid in gad7_ids)
    
    def _interpret_gad7(self, score: float) -> str:
        """Interpret GAD-7 severity."""
        if score >= 15:
            return "Severe anxiety"
        elif score >= 10:
            return "Moderate anxiety"
        elif score >= 5:
            return "Mild anxiety"
        else:
            return "Minimal/none"
