from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    MODEL_NAME = "meta-llama/llama-4-scout-17b-16e-instruct"

    VECTOR_TOP_K = 15
    FINAL_TOP_K = 10

settings = Settings()