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
- `jupyter lab` - Start Jupyter Lab to run the cv-agents.ipynb notebook for experimentation

### Running the CV Optimization Crew

- `python kickoff_crew.py --config_path config.json` - Run crew with JSON config file
- `python kickoff_crew.py --config '{"inputs": {...}}'` - Run crew with inline JSON config
- `python cv_agents.py` - Simple test runner with hardcoded inputs

## Architecture

### CrewAI 

We are using the CrewAI recommended project structure with hybrid .yaml/.py Agents and Tasks

Here are some links to CrewAI documentation to help us understand the target architecture.

- **YAML Configuration for Agents and Tasks:**
  - Agents: <https://docs.crewai.com/concepts/agents#yaml-configuration-recommended>
  - Tasks: <https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended>

- **Agent Tools:**
  - <https://docs.crewai.com/concepts/agents#agent-tools>

- **Structured task output, task dependencies, and task callbacks:**
  - <https://docs.crewai.com/concepts/tasks#overview-of-a-task>

- **Adding Knowledge Sources:**
  - <https://docs.crewai.com/concepts/knowledge#what-is-knowledge>

- `@before_kickoff` and `@after_kickoff` decorators:
  - <https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators>

### Core Components

**CV Generation Pipeline:**

- `make-cv.py` - Main CV generation script that loads YAML data and renders LaTeX template
- `make-cover-letter.py` - Cover letter generation script using JSON data
- `data/cv.yaml` - Primary CV data source
- `templates/cv.tex` - LaTeX template with custom Jinja2 delimiters
- `texenv/jinja.py` - Custom Jinja2 environment with LaTeX-safe delimiters and escaping

**AI-Powered CV Optimization:**

- `optimizer/` - CrewAI-based system for job-specific CV optimization following recommended project structure
- `optimizer/crew.py` - Main crew class with @CrewBase decorator using hybrid YAML/Python configuration
- `optimizer/agents.py` - Agent implementations that load YAML configurations from `config/agents.yaml`
- `optimizer/tasks.py` - Task implementations that load YAML configurations from `config/tasks.yaml`
- `optimizer/config/agents.yaml` - YAML agent configurations (job_analyst, candidate_profiler, cv_strategist)
- `optimizer/config/tasks.yaml` - YAML task configurations with dependencies
- `optimizer/models.py` - Pydantic models for job postings, candidate profiles, and CV structure
- `optimizer/tools/` - Directory for custom CrewAI tool implementations
- `kickoff_crew.py` - Command-line interface for running the crew with JSON/YAML config
- `cv_agents.py` - Simple test script for running the crew with hardcoded inputs

**Configuration:**

- `config.py` - Environment-based configuration for AI model settings
- `sample.env` - Template for required environment variables
- Models are configurable per agent (JOB_ANALYST_MODEL, CANDIDATE_PROFILER_MODEL, etc.)
- Requires API keys for various providers (Anthropic, OpenAI, Google, DeepSeek, Serper)

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
- Filters Pydantic deprecation warnings for cleaner test output

### Key Files

- `texenv/jinja.py` - Custom Jinja2 environment with LaTeX escaping functions
- `optimizer/crew.py` - Main CrewAI crew implementation with @agent, @task, and @crew decorators
- `optimizer/config/` - YAML configuration files for agents and tasks following CrewAI best practices
- `kickoff_crew.py` - CLI entry point for running the optimization crew
- `cv-agents.ipynb` - Jupyter notebook for experimentation and development
- `knowledge-base/` - Symlinked directory containing candidate and project information for RAG
- `vector_db/` - ChromaDB vector store for knowledge base queries
