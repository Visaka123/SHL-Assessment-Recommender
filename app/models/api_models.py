from pydantic import BaseModel, Field
from typing import List

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]

# --- 1. WHAT WE FORCE GROQ TO RESPOND WITH ---
class LLMExtractionSchema(BaseModel):
    analysis_and_reasoning: str = Field(
        description="Write a natural language paragraph explaining why these specific assessments fit the user's role/skills requirement."
    )
    selected_assessment_names: List[str] = Field(
        description="List of the exact assessment names chosen from the allowed checklist."
    )

# --- 2. WHAT YOUR FASTAPI ENDPOINT ACTUALLY RETURNS TO THE USER ---
class Recommendation(BaseModel):
    name: str
    url: str
    test_type: str
    job_levels: List[str]
    duration: str
    score: float

class ChatResponse(BaseModel):
    reply: str
    recommendations: List[Recommendation]
    end_of_conversation: bool