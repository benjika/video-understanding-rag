import os
import gradio as gr
import requests

import logging

def ask_question(query):
    """Ask a question about the video and get an answer from the LLM.
    Args:
        query (str): The question to ask.
    Returns:
        str: The answer from the LLM.
    """
    try:

        response = requests.post(os.getenv("API_URL") + "chat_with_db/", json={"query": query})
        logging.info(f"Response from API: {response}")
        if response.status_code == 200:
            return response.json()["result"]
        return f"Error {response.status_code}: {response.text}"
    except Exception as e:
        return f"Error: {e}"

demo = gr.Interface(
    fn=ask_question,
    inputs=gr.Textbox(placeholder="Ask about the video..."),
    outputs="text",
    title="Video Search Chatbot",
    description="Talk to your videos using LLM + pgvector"
)

def get_chat_tab():
    with gr.Tab("Ask About Video"):
        with gr.Row():
            question_input = gr.Textbox(
                label="Ask a question",
                placeholder="What happened in the video?",
                lines=2
            )
        chat_output = gr.Textbox(label="LLM Answer")
        ask_btn = gr.Button("Ask")
        ask_btn.click(fn=ask_question, inputs=question_input, outputs=chat_output)

if __name__ == "__main__":
    demo.launch()