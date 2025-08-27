#!/usr/bin/env python3
"""
Inspects the raw chunks retrieved from the vector database via the agent's RAG tool.
Usage: python -m scripts.inspect_rag_chunks 'your query' [-v]
"""

import argparse
import sys
from optimizer.agents import CustomAgents


def main():
    parser = argparse.ArgumentParser(
        description="Inspect chunks retrieved by the CrewAI RAG tool (pre-LLM)"
    )
    parser.add_argument("query", help="Query string to search for")
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Print full chunk content and metadata",
    )

    args = parser.parse_args()

    try:
        agents = CustomAgents()
        rag_tool = agents.get_rag_tool()

        # Try accessing the underlying retriever to bypass LLM output
        retriever = getattr(rag_tool, "retriever", None)
        if retriever is None:
            print("❌ Could not access 'retriever' on the RAG tool.")
            print("🔍 Dumping available attributes on rag_tool:")
            print("=" * 60)
            for attr in dir(rag_tool):
                if not attr.startswith("__"):
                    print(attr)
            print("=" * 60)
            print(
                "💡 Tip: Look for attributes like `_tool`, `_retriever`, or `vectorstore`."
            )
            sys.exit(1)

        docs = retriever.get_relevant_documents(args.query)

        print(f"\n🔍 Retrieved {len(docs)} chunks for query: '{args.query}'\n")
        print("=" * 80)

        for i, doc in enumerate(docs, start=1):
            source = doc.metadata.get("source", "UNKNOWN SOURCE")
            print(f"[{i}] Source: {source}")
            if args.verbose:
                print(f"     Metadata: {doc.metadata}")
                print(
                    f"     Content: {doc.page_content.strip()[:500]}"
                )  # Truncated for display
            else:
                print(
                    f"     Preview: {doc.page_content.strip()[:120].replace('\n', ' ')}"
                )
            print("-" * 80)

    except Exception as e:
        print(f"❌ Error during inspection: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
