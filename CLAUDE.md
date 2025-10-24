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

### CV Optimization Testing

- `make cv_alignment` - Test CV alignment task with job posting analysis
- `make cv_transformation` - Test CV transformation task using pre-generated alignment output
- `make job_analysis` - Test job analysis functionality
- `make cv_analysis` - Test CV analysis agent with CV parsing
- `make cv_optimization` - Run CV optimization with default configuration
- `make vector_db` - Rebuild the ChromaDB vector database from knowledge base content (runs `scripts/embed_kb.py`)

### Development Setup

- `./setup.sh` - Create virtual environment, install dependencies, and set up Jupyter kernel
- `source .venv/bin/activate` - Activate virtual environment
- `pip install -e .` - Install package with dependencies from pyproject.toml
- `pip freeze > requirements.txt` - Update requirements.txt after adding new dependencies
- `jupyter lab` - Start Jupyter Lab to run the cv-agents.ipynb notebook for experimentation

### Running the CV Optimization Crew

- `optimize-cv --config_path config.json` - Run crew with JSON config file (console script from pyproject.toml)
- `optimize-cv --config '{"inputs": {...}}'` - Run crew with inline JSON config
- `python -m scripts.cv_optimization` - Simple test runner with hardcoded inputs

### Knowledge Base Utilities

- `python -m scripts.embed_kb` - Rebuild ChromaDB vector database from knowledge base content
- `python -m scripts.query_kb [query]` - Query knowledge base using semantic search (optional query parameter)
- `python -m scripts.inspect_chroma` - Inspect ChromaDB vector database contents
- `python -m scripts.chroma_test` - Test ChromaDB functionality

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

- `src/builder/` - CV and cover letter generation module
  - `cli.py` - Console scripts entry point (make-cv, make-cover-letter commands)
  - `builder.py` - Unified build logic that loads YAML/JSON data and renders LaTeX templates for any document type
  - `template_env.py` - Custom Jinja2 environment with LaTeX-safe delimiters and escaping
- `data/cv.yaml` - Primary CV data source
- `templates/cv.tex` - LaTeX CV template with custom Jinja2 delimiters
- `templates/cover-letter.tex` - LaTeX cover letter template

**AI-Powered CV Optimization:**

- `src/optimizer/` - CrewAI-based system for job-specific CV optimization following recommended project structure
  - `crew.py` - Main crew class with @CrewBase decorator using hybrid YAML/Python configuration
  - `agents.py` - Agent implementations with RAG tool integration, loads YAML configurations from `config/agents.yaml`
  - `tasks.py` - Task implementations with RAG prompting, loads YAML configurations from `config/tasks.yaml`
  - `config/agents.yaml` - YAML agent configurations (job_analyst, cv_analyst, cv_strategist, cv_rewriter)
  - `config/tasks.yaml` - YAML task configurations with dependencies and RAG tool instructions
  - `config/settings.py` - Environment-based configuration for AI model settings
  - `models.py` - Pydantic models for job postings, CV transformation plans, and CV structure
  - `tools/` - Custom CrewAI tool implementations:
    - `semantic_search_tool.py` - Original RAG tool for semantic search
    - `chunky_rag_tool.py` - Enhanced RAG tool with LLM synthesis
    - `chunky_kb_tool.py` - Standalone knowledge base query tool
    - `semantic_search_wrapper.py` - Clean output formatter for LLM-synthesized results
  - `utils/` - Vector database utilities, prompt utilities, and RAG tool management
  - `embedder.py` - Knowledge base embedding and ChromaDB management
  - `logging/console_capture.py` - Console output capture with ANSI code stripping for log files
  - `cli.py` - Command-line interface for optimize-cv console script
- `src/models/schema.py` - Shared Pydantic models and CV schema definitions
- `scripts/` - Individual test scripts for each crew component and knowledge base utilities

**Configuration:**

- `pyproject.toml` - Package configuration with dependencies and console scripts (defines make-cv, make-cover-letter, optimize-cv)
- `sample.env` - Template for required environment variables
- `src/optimizer/config/settings.py` - AI model settings loaded from environment variables
- Required environment variables per agent:
  - CV_ANALYST_MODEL, CV_ANALYST_TEMPERATURE
  - JOB_ANALYST_MODEL, JOB_ANALYST_TEMPERATURE
  - CV_STRATEGIST_MODEL, CV_STRATEGIST_TEMPERATURE
  - CV_REWRITER_MODEL, CV_REWRITER_TEMPERATURE
  - CREW_MANAGER_MODEL, CREW_MANAGER_TEMPERATURE
  - KNOWLEDGE_BASE_PATH (defaults to "knowledge-base")
  - VECTOR_DB_PATH (defaults to "vector_db")
- Requires API keys for various providers (Anthropic, OpenAI, Google, DeepSeek, Serper)

### Template System

Uses custom Jinja2 delimiters to avoid LaTeX conflicts (defined in src/builder/template_env.py:24):

- Statements: `(# #)` instead of `{% %}`
- Expressions: `(( ))` instead of `{{ }}`
- Comments: `%( )%` instead of `{# #}`
- Line comments: `%%` instead of `##`

LaTeX special characters are automatically escaped via the `escape_tex` filter to prevent rendering errors.

### Data Flow

1. **Simple Build**: YAML/JSON data → unified builder → Jinja2 template → LaTeX → PDF
2. **AI Optimization**: Job posting → Job analysis → CV alignment planning → CV optimization → unified builder → Template → PDF
3. **RAG-Enhanced Optimization**: Job posting → AI analysis with RAG tool → Knowledge-informed CV transformation → unified builder → Template → PDF
4. **LLM Synthesis RAG**: Job posting → AI analysis with chunky tools → LLM-synthesized knowledge retrieval → CV transformation planning → CV optimization → unified builder → Template → PDF
5. **Vector Database**: Knowledge base content stored in `vector_db/` using ChromaDB with automatic embedding and retrieval

### Crew Architecture Details

The main CvOptimization crew uses a hybrid parallel/sequential execution pattern:

1. **Parallel Tasks** (async_execution=True): cv_analysis_task and job_analysis_task run concurrently
2. **Sequential Tasks**: cv_alignment_task waits for both parallel tasks, then cv_transformation_task executes last

Testing uses FakeAgents/FakeTasks pattern (src/optimizer/fakers.py:7) to load pre-generated outputs from files, allowing isolated testing of individual tasks without running full pipeline.

Specialized crew classes for testing individual components:
- CvAnalysis - runs only CV analysis task
- JobAnalysis - runs only job analysis task
- CvAlignment - runs CV alignment with fake upstream outputs
- CvTransformation - runs CV transformation with fake upstream outputs

### Testing

- Uses pytest with custom markers (`unit`, `integration`, `slow`)
- Test structure mirrors source code in `tests/unit/optimizer/`
- Configuration in `pytest.ini` with verbose output and short tracebacks
- Filters Pydantic deprecation warnings for cleaner test output
- Individual crew testing scripts in `scripts/` directory for isolated testing:
  - `cv_optimization.py` - Main CV agents test runner with hardcoded inputs
  - `cv_alignment.py` - Test CV alignment task with job posting analysis
  - `cv_transformation.py` - Test CV transformation task using pre-generated outputs
  - `cv_analysis.py` - Test CV analysis agent with CV parsing
  - `job_analysis.py` - Test job analysis functionality independently
  - `embed_kb.py` - Rebuild vector database using embedder
  - `query_kb.py` - Query knowledge base using SemanticSearchWrapper (accepts optional query argument)
  - `chroma_test.py` - ChromaDB testing utilities
  - `inspect_chroma.py` - Vector database inspection tools

### RAG Tool Architecture

The system provides multiple RAG tool implementations:

1. **SemanticSearchTool** - Basic vector similarity search returning raw chunks
2. **ChunkyRagTool** - Enhanced RAG with LLM synthesis of retrieved chunks
3. **ChunkyKnowledgeBaseTool** - Standalone KB query tool with LLM synthesis
4. **SemanticSearchWrapper** (src/optimizer/tools/semantic_search_wrapper.py:17) - Wraps ChunkyRagTool to provide clean, agent-friendly output format with sources

All RAG settings are centrally configured via get_rag_config() in settings.py.

### Key Files

- `src/builder/template_env.py` - Custom Jinja2 environment with LaTeX escaping functions
- `src/optimizer/crew.py` - Multiple crew implementations (@CrewBase decorator for main crew, plain classes for test crews)
- `src/optimizer/agents.py` - CustomAgents class loads YAML configs and initializes LLMs per agent
- `src/optimizer/tasks.py` - CustomTasks class loads YAML configs and creates task instances
- `src/optimizer/config/agents.yaml` - Agent role, goal, and backstory definitions
- `src/optimizer/config/tasks.yaml` - Task descriptions with Pydantic schema injection placeholders
- `src/optimizer/fakers.py` - FakeAgents/FakeTasks for testing with pre-generated outputs
- `src/optimizer/utils/vector_utils.py` - ChromaDB validation and vector database management utilities
- `src/optimizer/utils/prompt_utils.py` - Pydantic utilities for dynamic task descriptions (schema injection capabilities)
- `src/optimizer/logging/console_capture.py` - Console output capture with ANSI code stripping for log files
- `cv-agents.ipynb` - Jupyter notebook for experimentation and development
- `knowledge-base/` - Symlinked directory containing candidate and project information for RAG
- `vector_db/` - ChromaDB vector store with automatic embedding and retrieval capabilities
