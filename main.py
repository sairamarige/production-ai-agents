import asyncio
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

app=FastAPI(title="AI Question API")

class AskRequest(BaseModel):
    question:str 

def get_ai_answer(question:str) ->str:
    return f"This is answer for:{question}"
@app.get("/")
def home():
    return {"message":"AI API is running"}

@app.post("/ask")
def ask_ai(request:AskRequest):
    answer=get_ai_answer(request.question)
    return {"question": request.question,
        "answer": answer
    }
async def word_streamer():
    Words=[
        "AI",
        "agents",
        "are",
        "powerful",
        "when",
        "they",
        "can",
        "respond",
        "progressively"
    ]
    for  word in Words:
        yield word + " "
        await asyncio.sleep(0.5)
@app.get("/stream")
def stream_words():
    return StreamingResponse(word_streamer(),media_type="text/plain")
    
