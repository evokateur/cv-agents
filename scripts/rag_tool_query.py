#!/usr/bin/env python3
"""
Command-line script to query the vector database using the same RAG tool as the CrewAI agents.
Usage: python -m scripts.rag_tool_query 'query string'
"""

import argparse
import sys
import json
from optimizer.agents import CustomAgents


def main():
    parser = argparse.ArgumentParser(
        description="Query the vector database using the CrewAI RAG tool"
    )
    parser.add_argument("query", help="The query string to search for")
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Show verbose output including metadata",
    )

    args = parser.parse_args()

    try:
        # Initialize the agents to get the RAG tool
        agents = CustomAgents()
        rag_tool = agents.get_rag_tool()

        print(f"Query: {args.query}")
        print("=" * 60)

        # Run the query
        result = rag_tool._run(args.query)

        if args.verbose:
            print("\n--- Retrieved Chunks and Metadata ---\n")
            for i, doc in enumerate(result):
                source = doc.metadata.get("source", "UNKNOWN SOURCE")
                preview = doc.page_content[:120].replace("\n", " ")
                print(f"[{i + 1}] Source: {source}")
                print(f"     Preview: {preview}")
                print()
            print("Result:")
            print(result)
        else:
            print("Result:")
            print(result)

        # Try to access any metadata if available
        if hasattr(rag_tool, "metadata") or hasattr(result, "metadata"):
            print("\n" + "=" * 60)
            print("METADATA:")
            if hasattr(rag_tool, "metadata"):
                print("Tool metadata:", rag_tool.metadata)
            if hasattr(result, "metadata"):
                print("Result metadata:", result.metadata)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

