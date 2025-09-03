#!/usr/bin/env python3
"""Test script for SemanticSearchTool"""

import sys

sys.path.append(".")

from optimizer.tools.semantic_search_tool import SemanticSearchTool
from optimizer.knowledge_embedder import KnowledgeBaseEmbedder
from config import get_config


def test_semantic_search_tool():
    config = get_config()

    embedder = KnowledgeBaseEmbedder(
        knowledge_base_abspath=config.knowledge_base_abspath,
        vector_db_abspath=config.vector_db_abspath,
        force_rebuild=False,
    )

    vectordb = embedder.get_vector_db()

    tool = SemanticSearchTool(retriever=vectordb.as_retriever())
    result = tool._run("data analysis experience")
    print("SEMANTIC SEARCH TOOL:")
    print(result)


if __name__ == "__main__":
    test_semantic_search_tool()
