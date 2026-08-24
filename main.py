import asyncio
from datetime import datetime

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from starlette.background import BackgroundTask

app=FastAPI(title="AI Question API")

class AskRequest(BaseModel):
    question:str 

async def get_ai_answer(question: str) ->str:
    """
    Placeholder for real AI logic.
    Later, replace this with an actual LLM call
    (e.g. OpenAI, Anthropic, local model, etc.).
    """
    await asyncio.sleep(1)
    return f"This is answer for:{question}"


@app.get("/")
def home():
    return {"message":"AI API is running"}

@app.post("/ask")
async def ask_ai(request:AskRequest):
    answer=await get_ai_answer(request.question)
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
    return StreamingResponse(word_streamer(), media_type="text/plain")

def save_log(question:str, answer:str, complete:bool= True):
    tag= "" if complete else "[incomplete]"
    with open("ai_logs.txt","a",encoding="utf-8")as f:
        f.write(
            f"Time:{datetime.now()}\n"
            f"Question:{question}\n"
            f"Answer:{tag}{answer}\n"
            f"{'-' * 50}\n"
        )
async def generate_answer(question:str, collected:list[str]):


    answer =f"This is a streaming answer for: {question}"
    try:
        for word in answer.split():
            chunk=word + " "
            collected.append(chunk)
            yield chunk
            await asyncio.sleep(0.3)
    except asyncio.CancelledError:
        save_log(question,"".join(collected),complete=False)
        raise

@app.post("/ask/stream")
async def ask_stream(question:str):
    collected:list[str] = []
    response = StreamingResponse(
        generate_answer(question,collected),
        media_type="text/plain",
    )
    response.background=BackgroundTask(
        lambda:save_log(question, "".join(collected))
    )
    return response
@app.get("/multi-task")
async def multi_task():
    results=await asyncio.gather(
        get_ai_answer("explain Ai"),
        get_ai_answer("Explain loop engineering"),
        get_ai_answer("Explain RAG"),
    )
    return {
        "results":results
    }


