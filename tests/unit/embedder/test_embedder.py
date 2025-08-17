from embedding_tool import KnowledgeBaseEmbedder


def test_create_embeddings():
    embedder = KnowledgeBaseEmbedder()
    result = embedder.create_embeddings()
    assert result["status"] == "success"

    vectorstore = embedder.get_vectorstore()
    assert vectorstore is not None

    query = "bacworks"
    results = vectorstore.similarity_search(query, k=5)
    assert len(results) > 0
