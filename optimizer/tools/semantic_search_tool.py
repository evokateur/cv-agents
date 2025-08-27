from langchain_core.tools import BaseTool
from langchain_core.retrievers import BaseRetriever
from typing import Optional, List, Any


class SemanticSearchTool(BaseTool):
    name = "semantic_search_tool"
    description = (
        "Performs semantic search and returns top-k relevant documents with sources."
    )

    def __init__(self, retriever: BaseRetriever, top_k: int = 3):
        super().__init__()
        self.retriever = retriever
        self.top_k = top_k

    def _run(self, query: str, run_manager: Optional[Any] = None) -> str:
        try:
            docs = self.retriever.get_relevant_documents(query)
        except AttributeError:
            return "Error: Retriever does not implement `get_relevant_documents()`."

        top_docs = docs[: self.top_k]

        if not top_docs:
            return "No relevant documents found."

        results = []
        for i, doc in enumerate(top_docs, 1):
            source = doc.metadata.get("source", "Unknown")
            content = doc.page_content.strip()
            results.append(f"[{i}] Source: {source}\n{content}")

        return "\n\n".join(results)

    async def _arun(self, query: str, run_manager: Optional[Any] = None) -> str:
        raise NotImplementedError("Async not supported for this tool.")
