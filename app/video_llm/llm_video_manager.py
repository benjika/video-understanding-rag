import time
from google import genai
import os
from dotenv import load_dotenv
import json

load_dotenv()

VIDEO_DIR =  os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "video"))

class LLM_Video_Manager:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment")

        self.client = genai.Client(api_key=api_key)

    def ask_llm_about_video(self, video_path: str) -> str:
        """
        Ask the LLM a question about a video and return the response.
        Args:
            prompt (str): The question to ask the LLM about the video.
            video_path (str): The path to the video file.
        Returns:
            str: The LLM's response to the question.
        """

        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file {video_path} not found in {VIDEO_DIR}")
        myfile = self.client.files.upload(file=video_path)
        
        for i in range(10):
            current_file_state = self.client.files.get(name=myfile.name)  # type: ignore
            if current_file_state.state == "PROCESSING":
                time.sleep(5)
            else:
                break
            
        structured_prompt = (
        "Return a dictionary with 2 fields:\n"
        "'chronological': make visual and audio description of the video chronologically and a timestamp, return it as a list,\n"
        "'summary': make a summary of the video.\n"
        "Respond in valid JSON format."
    )
        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[
                myfile,
                structured_prompt
            ]
        )
        
        text = response.text
        
        if not text:
            raise ValueError("No response from LLM.")
        
        json_start, json_end = text.find("{"), text.rfind("}") + 1 # type: ignore
        
        if json_start == -1 or json_end == -1:
            raise ValueError("Could not find JSON object in the log string.")
        
        raw_json = text[json_start : json_end + 1] # type: ignore

        response_json = json.loads(raw_json)        

        return response_json


    def ask_llm_questions_about_a_video(self, context:str, query:str) -> str:
        """
        Ask the LLM a question about a video and return the response.
        Args:
            context (str): The context to provide to the LLM.
            query (str): The question to ask the LLM.
        Returns:
            str: The LLM's response to the question.
        """

        prompt = (
        f"The following are highlights from videos:\n{context}\n\n"
        f"Answer the following question based on the highlights above:\n{query}"
        "ANSWER ONLY BASED ON THE HIGHLIGHTS ABOVE.\n"
        "DO NOT MAKE UP ANYTHING.\n"
        )

        response = self.client.models.generate_content(
            model="gemini-1.5-flash-latest",
            contents=prompt,
            )
        return response.text # type: ignore
