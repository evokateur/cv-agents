#!/usr/bin/env python3
"""Query KB using SemanticSearchWrapper"""

import sys
import warnings

sys.path.append(".")

from optimizer.tools.semantic_search_wrapper import SemanticSearchWrapper
from config import get_embedchain_config


def run_query(query=None):
    if query is None:
        query = "data analysis experience"
    tool = SemanticSearchWrapper(config=get_embedchain_config())
    result = tool._run(query)
    print("QUERY RESULT:")
    print(result)


if __name__ == "__main__":
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    query = sys.argv[1] if len(sys.argv) > 1 else None
    run_query(query)
