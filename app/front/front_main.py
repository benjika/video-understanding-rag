import gradio as gr
from app.front.front_video_loader import get_upload_tab
from app.front.front_db_chat import get_chat_tab

def create_gradio_interface():
    """Create the Gradio interface for the video LLM tool."""
    with gr.Blocks(title="Video LLM Tool") as demo:
        gr.Markdown("## 🧠 Video Understanding with Gemini + pgvector")
        get_upload_tab()
        get_chat_tab()
    return demo
