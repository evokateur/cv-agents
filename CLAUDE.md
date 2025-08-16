# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Setup

```bash
# Create and activate virtual environment
./setup.sh

# Or manually:
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Copy environment variables and configure
cp sample.env .env
# Edit .env with your API keys
```

## Common Commands

```bash
# Generate CV from YAML data
make cv

# Generate cover letter
make cover-letter

# Run tests
make test
# Or: pytest --tb=short

# Clean build artifacts
make clean
```

## Architecture Overview

This is a dual-purpose CV generation system:

1. **Template-based CV generation**: Converts YAML/JSON data to LaTeX via Jinja templates
2. **AI-powered CV optimization**: Uses CrewAI agents to analyze job postings and optimize CVs

### Core Components

- **Data Layer**: `data/cv.yaml` contains CV information following the schema in `data/cv-schema.json`
- **Template Engine**: `texenv/jinja.py` provides LaTeX-compatible Jinja environment with custom delimiters: `(# #)` for statements, `(( ))` for expressions, `%( )%` for comments
- **CV Generation**: `make-cv.py` renders YAML data through `templates/cv.tex` template
- **AI Optimization System**: `optimizer/` contains CrewAI-based agents for job analysis and CV optimization

### AI Optimization Components

- **Agents**: Three specialized AI agents in `optimizer/agents/`:
  - `job_analyst.py`: Extracts job requirements from postings
  - `candidate_profiler.py`: Analyzes candidate background
  - `cv_strategist.py`: Creates optimization strategies
- **Tasks**: Corresponding tasks in `optimizer/tasks/` define agent workflows
- **Models**: Pydantic models in `optimizer/models.py` for structured data (JobPosting, CandidateProfile, CurriculumVitae)
- **Configuration**: `config.py` manages environment-based settings for different AI models

### Data Flow

1. Job posting URL → Job Analyst → Structured job requirements
2. Candidate data + Job requirements → Candidate Profiler → Profile analysis  
3. Profile + Job requirements → CV Strategist → Optimization recommendations
4. Optimized data → Template engine → LaTeX → PDF

## Testing

Tests use pytest with configuration in `pytest.ini`. Run specific test files:
```bash
pytest tests/unit/optimizer/tasks/test_job_analysis_task.py
```

## Environment Variables

Configure in `.env` (copy from `sample.env`):
- API keys for various LLM providers (Anthropic, OpenAI, DeepSeek, Google)
- `SERPER_API_KEY` for web search functionality
- Model configuration for each agent (model name and temperature)

## Key Dependencies

- **CrewAI**: Multi-agent AI framework
- **Jinja2**: Template engine with LaTeX escaping
- **Pydantic**: Data validation and serialization
- **LangChain**: Vector database and embeddings via Chroma
- **PyYAML**: Configuration file parsing