from pydantic import BaseModel


class TranscriptionResponse(BaseModel):
    transcription: str
    confidence: float


class AudioFileInput(BaseModel):
    file_path: str
    language_code: str


class ReportGeneratorInput(BaseModel):
    report_data: dict
    patient_data: dict


class ReportGeneratorOutput(BaseModel):
    report_content: str
