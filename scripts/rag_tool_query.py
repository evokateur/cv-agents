#!/usr/bin/env python3
"""
Command-line script to query the vector database using the same RAG tool as the CrewAI agents.
Usage: python -m scripts.rag_tool_query 'query string'
"""

import argparse
import sys
from optimizer.agents import CustomAgents


def main():
    parser = argparse.ArgumentParser(
        description="Query the vector database using the CrewAI RAG tool"
    )
    parser.add_argument("query", help="The query string to search for")

    args = parser.parse_args()

    try:
        agents = CustomAgents()
        rag_tool = agents.get_rag_tool()

        print(f"Query: {args.query}")
        print("=" * 60)

        # Run the query
        result = rag_tool._run(args.query)

        print("Result:")
        print(result)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
