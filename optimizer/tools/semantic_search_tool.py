from crewai_tools import tool
from langchain_core.retrievers import BaseRetriever


class SemanticSearchTool:
    def __init__(self, retriever: BaseRetriever, top_k: int = 3):
        self.retriever = retriever
        self.top_k = top_k

    @tool("semantic_search_tool")
    def search(self, query: str) -> str:
        """
        Perform semantic search against a vector database.
        Returns relevant content chunks with their source file paths.
        """
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
