import os
import gradio as gr
from crewai import Agent, Task, Crew, LLM
from crewai_tools import RagTool
from optimizer.tools.knowledge_base_tool import KnowledgeBaseTool
from optimizer.config.settings import get_config

# Disable CrewAI tracing
os.environ["CREWAI_TRACING_ENABLED"] = "false"

# CrewAI RAGTool needs this env var for embeddings
if "CHROMA_OPENAI_API_KEY" not in os.environ and "OPENAI_API_KEY" in os.environ:
    os.environ["CHROMA_OPENAI_API_KEY"] = os.environ["OPENAI_API_KEY"]

# Cache tools to avoid re-embedding on every message
_tool_cache = {}


def create_kb_tool(tool_type: str):
    """Create the knowledge base tool based on selected type."""
    # Return cached tool if available
    if tool_type in _tool_cache:
        return _tool_cache[tool_type]

    config = get_config()

    if tool_type == "Custom KnowledgeBaseTool":
        tool = KnowledgeBaseTool(vector_db_path=config.vector_db_abspath)
    else:  # CrewAI RAGTool
        # Let RAGTool manage embedding on its own
        tool = RagTool(
            name="Knowledge base",
            description="A knowledge base that can be used to answer questions about the candidate's skills, projects, and experience.",
        )
        # Add knowledge base documents
        print(
            f"Initializing RAGTool with documents from: {config.knowledge_base_abspath}"
        )
        tool.add(config.knowledge_base_abspath)
        print("✓ RAGTool initialized")

    # Cache the tool
    _tool_cache[tool_type] = tool
    return tool


def create_kb_agent(model: str, temperature: float, tool_type: str):
    """Create an agent with access to the knowledge base."""
    kb_tool = create_kb_tool(tool_type)

    llm = LLM(model=model, temperature=temperature)

    agent = Agent(
        role="Technical Knowledge Assistant",
        goal="Answer questions using the knowledge base, providing direct, specific technical information",
        backstory="You have access to detailed project documentation and technical information. Provide straightforward, technical answers without business jargon or marketing language.",
        tools=[kb_tool],
        verbose=True,
        llm=llm,
    )

    return agent


def chat_with_kb(message, history, model, temperature, tool_type):
    """Process a chat message and return response."""
    agent = create_kb_agent(model, temperature, tool_type)

    # Build context from conversation history
    context = ""
    if history:
        context = "Previous conversation:\n"
        for user_msg, bot_msg in history:
            context += f"User: {user_msg}\nAssistant: {bot_msg}\n"
        context += "\n"

    task = Task(
        description=f"{context}Answer this question: {message}",
        expected_output="A direct, technical answer based on the knowledge base. Avoid business jargon, marketing language, and buzzwords. Be specific and concrete.",
        agent=agent,
    )

    crew = Crew(
        agents=[agent],
        tasks=[task],
        verbose=False,
    )

    try:
        result = crew.kickoff()
        response = result.raw if hasattr(result, "raw") else str(result)
        return response
    except Exception as e:
        return f"Error: {str(e)}"


def create_app():
    """Create the KB chat Gradio app."""

    with gr.Blocks(title="KB Chat") as app:
        gr.Markdown("# Knowledge Base Chat")
        gr.Markdown(
            "Ask questions about the candidate's experience, skills, and projects."
        )

        with gr.Row():
            model_selector = gr.Dropdown(
                label="Model",
                choices=[
                    "gpt-4o",
                    "gpt-4o-mini",
                    "anthropic/claude-sonnet-4-20250514",
                    "anthropic/claude-3-5-sonnet-20241022",
                    "anthropic/claude-3-5-haiku-20241022",
                    "deepseek/deepseek-chat",
                ],
                value="gpt-4o-mini",
                interactive=True,
            )
            temperature_slider = gr.Slider(
                label="Temperature",
                minimum=0.0,
                maximum=2.0,
                value=0.7,
                step=0.1,
                interactive=True,
            )
            tool_selector = gr.Dropdown(
                label="Tool",
                choices=["Custom KnowledgeBaseTool", "CrewAI RAGTool"],
                value="Custom KnowledgeBaseTool",
                interactive=True,
                info="Custom returns raw chunks, RAGTool may synthesize",
            )

        chatbot = gr.Chatbot(
            label="Chat",
            height=500,
        )

        with gr.Row():
            msg = gr.Textbox(
                label="Message",
                placeholder="Ask a question about the candidate's experience...",
                scale=4,
            )
            submit_btn = gr.Button("Send", variant="primary", scale=1)

        clear_btn = gr.Button("Clear Chat")

        def respond(message, chat_history, model, temperature, tool_type):
            if not message.strip():
                return chat_history, ""

            bot_response = chat_with_kb(
                message, chat_history, model, temperature, tool_type
            )
            chat_history.append((message, bot_response))
            return chat_history, ""

        def clear_chat():
            return []

        submit_btn.click(
            fn=respond,
            inputs=[msg, chatbot, model_selector, temperature_slider, tool_selector],
            outputs=[chatbot, msg],
        )

        msg.submit(
            fn=respond,
            inputs=[msg, chatbot, model_selector, temperature_slider, tool_selector],
            outputs=[chatbot, msg],
        )

        clear_btn.click(
            fn=clear_chat,
            outputs=[chatbot],
        )

    return app


def launch():
    """Launch the KB chat application."""
    app = create_app()
    app.launch(inbrowser=True)
