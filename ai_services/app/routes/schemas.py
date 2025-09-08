from pydantic import BaseModel


class TranscriptionResponse(BaseModel):
    transcription: str
    confidence: float


class AudioFileInput(BaseModel):
    file_path: str
    language_code: str
