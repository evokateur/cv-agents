#!/usr/bin/env python3
"""Test script for ChunkyKnowledgeBaseTool"""

import sys
sys.path.append(".")

from optimizer.tools.chunky_kb_tool import ChunkyKnowledgeBaseTool
from config import get_embedchain_config


def test_chunky_kb_tool():
    tool = ChunkyKnowledgeBaseTool(config=get_embedchain_config())
    result = tool._run("data analysis experience")
    print("CHUNKY KB TOOL:")
    print(result)


if __name__ == "__main__":
    test_chunky_kb_tool()