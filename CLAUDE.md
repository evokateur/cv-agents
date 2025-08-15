# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Build and Generation
- `make cv` - Generate CV from YAML data and LaTeX template, outputs to `output/cv.pdf`
- `make cover-letter` - Generate cover letter, outputs to `output/cover-letter.pdf`
- `make clean` - Remove pdflatex build artifacts from output directory

### Testing
- `make test` or `pytest --tb=short` - Run all tests
- `pytest tests/unit/` - Run unit tests only
- `pytest -k "test_name"` - Run specific test

### Environment Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Architecture

### Core Components

**CV Generation Pipeline**
- `make-cv.py` - Main script that loads YAML data and renders LaTeX template
- `texenv/jinja.py` - Custom Jinja2 environment with LaTeX-compatible delimiters
- `data/cv.yaml` - Primary CV data source
- `templates/cv.tex` - LaTeX template with custom Jinja syntax
- `data/cv-schema.json` - JSON schema defining CV data structure

**Job Analysis System (CrewAI-based)**
- `optimizer/agents/job_analyst.py` - CrewAI agent for analyzing job postings
- `optimizer/tasks/job_analysis_task.py` - Task definitions for job analysis
- `optimizer/tools/` - Vector database and CV optimization tools
- Uses LLM models configurable via environment variables

### Template System

Uses custom Jinja2 delimiters to avoid LaTeX conflicts:
- Statements: `(# #)` instead of `{% %}`
- Expressions: `(( ))` instead of `{{ }}`
- Comments: `%( )%` instead of `{# #}`
- Line comments: `%%` instead of `##`

### Data Flow
1. CV data stored in `data/cv.yaml` following `cv-schema.json`
2. `make-cv.py` loads data and renders `templates/cv.tex`
3. pdflatex compiles rendered LaTeX to PDF in `output/`
4. Job analysis agents can optimize CV content based on job postings

### Testing Structure
- `tests/unit/` - Unit tests for optimizer components
- `pytest.ini` - Test configuration with markers for unit/integration/slow tests
- Tests use standard pytest patterns without "test" in names per project conventions