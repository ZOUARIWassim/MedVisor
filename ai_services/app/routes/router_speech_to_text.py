import logging

from app.routes.schemas import AudioFileInput, TranscriptionResponse
from app.services.transcriber_service import transcribe_audio_file
from fastapi import APIRouter, HTTPException

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/")
def health():
    return {"message": "Speech to Text is running"}


@router.post("/transcribe", response_model=TranscriptionResponse)
def transcribe(payload: AudioFileInput):
    logger.info(f"Processing transcription request for file: {payload.file_path}")
    try:
        result = transcribe_audio_file(payload.file_path, payload.language_code)

        # The Google Cloud Speech-to-Text API returns a response object with a 'results' field,
        # each containing 'alternatives' with 'transcript' and 'confidence'.
        transcripts = []
        confidences = []
        for result_item in result.results:
            if result_item.alternatives:
                transcripts.append(result_item.alternatives[0].transcript)
                if hasattr(result_item.alternatives[0], "confidence"):
                    confidences.append(result_item.alternatives[0].confidence)
        transcription_text = " ".join(transcripts)
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0
        response = TranscriptionResponse(
            transcription=transcription_text, confidence=avg_confidence
        )

        return response
    except Exception as e:
        logger.error(f"API error while transcribing audio file from {payload.file_path}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
