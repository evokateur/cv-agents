"""Wrapper for ChunkyRagTool that provides clean, agent-friendly output"""

from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Any, Type
from optimizer.tools.chunky_rag_tool import ChunkyRagTool
import json


class SemanticSearchInput(BaseModel):
    query: str = Field(
        ...,
        description="The search query or question to ask the knowledge base"
    )


class SemanticSearchWrapper(BaseTool):
    name: str = "Knowledge base"
    description: str = "A knowledge base that can be used to answer questions."
    args_schema: Type[BaseModel] = SemanticSearchInput
    chunky_tool: Any = None

    def __init__(self, config: dict = None, **kwargs):
        super().__init__(**kwargs)
        self.chunky_tool = ChunkyRagTool(config=config)

    def _run(self, query: str) -> str:
        json_result = self.chunky_tool._run(query)

        # Parse the JSON response
        data = json.loads(json_result)

        # Extract answer and source paths
        answer = data["answer"]
        sources = [src["metadata"]["url"] for src in data["sources"]]

        # Format in clean, agent-friendly format
        result = f"{answer}\n\nSources:\n"
        for source in sources:
            result += f"- {source}\n"

        return result.strip()

    async def _arun(self, query: str) -> str:
        return self._run(query)
