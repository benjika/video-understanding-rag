import gradio as gr
from front_video_loader import get_upload_tab
from front_db_chat import get_chat_tab

with gr.Blocks(title="Video LLM Tool") as demo:
    gr.Markdown("## 🧠 Video Understanding with Gemini + pgvector")
    get_upload_tab()
    get_chat_tab()

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)