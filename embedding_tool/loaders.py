"""
Document loading utilities for the knowledge base embedding tool.
"""

import os
import glob
from typing import List
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.schema import Document


class DocumentLoader:
    """Handles loading markdown documents from the knowledge base directory."""
    
    def __init__(self, knowledge_base_path: str = "knowledge-base"):
        self.knowledge_base_path = knowledge_base_path
        self.text_loader_kwargs = {'encoding': 'utf-8'}
    
    def load_documents(self) -> List[Document]:
        """
        Load all markdown documents from knowledge base subdirectories.
        
        Returns:
            List of Document objects with doc_type metadata added.
        """
        folders = glob.glob(f"{self.knowledge_base_path}/*")
        documents = []
        
        for folder in folders:
            if not os.path.isdir(folder):
                continue
                
            doc_type = os.path.basename(folder)
            loader = DirectoryLoader(
                folder, 
                glob="**/*.md", 
                loader_cls=TextLoader, 
                loader_kwargs=self.text_loader_kwargs
            )
            
            folder_docs = loader.load()
            for doc in folder_docs:
                doc.metadata["doc_type"] = doc_type
                documents.append(doc)
        
        return documents
    
    def get_document_types(self, documents: List[Document]) -> List[str]:
        """Extract unique document types from loaded documents."""
        return list(set(doc.metadata.get('doc_type', 'unknown') for doc in documents))