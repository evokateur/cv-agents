#!/usr/bin/env python3
"""Test script for SemanticSearchWrapper"""

import sys
sys.path.append(".")

from optimizer.tools.semantic_search_wrapper import SemanticSearchWrapper
from config import get_embedchain_config


def test_semantic_search_wrapper():
    tool = SemanticSearchWrapper(config=get_embedchain_config())
    result = tool._run("data analysis experience")
    print("SEMANTIC SEARCH WRAPPER:")
    print(result)


if __name__ == "__main__":
    test_semantic_search_wrapper()