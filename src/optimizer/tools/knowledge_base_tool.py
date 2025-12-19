"""Knowledge base query tool using langchain for RAG"""

from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from config.settings import get_rag_config


class KnowledgeBaseInput(BaseModel):
    query: str = Field(
        ...,
        description="The search query or question to ask the knowledge base"
    )


class KnowledgeBaseTool(BaseTool):
    name: str = "Knowledge base"
    description: str = "A knowledge base that can be used to answer questions about the candidate's skills, projects, and experience."
    args_schema: Type[BaseModel] = KnowledgeBaseInput

    vector_db_path: str = None
    collection_name: str = None
    embedding_model: str = None
    num_results: int = None

    def __init__(self, vector_db_path: str, **kwargs):
        super().__init__(**kwargs)
        self.vector_db_path = vector_db_path

        rag_config = get_rag_config()
        self.collection_name = rag_config["collection_name"]
        self.embedding_model = rag_config["embedding_model"]
        self.num_results = rag_config["num_results"]

    def _run(self, query: str) -> str:
        embedding_function = OpenAIEmbeddings(model=self.embedding_model)
        vectorstore = Chroma(
            persist_directory=self.vector_db_path,
            embedding_function=embedding_function,
            collection_name=self.collection_name
        )

        docs = vectorstore.similarity_search_with_score(query, k=self.num_results)

        if not docs:
            return "No relevant content found.\n\nSources:"

        contents = []
        sources = []
        for doc, score in docs:
            contents.append(doc.page_content)
            source = doc.metadata.get('source', 'Unknown')
            if source not in sources:
                sources.append(source)

        answer = "\n\n".join(contents)
        result = f"{answer}\n\nSources:\n"
        for source in sources:
            result += f"- {source}\n"

        return result.strip()

    async def _arun(self, query: str) -> str:
        return self._run(query)
