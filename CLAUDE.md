# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Building and Testing

- `make cv` - Generate CV PDF from YAML data and LaTeX template
- `make cover-letter` - Generate cover letter PDF from JSON data and LaTeX template
- `make clean` - Remove LaTeX build artifacts from output directory
- `make test` or `pytest --tb=short` - Run test suite with short traceback format
- `pytest tests/unit/` - Run only unit tests
- `pytest -m unit` - Run tests marked as unit tests
- `pytest -m slow` - Run slow tests only

### Development Setup

- `./setup.sh` - Create virtual environment, install dependencies, and set up Jupyter kernel
- `source .venv/bin/activate` - Activate virtual environment
- `pip install -r requirements.txt` - Install Python dependencies

## Architecture

### Core Components

**CV Generation Pipeline:**

- `make-cv.py` - Main CV generation script that loads YAML data and renders LaTeX template
- `make-cover-letter.py` - Cover letter generation script using JSON data
- `data/cv.yaml` - Primary CV data source
- `templates/cv.tex` - LaTeX template with custom Jinja2 delimiters
- `texenv/jinja.py` - Custom Jinja2 environment with LaTeX-safe delimiters and escaping

**AI-Powered CV Optimization:**

- `optimizer/` - CrewAI-based system for job-specific CV optimization
- `optimizer/agents/` - Specialized AI agents (job_analyst, candidate_profiler, cv_strategist)
- `optimizer/tasks/` - Task definitions for each optimization step
- `optimizer/models.py` - Pydantic models for job postings, candidate profiles, and CV structure
- `optimizer/tools/knowledge_base_rag_tool.py` - RAG tool for knowledge base queries

**Configuration:**

- `config.py` - Environment-based configuration for AI model settings
- `sample.env` - Template for required environment variables
- Models are configurable per agent (JOB_ANALYST_MODEL, CANDIDATE_PROFILER_MODEL, etc.)

### Template System

Uses custom Jinja2 delimiters to avoid LaTeX conflicts:

- Statements: `(# #)` instead of `{% %}`
- Expressions: `(( ))` instead of `{{ }}`
- Comments: `%( )%` instead of `{# #}`
- Line comments: `%%` instead of `##`

### Data Flow

1. **Simple Generation**: YAML data → Jinja2 template → LaTeX → PDF
2. **AI Optimization**: Job posting → AI analysis → Optimized CV data → Template → PDF
3. **Vector Database**: Knowledge base content stored in `vector_db/` using ChromaDB

### Testing

- Uses pytest with custom markers (`unit`, `integration`, `slow`)
- Test structure mirrors source code in `tests/unit/optimizer/`
- Configuration in `pytest.ini` with verbose output and short tracebacks

