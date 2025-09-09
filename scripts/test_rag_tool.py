import sys

sys.path.append(".")

from crewai_tools.tools.rag.rag_tool import RagTool

from config import get_embedchain_config


def test_rag_tool():
    tool = RagTool(config=get_embedchain_config(), summarize=True)
    result = tool._run("data analysis experience")
    print("RAG TOOL:")
    print(result)


if __name__ == "__main__":
    test_rag_tool()
