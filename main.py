from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
import logging
import uuid # To generate unique session IDs
import os

# Import the chat logic functions
# Note the rename of send_message to generate_answer_for_question in chat_logic
# but we can keep calling it send_message here for consistency if we alias it back in chat_logic.py
# For clarity, let's use the new name from chat_logic.py
from chat_logic import generate_answer_for_question, start_new_chat, active_models, logger # active_models instead of active_chats

# Define the request body structure
class ChatRequest(BaseModel):
    session_id: str | None = None
    message: str # This will now be the text of the selected question
    language: str | None = "en" # Add language, default to English

# Define the response body structure
class ChatResponse(BaseModel):
    session_id: str
    response: str # This will be the detailed answer
    media: dict | None = None # Video and audio information

# Initialize FastAPI app
app = FastAPI(
    title="Viraa Care Categorical Assistant MVP",
    description="A menu-driven assistant using FastAPI and Gemini",
    version="0.2.0"
)

# Mount static files
try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
except RuntimeError as e:
    logger.warning(f"Could not mount static directory: {e}. Ensure 'static' directory exists.")

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def read_root(request: Request):
    """Serves the HTML interface."""
    if any(route.name == "static" for route in request.app.router.routes):
        try:
            with open("static/index.html", "r") as f:
                html_content = f.read()
            return HTMLResponse(content=html_content)
        except FileNotFoundError:
             logger.error("static/index.html not found.")
             raise HTTPException(status_code=404, detail="Frontend not found.")
    else:
        logger.error("Static files directory not mounted correctly.")
        raise HTTPException(status_code=500, detail="Server configuration error: Static files not served.")

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(chat_request: ChatRequest):
    """
    Receives a selected question, interacts with the Gemini model via chat_logic,
    and returns the detailed answer.
    """
    session_id = chat_request.session_id
    selected_question = chat_request.message
    language = chat_request.language or "en" # Ensure language is set, default to English

    if not selected_question:
        raise HTTPException(status_code=400, detail="Selected question (message) cannot be empty.")

    if not session_id:
        session_id = str(uuid.uuid4())
        try:
            start_new_chat(session_id) # Ensures model instance is ready
            logger.info(f"Initialized resources for new session: {session_id}")
        except Exception as e:
            logger.error(f"Failed to initialize for new session {session_id}: {e}")
            raise HTTPException(status_code=500, detail=f"Could not initialize session resources: {str(e)}")
    elif session_id not in active_models: # Check active_models now
        logger.warning(f"Session ID {session_id} provided but no active model. Initializing.")
        try:
            start_new_chat(session_id)
        except Exception as e:
            logger.error(f"Failed to initialize for existing session ID {session_id}: {e}")
            raise HTTPException(status_code=500, detail=f"Could not initialize session resources: {str(e)}")

    try:
        # Get the detailed answer from the chat logic
        bot_answer = generate_answer_for_question(session_id, selected_question, language)
        
        # Add media information (for POC - same video/audio for all responses)
        media_info = {
            "video": {
                "url": "/static/media/demo-video.mp4",
                "type": "video/mp4",
                "poster": "/static/media/demo-video-poster.jpg"  # Optional poster image
            },
            "audio": {
                "url": "/static/media/demo-audio.mp3",
                "type": "audio/mpeg"
            }
        }
        
        return ChatResponse(session_id=session_id, response=bot_answer, media=media_info)

    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Unhandled exception in chat endpoint for session {session_id}: {e}")
        raise HTTPException(status_code=500, detail=f"An internal server error occurred: {str(e)}")

@app.get("/health", status_code=200)
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting Uvicorn server locally...")
    if not os.getenv("GOOGLE_API_KEY"):
        logger.warning("GOOGLE_API_KEY not set in environment. Please create a .env file.")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, log_level="info")