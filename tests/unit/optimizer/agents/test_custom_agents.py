import pytest
import os
from crewai_tools import RagTool

from optimizer.agents import CustomAgents
from optimizer.utils.vector_utils import is_valid_chroma_vector_db
from config import get_config


class TestCustomAgents:
    
    def test_get_rag_tool_creates_valid_vector_db(self):
        """Test that get_rag_tool creates a working RagTool with valid vector DB."""
        config = get_config()
        
        # Check if knowledge base exists (required for test)
        if not os.path.exists(config.knowledge_base_abspath):
            pytest.skip(f"Knowledge base not found at {config.knowledge_base_abspath}")
        
        # Check if we have required API keys
        if not os.getenv('OPENAI_API_KEY'):
            pytest.skip("OPENAI_API_KEY not set - required for RAG tool creation")
        
        agents = CustomAgents()
        rag_tool = agents.get_rag_tool()
        
        # Verify it returns a RagTool instance
        assert isinstance(rag_tool, RagTool)
        assert rag_tool.name == "CandidateKnowledgeBase"
        
        # Verify the vector DB was created and is valid
        assert os.path.exists(config.vector_db_abspath)
        assert is_valid_chroma_vector_db(config.vector_db_abspath)
    
    def test_get_rag_tool_reuses_existing_vector_db(self):
        """Test that get_rag_tool reuses an existing valid vector DB."""
        config = get_config()
        
        if not os.path.exists(config.knowledge_base_abspath):
            pytest.skip(f"Knowledge base not found at {config.knowledge_base_abspath}")
        
        if not os.getenv('OPENAI_API_KEY'):
            pytest.skip("OPENAI_API_KEY not set - required for RAG tool creation")
        
        agents = CustomAgents()
        
        # First call - should create or verify vector DB
        first_rag_tool = agents.get_rag_tool()
        assert isinstance(first_rag_tool, RagTool)
        
        # Verify vector DB exists after first call
        vector_db_exists_before = os.path.exists(config.vector_db_abspath)
        assert vector_db_exists_before
        
        # Second call - should reuse existing vector DB
        second_rag_tool = agents.get_rag_tool()
        assert isinstance(second_rag_tool, RagTool)
        assert second_rag_tool.name == "CandidateKnowledgeBase"
        
        # Vector DB should still exist and be valid
        assert os.path.exists(config.vector_db_abspath)
        assert is_valid_chroma_vector_db(config.vector_db_abspath)