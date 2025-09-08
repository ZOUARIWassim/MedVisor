import logging

from google.cloud import storage

logger = logging.getLogger(__name__)


def check_file_exists(file_path: str, bucket_name: str) -> bool:
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(file_path)
    logger.info(f"Checking if file exists: gs://{bucket_name}/{file_path}")
    try:
        exists = blob.exists()
    except Exception as e:
        logger.error(f"Error checking if file exists: {e}")
        return False
    logger.info(f"File exists: {exists}")
    return exists


def list_files_in_bucket(bucket_name: str, prefix: str = ""):
    """List files in the bucket for debugging"""
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    try:
        blobs = bucket.list_blobs(prefix=prefix)
        files = []
        for blob in blobs:
            files.append(blob.name)
            logger.info(f"Found file: {blob.name}")
        return files
    except Exception as e:
        logger.error(f"Error listing files in bucket {bucket_name} with prefix '{prefix}': {e}")
        return []


def read_file_from_storage(file_path: str, bucket_name: str):
    if not check_file_exists(file_path, bucket_name):
        # List files for debugging
        logger.info(
            f"File not found. Listing files in bucket {bucket_name} with prefix 'audio_files':"
        )
        list_files_in_bucket(bucket_name, "audio_files")
        raise FileNotFoundError(f"File {file_path} not found in bucket {bucket_name}")
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(file_path)
    try:
        return blob.download_as_bytes()
    except Exception as e:
        logger.error(f"Error downloading file {file_path} from bucket {bucket_name}: {e}")
        raise FileNotFoundError(
            f"Could not download file {file_path} from bucket {bucket_name}: {e}"
        )


def parse_gcs_uri(uri: str):
    if not uri or not uri.startswith("gs://"):
        raise ValueError(f"Invalid GCS URI: '{uri}'. Must start with 'gs://'.")
    prefix = "gs://"
    if uri.startswith(prefix):
        uri_ = uri[len(prefix) :]
    else:
        uri_ = uri
    parts = uri_.split("/", 1)
    if len(parts) != 2 or not parts[0] or not parts[1]:
        raise ValueError("URI missing bucket name or blob path after 'gs://'.")
    bucket_name, blob_name = parts
    return bucket_name, blob_name


def read_file_from_gcs_uri(uri: str, mode: str = "rb"):
    storage_client = storage.Client()
    bucket_name, blob_name = parse_gcs_uri(uri)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    if mode == "rb":
        return blob.download_as_bytes()
