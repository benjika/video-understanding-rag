import json
import time
from fastapi import APIRouter, UploadFile, File, Depends
from fastapi.responses import JSONResponse
import os
from app.db.db_manager import DBManager
from app.video_llm.llm_video_manager import LLM_Video_Manager
from app.api.schemas import ChatQuery, ChatResponse, VideoAnalysisResponse, AnalyzeVideoResponse


VIDEO_DIR = os.path.join(os.path.dirname(__file__), "video")
os.makedirs(VIDEO_DIR, exist_ok=True)
router = APIRouter()
video_manager = LLM_Video_Manager()

def get_db():
    db = DBManager()
    try:
        yield db
    finally:
        db.close()

@router.post("/analyze_video/", response_model=AnalyzeVideoResponse)
async def analyze_video(
    video: UploadFile = File(...),
    db: DBManager = Depends(get_db) 
    ):
    """
    Analyze the uploaded video and return the result.
    Args:
        video (UploadFile): The uploaded video file.
        db (DBManager): The database manager instance.
    Returns:
        AnalyzeVideoResponse: The response containing the analysis result.
    """

    video_path = os.path.abspath(os.path.join(VIDEO_DIR, video.filename)) # type: ignore
    try:
        with open(video_path, "wb") as f:
            f.write(await video.read())
            
        result = video_manager.ask_llm_about_video(video_path=video_path) # type: ignore

        timestamp = time.time()
        db.save_highlight(
            video_id=video.filename, # type: ignore
            timestamp=timestamp,
            description=json.dumps(result["chronological"]), # type: ignore
            summary=result["summary"] # type: ignore
        )

        return AnalyzeVideoResponse(status="success", result=result)
    finally:
        if os.path.exists(video_path):
            os.remove(video_path)

@router.post("/chat_with_db/", response_model=ChatResponse)
async def chat_with_db_endpoint(
    payload: ChatQuery,
    db: DBManager = Depends(get_db)
    ):
    """
    Chat with the database using a query.
    Args:
        payload (ChatQuery): The query payload containing the user's question.
        db (DBManager): The database manager instance.
    Returns:
        ChatResponse: The response containing the answer to the user's question.
    """
    query = payload.query
    context = db.search_similar_highlights(query)
    llm_answer = video_manager.ask_llm_questions_about_a_video(context=context, query=query) # type: ignore

    return ChatResponse(status="success", result=llm_answer)
