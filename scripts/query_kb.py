#!/usr/bin/env python3
"""Query KB using KnowledgeBaseTool"""

import sys
import warnings

from optimizer.tools.knowledge_base_tool import KnowledgeBaseTool
from optimizer.config.settings import get_config


def run_query(query=None):
    if query is None:
        query = "data analysis experience"
    config = get_config()
    tool = KnowledgeBaseTool(vector_db_path=config.vector_db_abspath)
    result = tool._run(query)
    print("QUERY RESULT:")
    print(result)


if __name__ == "__main__":
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    query = sys.argv[1] if len(sys.argv) > 1 else None
    run_query(query)
