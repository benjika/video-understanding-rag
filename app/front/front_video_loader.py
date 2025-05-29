import os
import shutil
import requests
import gradio as gr
import json

import logging
logging.basicConfig(level=logging.INFO)

VIDEO_DIR = os.path.join(os.path.dirname(__file__),"..", "video")
os.makedirs(VIDEO_DIR, exist_ok=True)


def is_video_file(filename):
    return filename.lower().endswith(('.mp4', '.mov', '.avi', '.mkv'))

def analyze_uploaded_video(video_file):
    """Analyze the uploaded video file and return the result.
    Args:
        video_file (str): The path to the uploaded video file.
    Returns:
        str: The result of the analysis.
    """
    if not video_file:
        return "Please upload a video file."
    
    filename = os.path.basename(video_file.name)
    if not is_video_file(filename):
        return "Error: Uploaded file is not a supported video format (.mp4, .mov, .avi, .mkv)"

    file_path = os.path.join(VIDEO_DIR, filename)
    shutil.copy(video_file.name, file_path)

    try:
        with open(file_path, "rb") as f:
            response = requests.post(os.getenv("API_URL") + "analyze_video/", files={"video": (filename, f)}) # type: ignore
            logging.info(f"Response from API: {response}")
            if response.status_code != 200:
                logging.error(f"Error: {response.status_code} - {response.text}")
                return f"Error: {response.status_code} - {response.text}"
            else:
                response_json = response.json()
                if "result" in response_json:
                    result = response_json["result"]
                    formatted_result = json.dumps(result, indent=4)
                    return formatted_result
                else:
                    return f"Error: Unexpected response format: {response_json}"
    except Exception as e:
        return f"Error: {e}"
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

demo = gr.Interface(
    fn=analyze_uploaded_video,
    inputs=[
        gr.File(label="Upload a video", type="filepath"),
    ],
    outputs=gr.Textbox(label="Answer"),
    title="Video understanding with Gemini LLM",
    description="Upload a video. The model will understand and respond using Gemini."
)

def get_upload_tab():
    with gr.Tab("Upload a Video"):
        with gr.Row():
            video_input = gr.File(label="Upload a video", type="filepath")
        with gr.Row():
            analyze_btn = gr.Button("Analyze")
        video_output = gr.Textbox(label="LLM Video Analysis", lines=15)
        analyze_btn.click(fn=analyze_uploaded_video, inputs=video_input, outputs=video_output)