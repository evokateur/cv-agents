"""
CLI entry point for the KB chat interface.
"""


def main():
    """Launch the KB chat Gradio UI."""
    from ui.kb_chat_app import launch

    launch()


if __name__ == "__main__":
    main()
