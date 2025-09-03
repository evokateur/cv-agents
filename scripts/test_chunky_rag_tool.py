#!/usr/bin/env python3
"""Test script for ChunkyRagTool"""

import sys

sys.path.append(".")

from optimizer.tools.chunky_rag_tool import ChunkyRagTool


def test_chunky_rag_tool():
    embedchain_config = {
        "llm": {
            "provider": "openai",
            "config": {"model": "gpt-4o-mini"},
        },
        "embedder": {
            "provider": "openai",
            "config": {"model": "text-embedding-ada-002"},
        },
        "vectordb": {
            "provider": "chroma",
            "config": {
                "dir": "vector_db",  # your persistent directory
                "collection_name": "knowledge_base",  # must match ingestion
            },
        },
    }

    tool = ChunkyRagTool(config=embedchain_config)
    result = tool._run("data analysis experience")
    print("CHUNKY RAG TOOL:")
    print(result)


if __name__ == "__main__":
    test_chunky_rag_tool()
