"""Expert system for ADHD differential diagnosis.

This module implements clinical decision-support logic using:
- Rule-based reasoning
- Pattern matching
- Bayesian-inspired likelihood estimation
- Expert clinical heuristics
"""

from typing import Dict, Any
import logging

from app.models.results import (
    EvaluationResult,
    ScaleScores,
    DiagnosticLikelihood,
    ClinicalRecommendation
)
from app.knowledge_base.dsm5_criteria import DSM5Criteria
from app.knowledge_base.clinical_rules import ClinicalRules, DiagnosticPattern

logger = logging.getLogger(__name__)

class ExpertSystem:
    """
    Clinical Expert System for ADHD Differential Diagnosis.
    
    Architecture:
    1. Knowledge Base: DSM-5-TR criteria + clinical rules
    2. Inference Engine: Rule-based reasoning + pattern matching
    3. Explanation Generator: Human-readable clinical reasoning
    
    Clinical approach:
    - Start with validated scales (ASRS, PHQ-9, GAD-7)
    - Apply DSM-5-TR diagnostic criteria
    - Use expert heuristics for differential diagnosis
    - Consider developmental history and context
    - Generate likelihood estimates, not definitive diagnoses
    """
    
    def __init__(self):
        self.dsm5 = DSM5Criteria()
        self.rules = ClinicalRules()
        logger.info("Expert system initialized with DSM-5-TR criteria")
    
    def evaluate(
        self,
        responses: Dict[str, Any],
        scale_scores: ScaleScores,
        user_info: Dict[str, Any]
    ) -> EvaluationResult:
        """
        Perform comprehensive clinical evaluation.
        
        Process:
        1. Validate input data
        2. Evaluate childhood onset (Criterion B)
        3. Assess cross-situational impairment (Criterion C)
        4. Apply differential diagnosis rules
        5. Calculate diagnostic likelihoods
        6. Determine pattern and recommendations
        7. Generate clinical reasoning explanation
        """
        logger.info(f"Starting evaluation for user age {user_info.get('age', 'unknown')}")
        
        # Step 1: Evaluate childhood onset (CRITICAL for ADHD)
        childhood_eval = self.rules.evaluate_childhood_onset(responses)
        
        # Step 2: Evaluate cross-situational impairment
        impairment_eval = self.rules.evaluate_cross_situational_impairment(responses)
        
        # Step 3: Differential diagnosis - ADHD vs Depression
        adhd_dep_diff = self.rules.differentiate_adhd_vs_depression(
            responses=responses,
            asrs_score=scale_scores.asrs_part_a,
            phq9_score=scale_scores.phq9_total
        )
        
        # Step 4: Differential diagnosis - ADHD vs Anxiety
        adhd_anx_diff = self.rules.differentiate_adhd_vs_anxiety(
            responses=responses,
            asrs_score=scale_scores.asrs_part_a,
            gad7_score=scale_scores.gad7_total
        )
        
        # Step 5: Calculate diagnostic likelihoods
        adhd_likelihood = self._calculate_adhd_likelihood(
            scale_scores=scale_scores,
            childhood_eval=childhood_eval,
            impairment_eval=impairment_eval,
            adhd_dep_diff=adhd_dep_diff,
            adhd_anx_diff=adhd_anx_diff
        )
        
        depression_likelihood = self._calculate_depression_likelihood(
            scale_scores=scale_scores,
            adhd_dep_diff=adhd_dep_diff
        )
        
        anxiety_likelihood = self._calculate_anxiety_likelihood(
            scale_scores=scale_scores,
            adhd_anx_diff=adhd_anx_diff
        )
        
        # Step 6: Determine overall diagnostic pattern
        pattern, pattern_description = self.rules.determine_diagnostic_pattern(
            adhd_likelihood=adhd_likelihood.likelihood,
            depression_likelihood=depression_likelihood.likelihood,
            anxiety_likelihood=anxiety_likelihood.likelihood
        )
        
        # Step 7: Generate recommendations
        recommendations = self._generate_recommendations(
            pattern=pattern,
            adhd_likelihood=adhd_likelihood,
            depression_likelihood=depression_likelihood,
            anxiety_likelihood=anxiety_likelihood,
            scale_scores=scale_scores,
            childhood_eval=childhood_eval
        )
        
        # Step 8: Generate clinical reasoning explanation
        reasoning = self._generate_clinical_reasoning(
            scale_scores=scale_scores,
            childhood_eval=childhood_eval,
            impairment_eval=impairment_eval,
            adhd_dep_diff=adhd_dep_diff,
            adhd_anx_diff=adhd_anx_diff,
            pattern=pattern
        )
        
        logger.info(f"Evaluation complete: Pattern={pattern.value}")
        
        return EvaluationResult(
            scale_scores=scale_scores,
            adhd_likelihood=adhd_likelihood,
            depression_likelihood=depression_likelihood,
            anxiety_likelihood=anxiety_likelihood,
            primary_pattern=pattern.value,
            pattern_description=pattern_description,
            clinical_reasoning=reasoning,
            recommendations=recommendations,
            disclaimer=self._get_disclaimer()
        )
    
    def _calculate_adhd_likelihood(
        self,
        scale_scores: ScaleScores,
        childhood_eval: Dict[str, Any],
        impairment_eval: Dict[str, Any],
        adhd_dep_diff: Dict[str, Any],
        adhd_anx_diff: Dict[str, Any]
    ) -> DiagnosticLikelihood:
        """
        Calculate ADHD likelihood using Bayesian-inspired approach.
        
        Key factors:
        1. ASRS score (validated screening tool)
        2. Childhood onset (REQUIRED by DSM-5-TR)
        3. Cross-situational impairment (REQUIRED)
        4. Differential diagnosis weights
        """
        # Start with ASRS screening result
        if scale_scores.asrs_part_a >= 4:
            base_likelihood = 0.75  # High ASRS score
        elif scale_scores.asrs_part_a >= 2:
            base_likelihood = 0.50  # Moderate ASRS score
        else:
            base_likelihood = 0.15  # Low ASRS score
        
        # Apply childhood onset criterion (CRITICAL)
        if not childhood_eval["criterion_b_met"]:
            base_likelihood *= 0.2  # Massive reduction if no childhood onset
            confidence = "high"
            reasoning = "Adult onset makes ADHD very unlikely"
        elif childhood_eval["onset_score"] >= 2.5:
            base_likelihood *= 1.3  # Boost for early childhood onset
            confidence = "high"
            reasoning = "Early childhood onset supports ADHD"
        else:
            confidence = "moderate"
            reasoning = "Childhood onset reported but needs verification"
        
        # Apply cross-situational impairment
        if not impairment_eval["criterion_c_met"]:
            base_likelihood *= 0.5  # Reduce if single-context issues
        
        # Apply differential diagnosis results
        if adhd_dep_diff["primary_diagnosis"] == "Depression":
            base_likelihood *= 0.6
        elif adhd_dep_diff["primary_diagnosis"] == "ADHD":
            base_likelihood *= 1.2
        
        if adhd_anx_diff["primary_diagnosis"] == "Anxiety":
            base_likelihood *= 0.7
        elif adhd_anx_diff["primary_diagnosis"] == "ADHD":
            base_likelihood *= 1.1
        
        # Cap at 0-1 range
        likelihood = min(max(base_likelihood, 0.0), 1.0)
        
        # Determine confidence level
        if likelihood >= 0.7 or likelihood <= 0.3:
            final_confidence = "high"
        else:
            final_confidence = "moderate"
        
        return DiagnosticLikelihood(
            likelihood=likelihood,
            confidence=final_confidence,
            key_factors=[
                f"ASRS screening: {scale_scores.asrs_interpretation}",
                f"Childhood onset: {childhood_eval['interpretation']}",
                f"Cross-situational impairment: {impairment_eval['interpretation']}"
            ],
            clinical_interpretation=self._interpret_likelihood(likelihood, "ADHD")
        )
    
    def _calculate_depression_likelihood(
        self,
        scale_scores: ScaleScores,
        adhd_dep_diff: Dict[str, Any]
    ) -> DiagnosticLikelihood:
        """Calculate depression likelihood."""
        # Base on PHQ-9 score
        if scale_scores.phq9_total >= 15:
            base_likelihood = 0.80
        elif scale_scores.phq9_total >= 10:
            base_likelihood = 0.65
        elif scale_scores.phq9_total >= 5:
            base_likelihood = 0.40
        else:
            base_likelihood = 0.10
        
        # Apply differential diagnosis
        if adhd_dep_diff["primary_diagnosis"] == "Depression":
            base_likelihood *= 1.3
        elif adhd_dep_diff["primary_diagnosis"] == "ADHD":
            base_likelihood *= 0.6
        
        likelihood = min(max(base_likelihood, 0.0), 1.0)
        
        confidence = "high" if likelihood >= 0.7 or likelihood <= 0.3 else "moderate"
        
        return DiagnosticLikelihood(
            likelihood=likelihood,
            confidence=confidence,
            key_factors=[
                f"PHQ-9 score: {scale_scores.phq9_total} ({scale_scores.phq9_severity})",
                f"Differential analysis: {adhd_dep_diff['primary_diagnosis']}"
            ],
            clinical_interpretation=self._interpret_likelihood(likelihood, "Depression")
        )
    
    def _calculate_anxiety_likelihood(
        self,
        scale_scores: ScaleScores,
        adhd_anx_diff: Dict[str, Any]
    ) -> DiagnosticLikelihood:
        """Calculate anxiety likelihood."""
        # Base on GAD-7 score
        if scale_scores.gad7_total >= 15:
            base_likelihood = 0.80
        elif scale_scores.gad7_total >= 10:
            base_likelihood = 0.65
        elif scale_scores.gad7_total >= 5:
            base_likelihood = 0.40
        else:
            base_likelihood = 0.10
        
        # Apply differential diagnosis
        if adhd_anx_diff["primary_diagnosis"] == "Anxiety":
            base_likelihood *= 1.3
        elif adhd_anx_diff["primary_diagnosis"] == "ADHD":
            base_likelihood *= 0.6
        
        likelihood = min(max(base_likelihood, 0.0), 1.0)
        
        confidence = "high" if likelihood >= 0.7 or likelihood <= 0.3 else "moderate"
        
        return DiagnosticLikelihood(
            likelihood=likelihood,
            confidence=confidence,
            key_factors=[
                f"GAD-7 score: {scale_scores.gad7_total} ({scale_scores.gad7_severity})",
                f"Differential analysis: {adhd_anx_diff['primary_diagnosis']}"
            ],
            clinical_interpretation=self._interpret_likelihood(likelihood, "Anxiety")
        )
    
    def _interpret_likelihood(self, likelihood: float, condition: str) -> str:
        """Generate human-readable interpretation of likelihood."""
        if likelihood >= 0.75:
            return f"High likelihood of {condition} - strong evidence from multiple sources"
        elif likelihood >= 0.60:
            return f"Moderate-high likelihood of {condition} - consistent pattern observed"
        elif likelihood >= 0.40:
            return f"Moderate likelihood of {condition} - mixed evidence"
        elif likelihood >= 0.25:
            return f"Low-moderate likelihood of {condition} - some evidence present"
        else:
            return f"Low likelihood of {condition} - limited supporting evidence"
    
    def _generate_recommendations(
        self,
        pattern: DiagnosticPattern,
        adhd_likelihood: DiagnosticLikelihood,
        depression_likelihood: DiagnosticLikelihood,
        anxiety_likelihood: DiagnosticLikelihood,
        scale_scores: ScaleScores,
        childhood_eval: Dict[str, Any]
    ) -> List[ClinicalRecommendation]:
        """Generate clinical recommendations based on evaluation."""
        recommendations = []
        
        # Always recommend professional evaluation
        recommendations.append(ClinicalRecommendation(
            priority="high",
            category="evaluation",
            title="Professional Evaluation Recommended",
            description="This screening suggests you may benefit from a comprehensive evaluation by a mental health professional (psychiatrist, psychologist, or specialized clinician).",
            rationale="Screening tools provide preliminary information but cannot replace clinical diagnosis."
        ))
        
        # ADHD-specific recommendations
        if adhd_likelihood.likelihood >= 0.5:
            if not childhood_eval["criterion_b_met"]:
                recommendations.append(ClinicalRecommendation(
                    priority="high",
                    category="diagnostic_clarification",
                    title="Childhood History Needs Clarification",
                    description="Your current symptoms suggest ADHD, but childhood onset information is unclear. Bring school report cards, speak with parents, or recall childhood difficulties.",
                    rationale="DSM-5-TR requires childhood onset for ADHD diagnosis."
                ))
            else:
                recommendations.append(ClinicalRecommendation(
                    priority="high",
                    category="specialist_referral",
                    title="ADHD Specialist Evaluation",
                    description="Consider evaluation by a clinician experienced in adult ADHD (psychiatrist, clinical psychologist, or ADHD specialist).",
                    rationale="Pattern consistent with possible ADHD."
                ))
        
        # Depression recommendations
        if depression_likelihood.likelihood >= 0.6:
            if scale_scores.phq9_total >= 15:
                recommendations.append(ClinicalRecommendation(
                    priority="high",
                    category="urgent_care",
                    title="Significant Depressive Symptoms",
                    description="Your depression screening suggests moderate-severe symptoms. Consider seeking evaluation soon, especially if symptoms are worsening or affecting daily functioning.",
                    rationale="PHQ-9 score indicates clinically significant depression."
                ))
            else:
                recommendations.append(ClinicalRecommendation(
                    priority="moderate",
                    category="treatment",
                    title="Depression Treatment Options",
                    description="Discuss treatment options with a mental health provider. Evidence-based treatments include therapy (CBT, IPT) and/or medication.",
                    rationale="Depressive symptoms are present and may benefit from treatment."
                ))
        
        # Anxiety recommendations
        if anxiety_likelihood.likelihood >= 0.6:
            recommendations.append(ClinicalRecommendation(
                priority="moderate",
                category="treatment",
                title="Anxiety Management",
                description="Consider anxiety-focused treatment such as Cognitive Behavioral Therapy (CBT) or medication evaluation with a psychiatrist.",
                rationale="Significant anxiety symptoms detected."
            ))
        
        # Comorbidity recommendations
        if (adhd_likelihood.likelihood >= 0.5 and 
            (depression_likelihood.likelihood >= 0.5 or anxiety_likelihood.likelihood >= 0.5)):
            recommendations.append(ClinicalRecommendation(
                priority="high",
                category="comprehensive_care",
                title="Multiple Conditions May Be Present",
                description="Your screening suggests possible ADHD along with depression and/or anxiety. This is common - about 50% of adults with ADHD have comorbid mood/anxiety disorders. Comprehensive treatment addressing all conditions is important.",
                rationale="Comorbid conditions require integrated treatment approach."
            ))
        
        return recommendations
    
    def _generate_clinical_reasoning(
        self,
        scale_scores: ScaleScores,
        childhood_eval: Dict[str, Any],
        impairment_eval: Dict[str, Any],
        adhd_dep_diff: Dict[str, Any],
        adhd_anx_diff: Dict[str, Any],
        pattern: DiagnosticPattern
    ) -> str:
        """Generate human-readable clinical reasoning explanation."""
        reasoning_parts = []
        
        reasoning_parts.append("## Clinical Assessment Summary\n")
        
        reasoning_parts.append("### Screening Scale Results\n")
        reasoning_parts.append(f"- **ASRS (ADHD)**: {scale_scores.asrs_interpretation}\n")
        reasoning_parts.append(f"- **PHQ-9 (Depression)**: {scale_scores.phq9_severity}\n")
        reasoning_parts.append(f"- **GAD-7 (Anxiety)**: {scale_scores.gad7_severity}\n\n")
        
        reasoning_parts.append("### Diagnostic Criteria Analysis\n")
        reasoning_parts.append(f"**Childhood Onset (DSM Criterion B)**: {childhood_eval['interpretation']}\n\n")
        reasoning_parts.append(f"**Cross-Situational Impairment (Criterion C)**: {impairment_eval['interpretation']}\n\n")
        
        reasoning_parts.append("### Differential Diagnosis Considerations\n")
        reasoning_parts.append(f"**ADHD vs Depression**: Primary pattern suggests {adhd_dep_diff['primary_diagnosis']} ")
        reasoning_parts.append(f"(confidence: {adhd_dep_diff['confidence']})\n\n")
        reasoning_parts.append(f"**ADHD vs Anxiety**: Primary pattern suggests {adhd_anx_diff['primary_diagnosis']} ")
        reasoning_parts.append(f"(confidence: {adhd_anx_diff['confidence']})\n\n")
        
        reasoning_parts.append("### Overall Clinical Pattern\n")
        reasoning_parts.append(f"Pattern identified: **{pattern.value}**\n\n")
        
        reasoning_parts.append("### Important Notes\n")
        reasoning_parts.append("- This screening provides preliminary information only\n")
        reasoning_parts.append("- Formal diagnosis requires comprehensive clinical evaluation\n")
        reasoning_parts.append("- Multiple conditions can co-occur\n")
        reasoning_parts.append("- Treatment should be individualized based on full assessment\n")
        
        return "".join(reasoning_parts)
    
    def _get_disclaimer(self) -> str:
        """Return standard clinical disclaimer."""
        return (
            "**IMPORTANT DISCLAIMER**: This screening tool is for educational and informational "
            "purposes only. It is NOT a diagnostic instrument and cannot replace a comprehensive "
            "evaluation by a qualified mental health professional. If you are experiencing "
            "distress, difficulty functioning, or thoughts of self-harm, please seek immediate "
            "professional help. Contact a mental health provider, your primary care physician, "
            "or crisis services if needed."
        )
