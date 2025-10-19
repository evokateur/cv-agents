# Migration Plan: Module Reorganization

## Overview

Reorganize the codebase into two independent modules (`builder` and `optimizer`) with shared models (`models`), following standard Python packaging conventions.

## Target Structure

```
cv-agents/
├── pyproject.toml                    # Modern Python packaging configuration
├── README.md
├── Makefile                          # Updated with new paths
├── pytest.ini
├── requirements.txt                  # Or move to pyproject.toml dependencies
├── sample.env
├── setup.sh
│
├── src/
│   ├── models/                       # Shared Pydantic models
│   │   ├── __init__.py              # Export all models
│   │   └── schema.py                # CurriculumVitae, Contact, Education, etc.
│   │
│   ├── builder/                      # LaTeX CV generation module
│   │   ├── __init__.py              # Export public API
│   │   ├── generator.py             # Core generation logic (from make-cv.py)
│   │   ├── cover_letter.py          # Cover letter generation (from make-cover-letter.py)
│   │   ├── template_env.py          # Custom Jinja2 environment (from texenv/jinja.py)
│   │   └── cli.py                   # CLI entry points
│   │
│   └── optimizer/                    # AI-powered CV optimization module
│       ├── __init__.py              # Export public API
│       ├── crew.py                  # CrewAI crew implementation
│       ├── agents.py                # Agent definitions
│       ├── tasks.py                 # Task definitions
│       ├── models.py                # JobPosting, CvTransformationPlan
│       ├── embedder.py              # Knowledge base embedder
│       ├── fakers.py                # Test data generators
│       │
│       ├── config/
│       │   ├── __init__.py
│       │   ├── agents.yaml
│       │   ├── tasks.yaml
│       │   └── settings.py          # Environment config (from config.py)
│       │
│       ├── tools/
│       │   ├── __init__.py
│       │   ├── chunky_rag_tool.py
│       │   ├── chunky_kb_tool.py
│       │   ├── semantic_search_tool.py
│       │   └── semantic_search_wrapper.py
│       │
│       ├── utils/
│       │   ├── __init__.py
│       │   ├── vector_utils.py
│       │   └── prompt_utils.py
│       │
│       ├── logging/
│       │   ├── __init__.py
│       │   └── console_capture.py
│       │
│       └── cli.py                   # CLI entry point (from optimizer/kickoff.py)
│
├── scripts/                          # Development and testing scripts
│   ├── alignment.py                 # Keep as-is, update imports
│   ├── transformation.py            # Keep as-is, update imports
│   ├── analysis.py                  # Keep as-is, update imports
│   ├── job_analysis.py              # Keep as-is, update imports
│   ├── embed_kb.py                  # Keep as-is, update imports
│   ├── query_kb.py                  # Keep as-is, update imports
│   ├── inspect_chroma.py            # Keep as-is, update imports
│   └── chroma_test.py               # Keep as-is, update imports
│
├── tests/
│   ├── __init__.py
│   ├── unit/
│   │   ├── models/                  # New: tests for shared models
│   │   │   ├── __init__.py
│   │   │   └── test_schema.py
│   │   │
│   │   ├── builder/                 # New: tests for builder module
│   │   │   ├── __init__.py
│   │   │   ├── test_generator.py
│   │   │   └── test_template_env.py
│   │   │
│   │   └── optimizer/               # Reorganized optimizer tests
│   │       ├── __init__.py
│   │       ├── test_crew.py
│   │       ├── test_agents.py
│   │       ├── test_tasks.py
│   │       ├── tools/
│   │       │   └── test_semantic_search_wrapper.py
│   │       └── utils/
│   │           └── test_vector_utils.py
│   │
│   └── integration/                 # New: integration tests
│       ├── __init__.py
│       └── test_end_to_end.py
│
├── data/                            # CV data files (unchanged)
│   ├── cv.json
│   ├── cv.yaml
│   ├── cv-schema.json
│   └── ...
│
├── templates/                       # LaTeX templates (unchanged)
│   ├── cv.tex
│   └── cover-letter.tex
│
├── knowledge-base/                  # Symlink to RAG knowledge base (unchanged)
├── db/                              # ChromaDB database (unchanged)
│   └── chroma.sqlite3
│
├── job_postings/                    # Test job postings (unchanged)
│   ├── automattic/
│   └── tests/
│
├── docs/                            # Documentation
│   ├── architecture-notes.md
│   ├── progress.md
│   └── migration-plan.md           # This file
│
├── examples/                        # LaTeX examples (unchanged)
├── llm-context/                     # Planning docs (unchanged)
└── CLAUDE.md                        # Updated with new structure
```

## Migration Steps

### Phase 1: Setup New Structure

1. **Create `src/` directory structure**
   ```bash
   mkdir -p src/models
   mkdir -p src/builder
   mkdir -p src/optimizer/{config,tools,utils,logging}
   ```

2. **Create `pyproject.toml`**
   - Define package metadata
   - Specify dependencies (from requirements.txt)
   - Configure entry points for CLI commands
   - Set up editable install with `pip install -e .`

3. **Create all `__init__.py` files**
   - Export public APIs from each module
   - Enable clean imports

### Phase 2: Extract Shared Models

1. **Create `src/models/schema.py`**
   - Move from `optimizer/models.py`: `CurriculumVitae`, `Contact`, `Education`, `Experience`, `AdditionalExperience`, `AreaOfExpertise`, `Language`
   - These are the CV structure models used by both builder and optimizer

2. **Create `src/models/__init__.py`**
   ```python
   from .schema import (
       CurriculumVitae,
       Contact,
       Education,
       Experience,
       AdditionalExperience,
       AreaOfExpertise,
       Language,
   )

   __all__ = [
       "CurriculumVitae",
       "Contact",
       "Education",
       "Experience",
       "AdditionalExperience",
       "AreaOfExpertise",
       "Language",
   ]
   ```

### Phase 3: Migrate builder Module

1. **Create `src/builder/template_env.py`**
   - Move from `texenv/jinja.py`
   - Keep custom Jinja2 environment and LaTeX escaping functions

2. **Create `src/builder/generator.py`**
   - Extract core logic from `make-cv.py`
   - Update imports: `from models import CurriculumVitae`
   - Create reusable functions for CV generation

3. **Create `src/builder/cover_letter.py`**
   - Extract core logic from `make-cover-letter.py`
   - Update imports as needed

4. **Create `src/builder/cli.py`**
   - CLI entry points for `make-cv` and `make-cover-letter` commands
   - Use Click or argparse for argument parsing

5. **Create `src/builder/__init__.py`**
   ```python
   from .generator import generate_cv
   from .cover_letter import generate_cover_letter
   from .template_env import get_latex_env

   __all__ = ["generate_cv", "generate_cover_letter", "get_latex_env"]
   ```

### Phase 4: Migrate optimizer Module

1. **Move optimizer files to `src/optimizer/`**
   ```bash
   # Core files
   mv optimizer/crew.py src/optimizer/
   mv optimizer/agents.py src/optimizer/
   mv optimizer/tasks.py src/optimizer/
   mv optimizer/embedder.py src/optimizer/
   mv optimizer/fakers.py src/optimizer/

   # Config
   mv optimizer/config/ src/optimizer/

   # Tools
   mv optimizer/tools/ src/optimizer/

   # Utils
   mv optimizer/utils/ src/optimizer/

   # Logging
   mv optimizer/logging/ src/optimizer/

   # CLI
   mv optimizer/kickoff.py src/optimizer/cli.py
   ```

2. **Update `src/optimizer/models.py`**
   - Keep `JobPosting` and `CvTransformationPlan` (optimizer-specific)
   - Remove CV structure models (now in models package)
   - Add import: `from models import CurriculumVitae`

3. **Move `config.py` to `src/optimizer/config/settings.py`**
   - Environment configuration belongs with optimizer module
   - Update all imports throughout optimizer code

4. **Update all imports in optimizer files**
   - Change `from optimizer.X import Y` to remain `from optimizer.X import Y`
   - Change CV model imports to `from models import CurriculumVitae`
   - Update config imports to `from optimizer.config.settings import ...`

5. **Create `src/optimizer/__init__.py`**
   ```python
   from .crew import CvOptimizationCrew
   from .models import JobPosting, CvTransformationPlan

   __all__ = ["CvOptimizationCrew", "JobPosting", "CvTransformationPlan"]
   ```

### Phase 5: Update Scripts

1. **Update all files in `scripts/`**
   - Imports from `optimizer.*` remain the same (just different location)
   - Change imports from `texenv.*` to `builder.template_env`
   - Update config imports to `from optimizer.config.settings import ...`

2. **Rename script files (remove cv_ prefix):**
   ```bash
   mv scripts/cv_alignment.py scripts/alignment.py
   mv scripts/cv_transformation.py scripts/transformation.py
   mv scripts/cv_analysis.py scripts/analysis.py
   ```

3. **Files to update:**
   - `scripts/alignment.py`
   - `scripts/transformation.py`
   - `scripts/analysis.py`
   - `scripts/job_analysis.py`
   - `scripts/embed_kb.py`
   - `scripts/query_kb.py`
   - `scripts/inspect_chroma.py`
   - `scripts/chroma_test.py`

### Phase 6: Update Tests

1. **Reorganize `tests/unit/` by module**
   ```bash
   mkdir -p tests/unit/models
   mkdir -p tests/unit/builder
   mkdir -p tests/unit/optimizer/{tools,utils}
   ```

2. **Move existing optimizer tests**
   ```bash
   mv tests/unit/optimizer/* tests/unit/optimizer/
   ```

3. **Update test imports**
   - Imports from `optimizer.*` remain the same
   - Change `from texenv.*` to `from builder.template_env`

4. **Create new test files**
   - `tests/unit/models/test_schema.py` - Test shared models
   - `tests/unit/builder/test_generator.py` - Test CV generation
   - `tests/unit/builder/test_template_env.py` - Test Jinja2 environment

### Phase 7: Update Configuration Files

1. **Update `Makefile`**
   - Change `python make-cv.py` to `python -m builder.cli` (or use entry point)
   - Update script references: `cv_alignment` → `alignment`, etc.
   - Keep targets but update underlying commands

2. **Update `CLAUDE.md`**
   - Document new structure in Architecture section
   - Update all file paths and module references
   - Update Commands section with new import paths

3. **Update `pytest.ini`**
   - Update testpaths if needed
   - Ensure pythonpath includes `src/`

4. **Update `.gitignore`**
   - Add `src/**/__pycache__/`
   - Add `*.egg-info/`
   - Add `dist/`, `build/` for packaging

### Phase 8: Create pyproject.toml

```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "cv-agents"
version = "0.1.0"
description = "CV generation and AI-powered optimization system"
requires-python = ">=3.10"
dependencies = [
    # Add dependencies from requirements.txt
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-mock",
]

[project.scripts]
make-cv = "builder.cli:main_cv"
make-cover-letter = "builder.cli:main_cover_letter"
optimize-cv = "optimizer.cli:main"

[tool.setuptools.packages.find]
where = ["src"]

[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]
```

### Phase 9: Clean Up

1. **Remove old directories**
   ```bash
   rm -rf optimizer/
   rm -rf texenv/
   rm make-cv.py
   rm make-cover-letter.py
   rm config.py
   ```

2. **Remove old test structure**
   ```bash
   rm -rf tests/unit/optimizer/
   ```

3. **Verify import cleanup**
   - Search for any remaining `from texenv.` imports
   - Search for any remaining `import config` (should be `optimizer.config.settings`)

### Phase 10: Testing and Validation

1. **Install package in editable mode**
   ```bash
   pip install -e .
   ```

2. **Run test suite**
   ```bash
   pytest
   ```

3. **Test CLI commands**
   ```bash
   make-cv
   make-cover-letter
   optimize-cv --help
   ```

4. **Test imports in Python REPL**
   ```python
   from models import CurriculumVitae
   from builder import generate_cv
   from optimizer import CvOptimizationCrew
   ```

5. **Run all Makefile targets**
   ```bash
   make cv
   make cover-letter
   make test
   make alignment
   make transformation
   ```

## Import Changes Summary

### Before
```python
from optimizer.models import CurriculumVitae, JobPosting
from optimizer.crew import CvOptimizationCrew
from texenv.jinja import get_latex_env
import config
```

### After
```python
from models import CurriculumVitae
from optimizer.models import JobPosting
from optimizer import CvOptimizationCrew
from builder.template_env import get_latex_env
from optimizer.config.settings import get_embedchain_config
```

## Benefits of New Structure

1. **Clear separation of concerns**: Builder and optimizer are independent modules
2. **Shared models**: Single source of truth for CV schema
3. **Standard Python packaging**: Enables `pip install`, proper imports, entry points
4. **Better testability**: Organized test structure mirrors source code
5. **Reusability**: `builder` can be used without AI dependencies
6. **Professional structure**: Follows Python packaging best practices
7. **Easier maintenance**: Clear module boundaries and responsibilities

## Rollback Plan

If migration encounters issues:

1. Git commit before starting migration
2. Keep old files until new structure is validated
3. Use git branches for migration work
4. Test incrementally after each phase
5. Can revert individual phases if needed

## Timeline Estimate

- Phase 1-2 (Setup + Models): 30 minutes
- Phase 3 (builder): 1 hour
- Phase 4 (optimizer): 1.5 hours
- Phase 5-6 (Scripts + Tests): 1 hour
- Phase 7-8 (Config + pyproject.toml): 45 minutes
- Phase 9-10 (Cleanup + Testing): 1 hour

**Total: ~6 hours**
