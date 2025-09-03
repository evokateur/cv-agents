# tools/chunky_rag_tool.py
import json
from crewai_tools.tools.rag.rag_tool import RagTool
from crewai_tools.adapters.embedchain_adapter import EmbedchainAdapter


class ChunkyRagTool(RagTool):
    name: str = "Knowledge base with sources"
    description: str = (
        "Like the default Knowledge base tool, but returns both the synthesized "
        "answer and the retrieved chunks with metadata in JSON format."
    )

    def _run(self, query: str) -> str:
        # Cast adapter to EmbedchainAdapter (hacky, but works)
        adapter: EmbedchainAdapter = self.adapter  # type: ignore

        # Get both the LLM result and sources
        result, sources = adapter.embedchain_app.query(
            query, citations=True, dry_run=False
        )

        structured_sources = [{"text": src[0], "metadata": src[1]} for src in sources]
        return json.dumps({"answer": result, "sources": structured_sources}, indent=2)

    async def _arun(self, query: str) -> str:
        return self._run(query)
