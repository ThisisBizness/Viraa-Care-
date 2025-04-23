from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
import logging
import uuid # To generate unique session IDs
import os

# Import the chat logic functions
from chat_logic import send_message, start_new_chat, active_chats, logger

# Define the request body structure
class ChatRequest(BaseModel):
    session_id: str | None = None # Allow session ID to be optional for starting new chats
    message: str

# Define the response body structure
class ChatResponse(BaseModel):
    session_id: str
    response: str

# Initialize FastAPI app
app = FastAPI(
    title="Virra Care Chatbot MVP",
    description="A simple chatbot using FastAPI and Gemini 2.5 Flash",
    version="0.1.0"
)

# Mount static files (for the simple HTML frontend)
# Use a try-except block in case the directory doesn't exist during initial setup
try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
except RuntimeError as e:
    logger.warning(f"Could not mount static directory: {e}. Ensure 'static' directory exists.")

# --- API Endpoints ---

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def read_root(request: Request):
    """Serves the simple HTML chat interface."""
    # Check if static files are mounted correctly
    if any(route.name == "static" for route in request.app.router.routes):
        # Read the index.html file
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
    """Receives a user message, interacts with the Gemini model, and returns the response."""
    session_id = chat_request.session_id
    user_message = chat_request.message

    if not user_message:
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    # If no session_id is provided, start a new chat
    if not session_id:
        session_id = str(uuid.uuid4()) # Generate a new unique session ID
        try:
            start_new_chat(session_id)
            logger.info(f"Started new session: {session_id}")
        except Exception as e:
            logger.error(f"Failed to start new chat session {session_id}: {e}")
            raise HTTPException(status_code=500, detail=f"Could not initialize chat session: {e}")
    elif session_id not in active_chats:
        # Handle case where a session ID is provided but doesn't exist on the server
        # Option 1: Start a new chat with this ID (current behavior in send_message)
        # Option 2: Return an error
        # Let's stick with Option 1 for simplicity, start_new_chat will be called within send_message
        logger.warning(f"Session ID {session_id} provided but not found. A new chat will be started implicitly.")
        # Optional: Explicitly call start_new_chat here if preferred
        # try:
        #     start_new_chat(session_id)
        # except Exception as e:
        #     logger.error(f"Failed to start new chat session {session_id}: {e}")
        #     raise HTTPException(status_code=500, detail=f"Could not initialize chat session: {e}")

    try:
        # Get the response from the chat logic
        bot_response = await send_message(session_id, user_message)

        # Return the session ID and the bot's response
        return ChatResponse(session_id=session_id, response=bot_response)

    except HTTPException as e:
        # Re-raise HTTP exceptions
        raise e
    except Exception as e:
        logger.error(f"Unhandled exception in chat endpoint for session {session_id}: {e}")
        # Log the full traceback for debugging if possible
        # import traceback
        # logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"An internal server error occurred: {e}")

# --- Health Check Endpoint (Optional but good practice) ---
@app.get("/health", status_code=200)
async def health_check():
    """Simple health check endpoint."""
    return {"status": "ok"}

# --- Main execution block (for running locally with uvicorn) ---
if __name__ == "__main__":
    import uvicorn
    logger.info("Starting Uvicorn server locally...")
    # Make sure to create a .env file with your GOOGLE_API_KEY
    if not os.getenv("GOOGLE_API_KEY"):
        logger.warning("GOOGLE_API_KEY not set in environment. Please create a .env file.")

    uvicorn.run(
        "main:app",         # app instance is defined in main.py
        host="127.0.0.1",   # Listen on localhost
        port=8000,          # Standard port
        reload=True,        # Enable auto-reload for development
        log_level="info"    # Set uvicorn's log level
    ) 