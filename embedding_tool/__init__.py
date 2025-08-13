"""
Knowledge Base Embedding Tool

Standalone tool to process knowledge base documents and create vector embeddings
for the CV optimization system.
"""

from .embedder import KnowledgeBaseEmbedder
from .loaders import DocumentLoader

__all__ = ["KnowledgeBaseEmbedder", "DocumentLoader"]