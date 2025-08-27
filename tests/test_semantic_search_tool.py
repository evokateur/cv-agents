import pytest
from optimizer.agents import CustomAgents


def test_semantic_search_tool_returns_sources():
    """Test that semantic search returns source paths"""
    agents = CustomAgents()
    tool = agents.get_semantic_search_tool()
    result = tool._run("PHP")
    assert "Source:" in result
    assert "/knowledge-base/" in result
    assert len(result.strip()) > 0