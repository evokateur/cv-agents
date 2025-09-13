import os
import glob
from optimizer.utils.vector_utils import is_valid_chroma_vector_db, get_chroma_vector_db
from langchain.vectorstores import Chroma
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings


class KnowledgeBaseEmbedder:
    def __init__(
        self,
        knowledge_base_abspath: str,
        vector_db_abspath: str,
        embedding_model: str = "text-embedding-ada-002",
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        force_rebuild: bool = False,
    ):
        self.knowledge_base_path = knowledge_base_abspath
        self.vector_db_path = vector_db_abspath
        self.embedding_model = embedding_model
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.force_rebuild = force_rebuild

    def build_if_needed(self) -> None:
        if self.force_rebuild or not is_valid_chroma_vector_db(self.vector_db_path):
            if self.force_rebuild and is_valid_chroma_vector_db(self.vector_db_path):
                # Delete existing DB to avoid ChromaDB conflicts
                from optimizer.utils.vector_utils import delete_vector_db
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

        # Load documents using DirectoryLoader approach from example
        def add_metadata(doc, doc_type):
            doc.metadata["doc_type"] = doc_type
            return doc

        # Text loader configuration for encoding
        text_loader_kwargs = {'encoding': 'utf-8'}

        documents = []
        
        # Load documents from subdirectories first
        folders = glob.glob(os.path.join(self.knowledge_base_path, "*"))
        for folder in folders:
            if os.path.isdir(folder):
                doc_type = os.path.basename(folder)
                loader = DirectoryLoader(
                    folder, 
                    glob="**/*.md", 
                    loader_cls=TextLoader, 
                    loader_kwargs=text_loader_kwargs
                )
                folder_docs = loader.load()
                documents.extend([add_metadata(doc, doc_type) for doc in folder_docs])
        
        # Load documents from root knowledge base directory
        root_loader = DirectoryLoader(
            self.knowledge_base_path,
            glob="*.md",  # Only direct children, not recursive
            loader_cls=TextLoader,
            loader_kwargs=text_loader_kwargs
        )
        root_docs = root_loader.load()
        if root_docs:
            # Root docs get no doc_type metadata - they're unspecified/general
            documents.extend(root_docs)

        if not documents:
            raise ValueError(f"No markdown documents found in {self.knowledge_base_path}")

        # Split documents into chunks
        text_splitter = CharacterTextSplitter(
            chunk_size=self.chunk_size, 
            chunk_overlap=self.chunk_overlap
        )
        chunks = text_splitter.split_documents(documents)

        print(f"📝 Total chunks created: {len(chunks)}")
        if documents:
            doc_types = set(doc.metadata.get('doc_type', 'unknown') for doc in documents)
            print(f"📂 Document types found: {doc_types}")

        # Create embeddings and vector store
        embeddings = OpenAIEmbeddings(model=self.embedding_model)
        
        # Delete existing collection if it exists
        if os.path.exists(self.vector_db_path):
            try:
                existing_vectorstore = Chroma(
                    persist_directory=self.vector_db_path,
                    embedding_function=embeddings,
                    collection_name="knowledge_base"
                )
                existing_vectorstore.delete_collection()
            except Exception:
                # If deletion fails, continue - Chroma.from_documents will handle it
                pass

        # Create new vectorstore
        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=self.vector_db_path,
            collection_name="knowledge_base"
        )
        
        print(f"✅ Vector database created with {vectorstore._collection.count()} documents")

    def get_vector_db(self) -> Chroma:
        return get_chroma_vector_db(
            vector_db_abspath=self.vector_db_path,
            collection_name="knowledge_base",
        )

    def get_vector_db_abspath(self) -> str:
        return self.vector_db_path
