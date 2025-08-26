import chromadb

VECTOR_DB_PATH = "vector_db"


def main():
    client = chromadb.PersistentClient(path=VECTOR_DB_PATH)

    print("📂 Collections:")
    collections = client.list_collections()
    for coll in collections:
        print("-", coll.name)

    if not collections:
        print("⚠️ No collections found in this vector DB.")
        return

    collection_name = "knowledge_base"
    collection = client.get_collection(name=collection_name)
    print(f"\n🔍 Inspecting collection: {collection_name}")

    count = collection.count()
    print(f"Total documents: {count}")

    results = collection.get(include=["documents", "metadatas"], limit=3)
    print("\nSample entries:")
    for i, doc in enumerate(results["documents"]):
        print(f"\n--- Document {i + 1} ---")
        print(doc[:500], "..." if len(doc) > 500 else "")
        print("Metadata:", results["metadatas"][i])


if __name__ == "__main__":
    main()
