# chroma_test.py

from dotenv import load_dotenv
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
import os

# UPDATE THIS to point to your existing vector DB path from VectorDbBuilder
VECTOR_DB_PATH = "vector_db"


def main():
    load_dotenv()
    if not os.path.exists(VECTOR_DB_PATH):
        print(f"Vector DB path does not exist: {VECTOR_DB_PATH}")
        return

    print(f"Loading Chroma DB from: {VECTOR_DB_PATH}")

    try:
        vectordb = Chroma(
            persist_directory=VECTOR_DB_PATH,
            embedding_function=OpenAIEmbeddings(),
            collection_name="knowledge_base",
        )

        retriever = vectordb.as_retriever()
        query = "What is an autonomous agent?"

        results = retriever.get_relevant_documents(query)

        if not results:
            print("No documents found for the query.")
        else:
            print(f"\n🔍 Top {len(results)} results:\n")
            for i, doc in enumerate(results, 1):
                source = doc.metadata.get("source", "Unknown")
                print(f"[{i}] Source: {source}")
                print(doc.page_content[:200])
                print("-" * 60)

    except Exception as e:
        print(f"❌ Failed to load Chroma DB or run query: {e}")


if __name__ == "__main__":
    main()
