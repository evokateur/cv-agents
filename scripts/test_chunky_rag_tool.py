#!/usr/bin/env python3
"""Test script for ChunkyRagTool"""

import sys
sys.path.append(".")

from optimizer.tools.chunky_rag_tool import ChunkyRagTool
from config import get_embedchain_config


def test_chunky_rag_tool():
    tool = ChunkyRagTool(config=get_embedchain_config())
    result = tool._run("data analysis experience")
    print("CHUNKY RAG TOOL:")
    print(result)


if __name__ == "__main__":
    test_chunky_rag_tool()