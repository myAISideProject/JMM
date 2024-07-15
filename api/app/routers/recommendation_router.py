from fastapi import APIRouter, HTTPException
from app.gpt.recommendation import fetch_random_ai_summarize_with_image
import time

router = APIRouter(prefix="/recommendation", tags=["recommendation"])

@router.get("/random-recommendation")
def get_random_ai_summarize():
    try:
        time.sleep(2)
        markdown_response = fetch_random_ai_summarize_with_image()
        return markdown_response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))