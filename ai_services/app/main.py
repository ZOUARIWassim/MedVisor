import logging

from app.routes import router_speech_to_text
from fastapi import FastAPI

# from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


@app.get("/")
async def check_health():
    return {"message": "AI Services is running"}


app.include_router(router_speech_to_text, prefix="/speech_to_text", tags=["speech_to_text"])
