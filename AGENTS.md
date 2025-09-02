# Repository Guidelines

## Project Structure & Module Organization
- `optimizer/`: core agents, tasks, tools, and models (see `agents.py`, `tasks.py`, `tools/semantic_search_tool.py`, `knowledge_embedder.py`).
- `optimizer/config/`: YAML for agents and tasks.
- `scripts/`: runnable utilities and demos (e.g., `cv_agents.py`).
- `templates/`: LaTeX templates; `data/`: CV/cover letter sources; `output/`: generated artifacts.
- `docs/`: architecture notes and direction (start with `architecture-notes.md`, `progress.md`).
- `tests/`: pytest suites (unit and integration); config in `pytest.ini`.

## Build, Test, and Development Commands
- `./setup.sh`: create `.venv` and install deps.
- `make agents`: run the multi-agent demo (`python -m scripts.cv_agents`).
- `make cv` / `make cover-letter`: render LaTeX from `data/*` into `output/*.pdf`.
- `make test`: run all tests with pytest (`-v`, strict markers).
- Examples: `pytest -m unit`, `pytest -k semantic_search`.

## Coding Style & Naming Conventions
- Python, PEP 8, 4-space indent; prefer type hints and module-level docstrings.
- Filenames: `snake_case.py`; classes: `PascalCase`; functions/vars: `snake_case`.
- Keep tools small and composable (see `semantic_search_tool.py`); place shared helpers in `optimizer/utils/`.

## Testing Guidelines
- Framework: `pytest` (+ `pytest-asyncio` if needed).
- Naming: `tests/test_*.py`, functions `test_*`. Use markers: `unit`, `integration`, `slow`.
- Add focused tests for new tool behavior and vector DB interactions; avoid brittle construction tests.

## Commit & Pull Request Guidelines
- Commits: short, present-tense summaries (e.g., "add architecture note", "fix source path extraction").
- PRs: clear description, link issues, note architecture impacts; include before/after outputs when touching CV/CL rendering; update docs in `docs/` if behavior or architecture changes.

## Security & Configuration Tips
- Copy `sample.env` → `.env`; set API keys and model names (e.g., `OPENAI_API_KEY`, `CV_ADVISOR_MODEL`).
- Paths: `KNOWLEDGE_BASE_PATH` (default `knowledge-base`), `VECTOR_DB_PATH` (default `vector_db`) managed via `config.py`.
- Don’t commit secrets or generated PDFs (`output/`).

## Architecture Overview (Essentials)
- Agents consult a knowledge base via `SemanticSearchTool` (returns chunks + source paths). Use FileReadTool on returned sources when deeper context is needed.
- Embeddings/DB built by `KnowledgeBaseEmbedder`; prompts inject Pydantic schemas where tasks pass structured outputs.
- For direction and rationale, read `docs/architecture-notes.md` and `docs/progress.md`.

