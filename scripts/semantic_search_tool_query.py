#!/usr/bin/env python3
"""
Command-line script to query the vector database using the same semantic search tool as the CrewAI agents.
Usage: python -m scripts.semantic_search_tool_query 'query string'
"""

import argparse
import sys
from optimizer.agents import CustomAgents


def main():
    parser = argparse.ArgumentParser(
        description="Query the vector database using the SemanticSearchTool"
    )
    parser.add_argument("query", help="The query string to search for")

    args = parser.parse_args()

    try:
        agents = CustomAgents()
        tool = agents.get_semantic_search_tool()

        print(f"Query: {args.query}")
        print("=" * 60)

        # Run the query
        result = tool._run(args.query)

        print("Result:")
        print(result)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
