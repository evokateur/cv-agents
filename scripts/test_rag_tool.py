#!/usr/bin/env python3
"""
Test script for CrewAI RagTool using approach #2 with knowledge-base directory
"""

from crewai_tools import RagTool
from config import get_config
import os

def test_rag_tool():
    config = get_config()
    
    # Create RagTool with approach #1 - let it auto-manage
    rag_tool = RagTool(
        config=dict(
            llm=dict(
                provider="openai",
                config=dict(
                    model=config.candidate_profiler_model,
                    temperature=0.7,
                ),
            ),
            embedder=dict(
                provider="openai", 
                config=dict(
                    model="text-embedding-ada-002",
                ),
            ),
            chunker=dict(
                chunk_size=1000,
                chunk_overlap=200,
            ),
            vectordb=dict(
                provider="chroma",
                config=dict(
                    dir=os.path.abspath("test_vector_db"),  # Separate test DB
                    collection_name="test_knowledge_base",
                    allow_reset=True,
                ),
            ),
        )
    )
    
    # Add documents from knowledge-base directory
    print("Adding documents from knowledge-base directory...")
    try:
        rag_tool.add(os.path.abspath("knowledge-base"), data_type="directory")
        print("Documents added successfully!")
    except Exception as e:
        print(f"Error adding documents: {e}")
        # Alternative approach - add individual files
        import glob
        md_files = glob.glob("knowledge-base/**/*.md", recursive=True)
        print(f"Found {len(md_files)} markdown files")
        for file_path in md_files:
            try:
                rag_tool.add(file_path, data_type="text_file")
                print(f"Added: {file_path}")
            except Exception as e:
                print(f"Error adding {file_path}: {e}")
    
    print("RagTool created successfully!")
    print(f"Knowledge base directory: {os.path.abspath('knowledge-base')}")
    print(f"Test vector DB directory: {os.path.abspath('test_vector_db')}")
    
    # Test queries
    test_queries = [
        "What projects has Wesley worked on?",
        "Tell me about Wesley's experience with Python",
        "What is the bacworks project?",
        "What companies has Wesley worked with?"
    ]
    
    print("\n" + "="*50)
    print("TESTING RAG QUERIES")
    print("="*50)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n[Query {i}] {query}")
        print("-" * 40)
        try:
            result = rag_tool._run(query)
            print(f"Result: {result}")
        except Exception as e:
            print(f"Error: {e}")
    
    return rag_tool

if __name__ == "__main__":
    test_rag_tool()