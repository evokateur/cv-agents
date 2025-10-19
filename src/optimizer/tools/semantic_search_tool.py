from crewai.tools import BaseTool
from langchain_core.retrievers import BaseRetriever
from pydantic import BaseModel, Field
from typing import Optional, Type


class SemanticSearchInput(BaseModel):
    query: str = Field(..., description="The search query to find relevant documents")
    top_k: Optional[int] = Field(5, description="Number of top results to return")


class SemanticSearchTool(BaseTool):
    name: str = "SemanticSearchTool"
    description: str = (
        "Performs semantic search and returns top-k relevant documents with sources."
    )
    args_schema: Type[BaseModel] = SemanticSearchInput
    retriever: BaseRetriever
    top_k: int = 5

    def __init__(self, retriever: BaseRetriever, top_k: int = 5, **kwargs):
        super().__init__(retriever=retriever, top_k=top_k, **kwargs)

    def _run(self, query: str, top_k: Optional[int] = None, **kwargs) -> str:
        k = top_k if top_k is not None else self.top_k

        try:
            docs = self.retriever.get_relevant_documents(query)
        except AttributeError:
            return "Error: Retriever does not implement `get_relevant_documents()`."

        top_docs = docs[:k]

        if not top_docs:
            return "No relevant documents found."

        results = []
        for i, doc in enumerate(top_docs, 1):
            source = doc.metadata.get("url", doc.metadata.get("source", "Unknown"))
            content = doc.page_content.strip()
            results.append(f"[{i}] Source: {source}\n{content}")

        return "\n\n".join(results)
