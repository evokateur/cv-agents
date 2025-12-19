import os
from pathlib import Path
from shared.vector_utils import is_valid_chroma_vector_db, get_chroma_vector_db
from config.settings import get_rag_config
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


class KnowledgeBaseEmbedder:
    def __init__(
        self,
        knowledge_base_abspath: str,
        vector_db_abspath: str,
        force_rebuild: bool = False,
    ):
        self.knowledge_base_path = knowledge_base_abspath
        self.vector_db_path = vector_db_abspath
        self.force_rebuild = force_rebuild

        rag_config = get_rag_config()
        self.embedding_model = rag_config["embedding_model"]
        self.chunk_size = rag_config["chunk_size"]
        self.chunk_overlap = rag_config["chunk_overlap"]
        self.collection_name = rag_config["collection_name"]

    def build_if_needed(self) -> None:
        if self.force_rebuild or not is_valid_chroma_vector_db(self.vector_db_path):
            if self.force_rebuild and is_valid_chroma_vector_db(self.vector_db_path):
                # Delete existing DB to avoid ChromaDB conflicts
                from shared.vector_utils import delete_vector_db

                delete_vector_db(self.vector_db_path)
            print("🛠️ Building or rebuilding vector DB from knowledge base...")
            self._build_vector_db()
        else:
            print("📦 Using existing vector DB at:", self.vector_db_path)

    def _build_vector_db(self) -> None:
        if not os.path.exists(self.knowledge_base_path):
            raise FileNotFoundError(
                f"Knowledge base not found at: {self.knowledge_base_path}"
            )

        print(f"📂 Loading documents from {self.knowledge_base_path}")

        # Load all markdown and text files from the knowledge base
        loader = DirectoryLoader(
            self.knowledge_base_path,
            glob="**/*.md",
            loader_cls=TextLoader,
            show_progress=True,
            use_multithreading=True
        )
        documents = loader.load()

        print(f"📄 Loaded {len(documents)} documents")

        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
        )
        chunks = text_splitter.split_documents(documents)

        print(f"✂️  Split into {len(chunks)} chunks")

        # Create embeddings and vector store
        embedding_function = OpenAIEmbeddings(model=self.embedding_model)

        print(f"💾 Creating vector database at {self.vector_db_path}")
        Chroma.from_documents(
            documents=chunks,
            embedding=embedding_function,
            persist_directory=self.vector_db_path,
            collection_name=self.collection_name
        )

        print("✅ Vector database created successfully")

    def get_vector_db(self) -> Chroma:
        return get_chroma_vector_db(
            vector_db_abspath=self.vector_db_path,
            collection_name=self.collection_name,
        )

    def get_vector_db_abspath(self) -> str:
        return self.vector_db_path
