import logging

from google.cloud import speech

logger = logging.getLogger(__name__)

client = speech.SpeechClient()


def transcribe_audio(
    audio_content: bytes,
    sample_rate: int,
    channels: int,
    language_code: str = "en-US",
):
    logger.info("Transcribing audio file...")
    audio = speech.RecognitionAudio(content=audio_content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=sample_rate,
        audio_channel_count=channels,
        enable_separate_recognition_per_channel=False,
        language_code=language_code,
    )
    response = client.recognize(config=config, audio=audio)
    logger.info("Audio file transcribed successfully")
    return response
