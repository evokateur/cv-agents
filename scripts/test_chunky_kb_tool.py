#!/usr/bin/env python3
"""Test script for ChunkyKnowledgeBaseTool"""

import sys

sys.path.append(".")

from optimizer.tools.chunky_kb_tool import ChunkyKnowledgeBaseTool


def test_chunky_kb_tool():
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
                "dir": "vector_db",
                "collection_name": "knowledge_base",
            },
        },
    }

    tool = ChunkyKnowledgeBaseTool(config=embedchain_config)
    result = tool._run("data analysis experience")
    print("CHUNKY KB TOOL:")
    print(result)


if __name__ == "__main__":
    test_chunky_kb_tool()

