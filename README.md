# CV Generator/Optimizer

Generates a LaTeX CV from JSON/YAML data using a Jinja2 environment that plays well with LaTeX.

Custom delimiters, you see..

|              | customized | standard jinja2 |
| ------------ | ---------- | --------------- |
| Statements   | `(# #)`    | `{% %}`         |
| Expressions  | `(( ))`    | `{{ }}`         |
| Comments     | `%( )%`    | `{# #}`         |
| Line Comment | `%%`       | `##`            |

---

It also uses CrewAI Agents & Tasks to optimize CV data for job postings with RAG-enhanced knowledge retrieval

```
Job posting URL ──┐
                  ├─→ CV Alignment Task → CV Transformation Task → Optimized CV
Candidate CV ─────┘
```

The system uses four specialized agents working across parallel and sequential tasks:

- **Job Analyst**: Analyzes job postings and extracts structured requirements (parallel)
- **CV Analyst**: Parses and structures candidate CV data (parallel)
- **CV Strategist**: Creates alignment plans using RAG tools to query candidate knowledge base (sequential)
- **CV Rewriter**: Applies optimization plans and restructures CV content (sequential)

Pydantic models define the structure throughout the pipeline. The CV output conforms to the [schema](https://github.com/evokateur/cv-agents/blob/main/data/cv-schema.json) expected by the LaTeX generator.

Abridged project directory structure:

```
.
├── pyproject.toml
├── src
│   ├── builder
│   │   ├── cli.py
│   │   ├── builder.py
│   │   └── template_env.py
│   ├── models
│   │   └── schema.py
│   └── optimizer
│       ├── agents.py
│       ├── cli.py
│       ├── config
│       │   ├── agents.yaml
│       │   ├── settings.py
│       │   └── tasks.yaml
│       ├── crew.py
│       ├── embedder.py
│       ├── fakers.py
│       ├── logging
│       │   └── console_capture.py
│       ├── models.py
│       ├── tasks.py
│       └── tools
│           ├── chunky_rag_tool.py
│           └── semantic_search_wrapper.py
└── templates
    ├── cover-letter.tex
    └── cv.tex
```

The CV Strategist uses RAG tools to query a ChromaDB vector store of chunked and embedded knowledge base documents. The CV optimization system includes specialized tools for semantic search, LLM synthesis, and knowledge base queries.

Knowledge base is kept in a private repository and symlinked to `knowledge-base/`. The vector database is automatically built from this content using ChromaDB embeddings.

This is what it looks like (more or less)

```
knowledge-base
├── companies
│   └── frobozz-co.md
│   └── acme.md
├── developers
│   └── wesley-hinkle.md
└── projects
|   ├── magic-api-gateway.md
|   ├── zork-legacy-cms.md
|   ├── torch-saas.md
|   ├── grue-detector.md
|   ├── zorkmid-sdk.md
|   ├── anvil.md
└── skills-mapping.md
```

## Setup

Initial setup with virtual environment and dependencies:

```bash
./setup.sh  # Creates .venv, installs deps, sets up Jupyter kernel
# OR manually:
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"  # Installs project with dependencies and dev tools (pytest, jupyter)
```

Build the vector database from knowledge base content:

```bash
make vector_db  # Rebuilds ChromaDB from knowledge-base/ content
```

### Adding New Dependencies

To add a new Python package:

```bash
# 1. Edit pyproject.toml and add the package to dependencies list
# 2. Install the updated dependencies
pip install -e ".[dev]"

# 3. Update the locked requirements file
pip freeze > requirements.txt
```

## Usage

### Basic CV Generation

Generate LaTeX CV from YAML data and convert to PDF:

```bash
make cv                    # Generate CV PDF
make cover-letter          # Generate cover letter PDF
make clean                 # Remove LaTeX build artifacts
```

### CV Optimization with AI

Run the full CrewAI optimization pipeline:

```bash
# Using the optimize-cv CLI command
optimize-cv --config_path config.json

# With inline JSON config
optimize-cv --config '{"inputs": {...}}'
```

### Testing Individual Components

```bash
make job_analysis          # Run job analysis task 
make cv_analysis           # Run CV analysis task
make cv_alignment          # Run CV alignment task
make cv_transformation     # Run CV transformation task
```

### Knowledge Base Tools

```bash
python -m scripts.embed_kb             # Rebuild vector database
python -m scripts.query_kb [query]     # Query knowledge base
python -m scripts.inspect_chroma       # Inspect ChromaDB contents
```

### Development

```bash
jupyter lab                # Start Jupyter for cv-agents.ipynb experimentation
make test                  # Run test suite
pytest tests/unit/         # Run unit tests only
```

Claude's latest [`/init`](/CLAUDE.md) probably explains all this better than I do.
