import logging
import os
import time

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(),           # prints to console
        logging.FileHandler("app.log"),    # Task 5: saves to app.log
    ],
)

logger = logging.getLogger(__name__)

app = FastAPI(title="AI API")


class Question(BaseModel):
    question: str


def generate_ai_response(question: str) -> str:
  
    if not question.strip():
        raise ValueError("Question cannot be empty")
    # Simulated "processing"
    time.sleep(0.1)
    return f"AI answer to: {question}"


# Application level logging

@app.on_event("startup")
async def on_startup():
    logger.info("Application started")


@app.on_event("shutdown")
async def on_shutdown():
    logger.info("Application shutting down")



@app.post("/ask")
async def ask(payload: Question):
    logger.info("Request received")

    logger.info("AI question received (length=%d chars)", len(payload.question))

    logger.debug("Processing started")
    try:
        answer = generate_ai_response(payload.question)
    except Exception:
        logger.exception("AI response generation failed")
        raise HTTPException(status_code=500, detail="AI response generation failed")

    logger.debug("Processing completed")
    logger.info("AI response generated successfully")

    return {"answer": answer}



@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    logger.info("WebSocket connection established")
    logger.info("Client connected")

    try:
        while True:
            message = await websocket.receive_text()
            logger.info("Message received")
            logger.debug("Received message length=%d", len(message))

            try:
                response = generate_ai_response(message)
                await websocket.send_text(response)
                logger.info("Response sent")
            except Exception:
                logger.exception("AI response generation failed")
                await websocket.send_text("Error: could not generate a response")

    except WebSocketDisconnect:
        logger.info("WebSocket disconnected")
        logger.info("Client disconnected")