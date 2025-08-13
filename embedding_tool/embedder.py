"""
Main embedding logic for processing knowledge base documents into vector embeddings.
"""

import os
from typing import List, Optional
from dotenv import load_dotenv
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema import Document
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

from .loaders import DocumentLoader


class KnowledgeBaseEmbedder:
    """Handles embedding of knowledge base documents into ChromaDB vector store."""

    def __init__(
        self,
        knowledge_base_path: str = "knowledge-base",
        vector_db_path: str = "vector_db",
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ):
        load_dotenv(override=True)
        os.environ["OPENAI_API_KEY"] = os.getenv(
            "OPENAI_API_KEY", "your-key-if-not-using-env"
        )

        self.knowledge_base_path = knowledge_base_path
        self.vector_db_path = vector_db_path
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        self.document_loader = DocumentLoader(knowledge_base_path)
        self.text_splitter = CharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )
        self.embeddings = OpenAIEmbeddings()

    def create_embeddings(self) -> dict:
        """
        Create vector embeddings from knowledge base documents.

        Returns:
            Dictionary with processing statistics and results.
        """
        # Load documents
        documents = self.document_loader.load_documents()

        if not documents:
            return {
                "status": "error",
                "message": f"No documents found in {self.knowledge_base_path}",
                "documents_loaded": 0,
                "chunks_created": 0,
                "vectors_stored": 0,
                "doc_types": [],
            }

        # Split documents into chunks
        chunks = self.text_splitter.split_documents(documents)

        # Get document types for reporting
        doc_types = self.document_loader.get_document_types(documents)

        # Delete existing vector store if it exists
        if os.path.exists(self.vector_db_path):
            existing_store = Chroma(
                persist_directory=self.vector_db_path,
                embedding_function=self.embeddings,
            )
            existing_store.delete_collection()

        # Create new vector store
        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            persist_directory=self.vector_db_path,
        )

        # Get vector count and dimensions for reporting
        vector_count = vectorstore._collection.count()

        # Get sample embedding for dimension info
        sample_embedding = vectorstore._collection.get(limit=1, include=["embeddings"])[
            "embeddings"
        ][0]
        dimensions = len(sample_embedding)

        return {
            "status": "success",
            "message": f"Successfully created embeddings for {len(documents)} documents",
            "documents_loaded": len(documents),
            "chunks_created": len(chunks),
            "vectors_stored": vector_count,
            "vector_dimensions": dimensions,
            "doc_types": doc_types,
            "knowledge_base_path": self.knowledge_base_path,
            "vector_db_path": self.vector_db_path,
        }

    def get_vectorstore(self) -> Optional[Chroma]:
        """
        Get existing vectorstore if it exists.

        Returns:
            Chroma vectorstore instance or None if doesn't exist.
        """
        if not os.path.exists(self.vector_db_path):
            return None

        return Chroma(
            persist_directory=self.vector_db_path, embedding_function=self.embeddings
        )

