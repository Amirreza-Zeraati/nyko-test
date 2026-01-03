# Expert System Architecture - ADHD Screening System

## Overview

This document provides an in-depth explanation of the expert system's architecture, clinical reasoning logic, and implementation details.

## System Architecture

### 1. Knowledge Base Layer

The knowledge base encodes clinical expertise from multiple sources:

#### A. DSM-5-TR Diagnostic Criteria (`dsm5_criteria.py`)

**ADHD Criteria**:
- **Criterion A1**: 9 inattention symptoms with weighted importance
- **Criterion A2**: 9 hyperactivity-impulsivity symptoms
- **Criterion B**: Childhood onset (age < 12) - REQUIRED
- **Criterion C**: Cross-situational impairment - REQUIRED
- **Criterion D**: Functional impairment threshold
- **Criterion E**: Not better explained by another disorder

**Weight System**:
```python
# Example: Distraction is highly characteristic of ADHD
weight = 1.3  # Higher than baseline 1.0

# Talking excessively is less specific
weight = 0.8  # Lower weight
```

**Depression Criteria**:
- Core symptoms: depressed mood, anhedonia (high weight)
- Vegetative symptoms: sleep, appetite, energy
- Cognitive symptoms: concentration (mood-dependent)
- Temporal pattern: episodic (2+ weeks)

**Anxiety Criteria**:
- Excessive worry (content-specific)
- Physical symptoms: tension, restlessness
- Cognitive: worry-driven concentration issues

#### B. Clinical Rules (`clinical_rules.py`)

Expert heuristics for differential diagnosis:

**Rule 1: Childhood Onset Evaluation**
```python
if age_of_onset > 12:
    adhd_likelihood *= 0.0  # Eliminates primary ADHD
    interpretation = "Adult onset rules out ADHD"
else if age_of_onset <= 7:
    adhd_likelihood *= 1.5  # Strong evidence
    interpretation = "Early onset supports ADHD"
```

**Rule 2: Temporal Pattern Analysis**
```python
if lifelong_symptoms and episodic_symptoms:
    # Complex presentation - comorbidity likely
    confidence = "moderate"
else if lifelong_symptoms:
    # Favors ADHD over mood/anxiety
    adhd_weight += 2.0
```

**Rule 3: Thought Content Analysis**
```python
if mind_random_thoughts > worry_content:
    # ADHD: mind wanders randomly
    adhd_weight += 1.5
else if worry_content > random_thoughts:
    # Anxiety: worry-focused attention
    anxiety_weight += 1.5
```

### 2. Inference Engine Layer

The inference engine applies rules and calculates likelihoods:

#### A. Scoring Service (`scoring.py`)

**ASRS Calculation**:
```python
# Part A (screening): 6 items
# Threshold: 4+ items scored ≥ 2 ("Sometimes" or higher)
if part_a_threshold >= 4:
    interpretation = "Highly consistent with ADHD"
```

**PHQ-9 Interpretation**:
```python
if score >= 20: return "Severe depression"
elif score >= 15: return "Moderately severe"
elif score >= 10: return "Moderate"
elif score >= 5: return "Mild"
else: return "Minimal/none"
```

#### B. Expert System (`expert_system.py`)

**Likelihood Calculation Algorithm**:

```python
def calculate_adhd_likelihood():
    # Step 1: Base likelihood from ASRS
    if asrs_part_a >= 4:
        base = 0.75  # High screening score
    else:
        base = 0.15  # Low screening score
    
    # Step 2: Apply childhood onset (CRITICAL)
    if not childhood_onset_before_12:
        base *= 0.2  # Massive reduction
    
    # Step 3: Cross-situational impairment
    if single_context_only:
        base *= 0.5  # Reduce likelihood
    
    # Step 4: Differential diagnosis
    if depression_primary:
        base *= 0.6
    
    # Step 5: Cap at [0, 1]
    return min(max(base, 0.0), 1.0)
```

**Pattern Recognition**:

```python
if adhd_likelihood >= 0.7:
    if depression_likelihood >= 0.5:
        return "ADHD with comorbid depression"
    else:
        return "ADHD predominant"
elif depression_likelihood >= 0.7:
    return "Depression predominant"
```

### 3. Explanation Generator

Generates human-readable clinical reasoning:

```python
def generate_reasoning():
    reasoning = []
    
    # Scale scores
    reasoning.append(f"ASRS: {interpretation}")
    reasoning.append(f"PHQ-9: {severity}")
    
    # Diagnostic criteria
    reasoning.append(f"Childhood onset: {criterion_b_result}")
    reasoning.append(f"Cross-situational: {criterion_c_result}")
    
    # Differential diagnosis
    reasoning.append(f"ADHD vs Depression: {primary_pattern}")
    
    # Overall pattern
    reasoning.append(f"Pattern: {diagnostic_pattern}")
    
    return "\n".join(reasoning)
```

## Clinical Reasoning Strategies

### Strategy 1: Criterion-Based Filtering

**Implementation**:
1. Check REQUIRED criteria first (B, C, D)
2. If any required criterion fails, adjust likelihood dramatically
3. Only proceed with full evaluation if criteria met

**Example**:
```python
if not childhood_onset:
    return {
        "adhd_likelihood": 0.0,
        "reasoning": "DSM-5-TR Criterion B not met - adult onset excludes primary ADHD"
    }
```

### Strategy 2: Differential Diagnosis Logic

**ADHD vs Depression**:

| Feature | ADHD | Depression |
|---------|------|------------|
| Temporal | Lifelong | Episodic |
| Onset | Childhood | Adolescence/adult |
| Mood | Variable | Persistently low |
| Concentration | Always impaired | Mood-dependent |
| Interest | Can focus if interested | Anhedonia |
| Physical | Restless (energized) | Fatigued |

**Implementation**:
```python
if lifelong_pattern and childhood_onset:
    adhd_weight += 3.0
if anhedonia and persistent_sadness:
    depression_weight += 3.0
```

### Strategy 3: Weighted Evidence Accumulation

**Concept**: Not all symptoms are equally diagnostic

```python
# Highly specific for ADHD
if easily_distracted:
    adhd_score += 1.3

# Less specific (common in anxiety too)
if restless:
    adhd_score += 0.8
```

### Strategy 4: Comorbidity Detection

**Logic**:
```python
if adhd_likelihood > 0.5 and depression_likelihood > 0.5:
    pattern = "Comorbid ADHD + Depression"
    recommendation = "Treat both conditions - ADHD first, then depression"
```

**Clinical Rationale**:
- 50-70% of adults with ADHD have comorbid conditions
- Depression may be secondary to ADHD-related failures
- Anxiety may result from executive dysfunction
- Treatment approach differs based on primary vs secondary

## Advanced Features

### 1. Confidence Estimation

```python
def estimate_confidence(likelihood, supporting_evidence):
    if likelihood >= 0.7 or likelihood <= 0.3:
        # Strong evidence in one direction
        return "high"
    elif conflicting_evidence:
        return "low"
    else:
        return "moderate"
```

### 2. Uncertainty Handling

```python
if childhood_onset_unclear:
    reasoning.append(
        "Childhood history unclear - recommend collateral information"
    )
    confidence = "moderate"  # Downgrade confidence
```

### 3. Context-Aware Interpretation

```python
if work_impairment_high and home_impairment_low:
    reasoning.append(
        "Single-context impairment suggests situational stress, "
        "not ADHD. Consider workplace evaluation."
    )
```

## Validation and Testing

### Clinical Validity

**Sensitivity/Specificity Balance**:
- High sensitivity: Catch most true ADHD cases (minimize false negatives)
- Adequate specificity: Avoid over-diagnosing (minimize false positives)
- Trade-off: Screening tool prioritizes sensitivity

**Comparison with Clinical Diagnosis**:
```
Agreement with expert clinicians: Target 75-85%
ASRS alone: ~70%
ASRS + developmental history: ~80%
Full expert system: Target ~85%
```

### Technical Validation

**Unit Tests**:
```python
def test_childhood_onset_rule():
    response = {"symptom_onset_age": 18}
    result = evaluate_childhood_onset(response)
    assert result["criterion_b_met"] == False
    assert result["onset_score"] == 0.0
```

**Integration Tests**:
```python
def test_adhd_predominant_pattern():
    # Simulate clear ADHD case
    responses = {...}  # High ASRS, low PHQ-9/GAD-7
    result = expert_system.evaluate(responses, ...)
    assert result.adhd_likelihood.likelihood > 0.7
    assert "ADHD" in result.primary_pattern
```

## Limitations and Future Work

### Current Limitations

1. **No Collateral Information**: Relies on self-report only
2. **No Objective Testing**: No performance-based measures
3. **Cultural Factors**: May not account for cultural presentation differences
4. **Symptom Validity**: Cannot detect intentional misrepresentation

### Planned Enhancements

1. **Machine Learning Integration**: Train on clinical dataset
2. **Natural Language Processing**: Analyze free-text responses
3. **Temporal Analysis**: Track symptom changes over time
4. **Collateral Input**: Allow input from family/friends
5. **Performance Tests**: Integrate CPT or similar objective measures

## References

### Clinical Literature

1. **Kessler RC et al. (2005)**. "The World Health Organization Adult ADHD Self-Report Scale (ASRS)". *Psychological Medicine*, 35(2), 245-256.

2. **Sobanski E. (2006)**. "Psychiatric comorbidity in ADHD - a neurobiological and psychopathological perspective". *European Child & Adolescent Psychiatry*, 15(Suppl 1), I5-I18.

3. **Matte B et al. (2015)**. "Differential diagnosis of the attention deficit hyperactivity disorder in adults". *Trends in Psychiatry and Psychotherapy*, 37(1), 47-52.

### Diagnostic Guidelines

1. **APA (2022)**. *Diagnostic and Statistical Manual of Mental Disorders* (5th ed., text rev.).

2. **NICE (2018)**. *Attention deficit hyperactivity disorder: diagnosis and management*. National Institute for Health and Care Excellence guideline [NG87].

3. **CADDRA (2020)**. *Canadian ADHD Practice Guidelines* (4th ed.).

### Technical Implementation

1. **Russell S, Norvig P (2020)**. *Artificial Intelligence: A Modern Approach* (4th ed.). Expert systems chapter.

2. **Shortliffe EH (1976)**. *Computer-Based Medical Consultations: MYCIN*. Foundational work on medical expert systems.

## Conclusion

This expert system synthesizes:
- Evidence-based clinical criteria (DSM-5-TR)
- Validated assessment instruments (ASRS, PHQ-9, GAD-7)
- Expert clinical reasoning patterns
- Differential diagnosis heuristics

The goal is to provide a **clinically informed screening tool** that:
1. Identifies individuals who may benefit from professional evaluation
2. Helps differentiate between overlapping presentations
3. Educates users about diagnostic complexity
4. Reduces misdiagnosis and inappropriate treatment

**This tool augments, not replaces, clinical judgment.**
