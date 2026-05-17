from groq import Groq
from app.config import settings
from app.models.api_models import LLMExtractionSchema  # Use the specialized extraction schema

client = Groq(
    api_key=settings.GROQ_API_KEY
)

def generate_response(messages, temperature=0.0):
    completion = client.chat.completions.create(
        model=settings.MODEL_NAME,
        messages=messages,
        temperature=0.0,
        response_format={
            "type": "json_object",
            "schema": LLMExtractionSchema.model_json_schema()  # Strict targeting
        }
    )
    return completion.choices[0].message.content