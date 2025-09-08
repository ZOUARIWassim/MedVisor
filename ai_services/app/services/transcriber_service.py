import io
import logging
import wave

from app.modules.speech_to_text.transcriber import transcribe_audio
from app.utils.storage import read_file_from_gcs_uri

logger = logging.getLogger(__name__)


def transcribe_audio_file(file_path: str, language_code: str):
    logger.info(f"Reading audio file from {file_path}")
    try:
        audio_content = read_file_from_gcs_uri(file_path, "rb")
    except FileNotFoundError:
        logger.error(f"Audio file not found in {file_path}")
        raise FileNotFoundError(f"Audio file not found in gs://medvisor/{file_path}")
    except Exception as e:
        logger.error(f"Error reading audio file from {file_path}: {e}")
        raise e
    logger.info(f"Audio file read successfully from {file_path}")

    with wave.open(io.BytesIO(audio_content), "rb") as audio_file:
        sample_rate = audio_file.getframerate()
        channels = audio_file.getnchannels()

    return transcribe_audio(audio_content, sample_rate, channels, language_code)
