# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Environment Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### CV Generation
- `make cv` - Generate CV PDF from YAML data using LaTeX template
- `make cover-letter` - Generate cover letter PDF
- `make clean` - Remove LaTeX build artifacts

### Testing
- `pytest` or `make test` - Run full test suite
- `pytest tests/unit/embedder/test_embedder.py` - Run specific test file
- `pytest -m unit` - Run only unit tests
- `pytest -m slow` - Run slow tests

## Architecture Overview

This is a CV optimization system with two main components:

### 1. CV Generation Pipeline
- **Data Layer**: `data/cv.yaml` contains structured CV content
- **Template Engine**: LaTeX templates in `templates/` with custom Jinja delimiters:
  - Statements: `(# #)` instead of `{% %}`
  - Expressions: `(( ))` instead of `{{ }}`
  - Comments: `%( )%` instead of `{# #}`
- **Output**: Generates PDFs in `output/` directory

### 2. AI-Powered CV Optimizer
Multi-agent CrewAI system that analyzes job postings and optimizes CVs:

#### Agent Architecture
- **Job Analyst** (`optimizer/agents/job_analyst.py`): Extracts requirements from job postings using web scraping tools
- **Candidate Profiler** (`optimizer/agents/candidate_profiler.py`): Searches knowledge base to build candidate profile matching job requirements  
- **CV Strategist** (`optimizer/agents/cv_strategist.py`): Optimizes CV content based on job analysis and candidate profile

#### Task Flow
1. **Job Analysis Task**: Scrapes job posting URL → structured `JobPosting` model
2. **Candidate Profiling Task**: Searches knowledge base → comprehensive `CandidateProfile` with skill matching, relevant experiences, achievements
3. **CV Optimizing Task**: Uses both previous outputs → optimized `CurriculumVitae` tailored for specific role

#### Key Models (`optimizer/models.py`)
- `JobPosting`: Structured job requirements and responsibilities
- `CandidateProfile`: Comprehensive candidate analysis with skill matching, experience relevance, and positioning strategy
- `CurriculumVitae`: Final optimized CV structure

### Knowledge Base & Embedding System
- **Embedder** (`embedding_tool/`): Creates vector embeddings of knowledge base content using OpenAI embeddings and Chroma vector store
- **Knowledge Base**: `knowledge-base/` directory contains source documents for candidate profiling
- **Vector Store**: `vector_db/` contains Chroma database for semantic search

## Configuration

Environment variables are configured via `.env` file (see `sample.env`):

### Required API Keys
- `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `SERPER_API_KEY` for various agent models and tools
- `GOOGLE_API_KEY`, `DEEPSEEK_API_KEY` for additional model options

### Agent Configuration
- `{AGENT}_MODEL`: Model name for each agent (job_analyst, candidate_profiler, cv_strategist)
- `{AGENT}_TEMPERATURE`: Temperature setting for each agent

## Data Structures

CV data follows strict schema defined in `data/cv-schema.json`. Key sections:
- Contact information and professional summary
- Experience with responsibilities as lists
- Areas of expertise organized by category
- Education and additional experience

The system maintains backwards compatibility between YAML source data and the optimized output models.