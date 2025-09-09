from google import genai
from google.genai import types


def create_client():
    return genai.Client(vertexai=True, location="europe-west1")


def generate_content(
    model: str, contents: list[types.Content], config: types.GenerateContentConfig = None
):
    client = create_client()
    response = client.models.generate_content(model=model, contents=contents, config=config)
    if response.parsed:
        return response.parsed
    elif response.text:
        return response.text
    else:
        return response
