import time
from google import genai
import os
from dotenv import load_dotenv
import json

load_dotenv()

VIDEO_DIR =  os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "video"))

class LLM_Video_Manager:
    def __init__(self):
        self.client = genai.Client()

    def ask_llm_about_video(self, video_name: str = "John_Youngs_Lunar_Salute_on_Apollo_16.mp4") -> str:
        """
        Ask the LLM a question about a video and return the response.
        Args:
            prompt (str): The question to ask the LLM about the video.
            video_name (str): The name of the video file to analyze.
        Returns:
            str: The LLM's response to the question.
        """
        video_path = os.path.join(VIDEO_DIR, video_name)
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file {video_name} not found in {VIDEO_DIR}")
        myfile = self.client.files.upload(file=video_path)
        
        for i in range(10):
            current_file_state = self.client.files.get(name = myfile.name) # type: ignore
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

        text = text.replace("```","").replace("json","")
        try:
            response_json = json.loads(text)
        except json.JSONDecodeError:
            raise ValueError("Response is not valid JSON.")

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
