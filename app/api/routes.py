import json
import time
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
import os
from db.db_manager import DBManager
from video_llm.llm_video_manager import LLM_Video_Manager
from api.schemas import ChatQuery, ChatResponse


VIDEO_DIR = os.path.join(os.path.dirname(__file__), "video")
os.makedirs(VIDEO_DIR, exist_ok=True)
router = APIRouter()
video_manager = LLM_Video_Manager()

@router.post("/analyze_video/")
async def analyze_video(
    video: UploadFile = File(...),
    ):
    """
    Analyze the uploaded video and return the result.
    Args:
        video (UploadFile): The uploaded video file.
    """

    video_path = os.path.join(VIDEO_DIR, video.filename) # type: ignore
    with open(video_path, "wb") as f:
        f.write(await video.read())
        

    result = video_manager.ask_llm_about_video(video_name=video.filename) # type: ignore

    timestamp = time.time()
    db_manager = DBManager()
    db_manager.save_highlight(
        video_id=video.filename, # type: ignore
        timestamp=timestamp,
        description=json.dumps(result["chronological"]), # type: ignore
        summary=result["summary"] # type: ignore
    )
    db_manager.close()

    return JSONResponse(content={"status": "success", "result": result})

@router.post("/chat_with_db/", response_model=ChatResponse)
async def chat_with_db_endpoint(payload: ChatQuery):
    """
    Chat with the database using a query.
    """
    query = payload.query

    db = DBManager()
    context = db.search_similar_highlights(query)
    db.close()

    llm_answer = video_manager.ask_llm_questions_about_a_video(context=context, query=query) # type: ignore
    
    return {"status": "success", "result": llm_answer}
