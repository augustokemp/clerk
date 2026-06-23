from fastapi import FastAPI
from pydantic import BaseModel
import asyncio
from ask import answer

class AskRequest(BaseModel):
    question: str

class AskResponse(BaseModel):
    answer: str
    sources: list[str]

app = FastAPI(title="clerk")

@app.post("/ask", response_model=AskResponse)
async def ask(req: AskRequest):
    text, sources = await asyncio.to_thread(answer, req.question)
    return AskResponse(answer=text, sources=sources)