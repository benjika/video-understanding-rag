from pydantic import BaseModel

class ChatQuery(BaseModel):
    query: str
    
class VideoAnalysisResponse(BaseModel):
    status: str
    result: dict
    
class ChatResponse(BaseModel):
    status: str
    result: str