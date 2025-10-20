# tools/chunky_kb_tool.py
import json
import portalocker
from crewai.tools import BaseTool
from embedchain import App
from typing import Any


class ChunkyKnowledgeBaseTool(BaseTool):
    name: str = "Knowledge base with sources"
    description: str = (
        "Retrieves from the knowledge base using embedchain.App, returning both "
        "the synthesized answer and the retrieved chunks with metadata in JSON format."
    )
    app: Any = None  # Declare the field for Pydantic

    def __init__(self, config: dict[str, Any] | None = None, **kwargs):
        super().__init__(**kwargs)
        # Lock around App creation, same as RagTool does
        lock_path = "crewai-rag-tool.lock"
        with portalocker.Lock(lock_path, timeout=10):
            self.app = App.from_config(config=config) if config else App()

    def _run(self, query: str) -> str:
        result, sources = self.app.query(query, citations=True, dry_run=False)

        structured_sources = [{"text": src[0], "metadata": src[1]} for src in sources]
        payload = {
            "answer": result,
            "sources": structured_sources,
        }
        return json.dumps(payload, indent=2)

    async def _arun(self, query: str) -> str:
        return self._run(query)
