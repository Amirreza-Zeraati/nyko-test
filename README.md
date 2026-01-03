# ADHD Screening Expert System

A sophisticated clinical decision-support web application for differential assessment of ADHD in adolescents and adults.

## Overview

This expert system combines validated clinical scales (ASRS, PHQ-9, GAD-7) with DSM-5-TR diagnostic criteria and expert clinical reasoning to:
- Screen for ADHD symptoms
- Differentiate ADHD from depression and anxiety
- Identify comorbid presentations
- Provide evidence-based recommendations

## Architecture

### Expert System Components

**Knowledge Base** (`app/knowledge_base/`):
- `dsm5_criteria.py` - DSM-5-TR diagnostic criteria for ADHD, depression, anxiety
- `clinical_rules.py` - Expert reasoning rules and differential diagnosis logic
- `scales.py` - Validated clinical assessment instruments (ASRS, PHQ-9, GAD-7)

**Inference Engine** (`app/services/expert_system.py`):
- Rule-based reasoning
- Bayesian-inspired likelihood calculation
- Pattern matching and classification
- Clinical reasoning explanation generation

**Supporting Services** (`app/services/`):
- `scoring.py` - Clinical scale score calculation and interpretation
- `session_manager.py` - User session and state management

### Web Application

**Backend** (FastAPI):
- `app/main.py` - Application entry point
- `app/routes/` - API endpoints for registration, questionnaire, evaluation
- `app/models/` - Pydantic data models

**Frontend**:
- `app/templates/` - Jinja2 HTML templates
- `static/css/` - Stylesheets
- `static/js/` - Client-side JavaScript

## Clinical Approach

The system implements expert-level diagnostic reasoning:

### 1. Validated Screening Scales
- **ASRS v1.1**: 18-item ADHD symptom checklist
- **PHQ-9**: Depression severity assessment
- **GAD-7**: Anxiety severity assessment

### 2. DSM-5-TR Criteria Application
- **Criterion A**: Symptom count and severity
- **Criterion B**: Childhood onset (CRITICAL for ADHD)
- **Criterion C**: Cross-situational impairment
- **Criterion D**: Functional impairment threshold
- **Criterion E**: Differential diagnosis

### 3. Differential Diagnosis Logic

**ADHD vs Depression**:
- Temporal pattern: lifelong (ADHD) vs episodic (depression)
- Mood symptoms: anhedonia, sadness, guilt
- Concentration: consistent (ADHD) vs mood-dependent (depression)

**ADHD vs Anxiety**:
- Thought content: random wandering (ADHD) vs worry-focused (anxiety)
- Restlessness: need for movement (ADHD) vs nervous energy (anxiety)
- Physical symptoms: tension, racing heart (anxiety)

### 4. Pattern Recognition
- ADHD predominant
- Depression predominant
- Anxiety predominant
- Comorbid presentations
- Subclinical/unclear patterns

## Installation

```bash
# Clone repository
git clone https://github.com/Amirreza-Zeraati/nyko-test.git
cd nyko-test

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your configuration

# Run application
uvicorn app.main:app --reload
```

Access at: `http://localhost:8000`

## Usage Flow

1. **Registration** (`/`)
   - User provides basic information
   - Session created

2. **Questionnaire** (`/questionnaire`)
   - Multi-page assessment (5 pages)
   - ADHD symptoms, depression, anxiety, developmental history
   - Progress tracked

3. **Evaluation** (`/api/evaluation/result`)
   - Expert system analyzes responses
   - Calculates diagnostic likelihoods
   - Generates clinical reasoning
   - Provides recommendations

4. **Results**
   - Visual likelihood meters
   - Scale scores
   - Clinical reasoning explanation
   - Prioritized recommendations
   - Medical disclaimer

## API Endpoints

### Registration
- `POST /api/registration/start` - Create new session

### Questionnaire
- `GET /api/questionnaire/page/{page_num}` - Get questions for page
- `POST /api/questionnaire/submit` - Submit all responses

### Evaluation
- `GET /api/evaluation/result` - View results page
- `POST /api/evaluation/analyze` - Run expert system analysis

## Key Features

### Clinical Excellence
- Evidence-based diagnostic criteria
- Expert clinical reasoning patterns
- Common misdiagnosis prevention
- Contextual interpretation

### Technical Quality
- Type-safe with Pydantic models
- Async/await for performance
- Session-based state management
- RESTful API design

### User Experience
- Clean, intuitive interface
- Progress tracking
- Mobile-responsive
- Accessible design

## Important Notes

### Medical Disclaimer
This tool is for **screening and educational purposes only**. It does NOT:
- Provide medical diagnoses
- Replace professional evaluation
- Offer treatment recommendations
- Constitute medical advice

Users experiencing distress or functional impairment should consult qualified mental health professionals.

### Ethical Considerations
- Privacy: Session data is temporary
- Transparency: Reasoning is explained
- Uncertainty: Confidence levels provided
- Limitations: Clearly communicated

## Development

### Project Structure
```
nyko-test/
├── app/
│   ├── knowledge_base/      # Clinical knowledge
│   ├── models/              # Data models
│   ├── routes/              # API endpoints
│   ├── services/            # Business logic
│   ├── templates/           # HTML templates
│   └── main.py              # Entry point
├── static/
│   ├── css/                 # Stylesheets
│   └── js/                  # JavaScript
├── requirements.txt
└── README.md
```

### Testing
```bash
# Run tests (when implemented)
pytest tests/

# Type checking
mypy app/

# Code formatting
black app/
```

## Future Enhancements

- PDF report generation
- Multi-language support
- Clinician dashboard
- Database persistence
- Advanced analytics
- Treatment tracking

## References

### Clinical Guidelines
- American Psychiatric Association. (2022). DSM-5-TR
- WHO. Adult ADHD Self-Report Scale (ASRS v1.1)
- Kroenke et al. (2001). PHQ-9 validation study
- Spitzer et al. (2006). GAD-7 validation study

### Research
- Kessler RC et al. (2005). ADHD in adults
- Sobanski E. (2006). Psychiatric comorbidity in ADHD
- Research on ADHD-depression-anxiety differentiation

## License

For educational and research purposes.

## Contact

Developed by: Amirreza Zeraati
GitHub: [@Amirreza-Zeraati](https://github.com/Amirreza-Zeraati)

---

**⚠️ This is a screening tool, not a diagnostic instrument. Always consult qualified healthcare professionals for proper evaluation and treatment.**
