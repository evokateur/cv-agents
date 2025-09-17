import json
import logging
from datetime import datetime
from crewai.events import BaseEventListener, crewai_event_bus
from crewai.events import (
    CrewKickoffStartedEvent,
    CrewKickoffCompletedEvent,
    AgentExecutionCompletedEvent,
    KnowledgeRetrievalStartedEvent,
    KnowledgeRetrievalCompletedEvent,
    LLMStreamChunkEvent,
    MemoryQueryStartedEvent,
    MemoryQueryCompletedEvent,
    MemoryQueryFailedEvent
)


class CrewExecutionLogger(BaseEventListener):
    """Custom event listener for logging CrewAI execution details."""

    def __init__(self, log_file_path):
        self.log_file_path = log_file_path
        self.logger = logging.getLogger("CrewAI-Execution")

        # Create file handler for execution logs
        handler = logging.FileHandler(log_file_path)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        # Clear existing handlers to avoid duplicates
        self.logger.handlers.clear()
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
        self.logger.propagate = False  # Prevent duplicate logs

        # Register with the global event bus immediately
        self.setup_listeners(crewai_event_bus)
        self.logger.info("CrewExecutionLogger initialized and registered with event bus")

    def setup_listeners(self, crewai_event_bus):
        """Set up event listeners for various CrewAI events."""

        @crewai_event_bus.on(CrewKickoffStartedEvent)
        def on_crew_started(source, event):
            crew_name = getattr(event, 'crew_name', 'Unknown Crew')
            self.logger.info(f"🚀 Crew '{crew_name}' started execution")

        @crewai_event_bus.on(CrewKickoffCompletedEvent)
        def on_crew_completed(source, event):
            crew_name = getattr(event, 'crew_name', 'Unknown Crew')
            self.logger.info(f"✅ Crew '{crew_name}' completed successfully")
            if hasattr(event, 'result') and event.result:
                # Log result summary without overwhelming detail
                result_summary = str(event.result)[:500] + "..." if len(str(event.result)) > 500 else str(event.result)
                self.logger.info(f"Result summary: {result_summary}")

        @crewai_event_bus.on(AgentExecutionCompletedEvent)
        def on_agent_completed(source, event):
            agent_name = getattr(event, 'agent_name', 'Unknown Agent')
            self.logger.info(f"✅ Agent '{agent_name}' completed execution")
            if hasattr(event, 'output') and event.output:
                # Log output summary to avoid massive logs
                output_summary = str(event.output)[:300] + "..." if len(str(event.output)) > 300 else str(event.output)
                self.logger.info(f"   Output: {output_summary}")

        @crewai_event_bus.on(KnowledgeRetrievalStartedEvent)
        def on_knowledge_retrieval_started(source, event):
            self.logger.info("🔍 Knowledge retrieval started")

        @crewai_event_bus.on(KnowledgeRetrievalCompletedEvent)
        def on_knowledge_retrieval_completed(source, event):
            self.logger.info("✅ Knowledge retrieval completed")

        @crewai_event_bus.on(LLMStreamChunkEvent)
        def on_llm_stream_chunk(source, event):
            # Only log occasionally to avoid spam
            if hasattr(event, 'chunk') and len(str(event.chunk)) > 50:
                chunk_preview = str(event.chunk)[:50] + "..."
                self.logger.debug(f"🧠 LLM streaming: {chunk_preview}")

        @crewai_event_bus.on(MemoryQueryStartedEvent)
        def on_memory_query_started(source, event):
            self.logger.info("🧠 Memory query started")

        @crewai_event_bus.on(MemoryQueryCompletedEvent)
        def on_memory_query_completed(source, event):
            self.logger.info("✅ Memory query completed")

        @crewai_event_bus.on(MemoryQueryFailedEvent)
        def on_memory_query_failed(source, event):
            self.logger.error("❌ Memory query failed")
            if hasattr(event, 'error'):
                self.logger.error(f"   Error: {event.error}")