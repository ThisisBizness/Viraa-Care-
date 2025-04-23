import google.generativeai as genai
import os
from dotenv import load_dotenv
import logging
from google.generativeai.types import GenerationConfig
from google.ai.generativelanguage import SafetySetting, HarmCategory

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    logger.error("GOOGLE_API_KEY not found in environment variables.")
    # You might want to raise an exception or handle this case appropriately
    # For now, we'll allow it to proceed but genai.configure will likely fail
    # raise ValueError("GOOGLE_API_KEY not found. Please set it in your .env file.")

try:
    genai.configure(api_key=API_KEY)
except Exception as e:
    logger.error(f"Failed to configure Google Generative AI: {e}")
    # Handle configuration error, perhaps exit or return an error state

# --- Model Configuration ---
MODEL_NAME = "gemini-2.5-flash-preview-04-17"

# System Prompt defining the chatbot's persona and behavior
SYSTEM_PROMPT = """
**Your Role and Persona:**
You are a highly experienced virtual assistant for Viraa Care. Your persona is that of a composite expert embodying the knowledge, wisdom, and demeanor of a seasoned Pediatrician, Child Psychologist, and Clinician, each with over 40 years of experience. You specialize in supporting parents of children from birth to 1000 days old.

**Your Tone:**
Maintain a tone that is:
* **Empathetic and Reassuring:** Acknowledge parental concerns and anxieties with understanding.
* **Patient and Calm:** Never rush to conclusions.
* **Knowledgeable and Confident:** Draw upon a deep understanding of child development, health, and psychology for this age group.
* **Professional:** Provide information clearly and responsibly.
* **Accessible:** Avoid overly technical jargon. Explain concepts simply.

**Core Interaction Protocol (CRITICAL):**
1.  **Receive User Query:** A parent will ask a question about their child (0-1000 days) or parenting.
2.  **DO NOT ANSWER IMMEDIATELY.** Your absolute first step is to understand the situation thoroughly.
3.  **Acknowledge and Initiate Clarification:** Briefly acknowledge the parent's query/concern. Then, begin asking clarifying questions to gather necessary details.
4.  **Ask Sufficient Questions:** Use your 'Thinking' capability to analyze the user's query and subsequent responses. Ask targeted questions about:
    * Child's specific age (in days, weeks, or months – be precise).
    * Specific symptoms/behaviors (description, frequency, duration, severity).
    * Feeding details (breastmilk, formula, solids, schedule, issues).
    * Sleep patterns (naps, night sleep, routines, wakings).
    * Developmental context (milestones, recent changes).
    * Environmental factors (routine changes, family situation).
    * The parent's specific worry or goal.
5.  **Iterate if Necessary:** If the parent's answers are incomplete or raise new questions, ask further follow-up questions. Continue this process until you are satisfied that you have a comprehensive understanding of the situation. Explicitly state when you need more information.
6.  **Provide Comprehensive Answer:** ONLY AFTER you have gathered sufficient information, provide a thoughtful, detailed, and evidence-informed response based on your expert persona. Structure your answer logically. Explain potential causes or factors. Offer general guidance, age-appropriate strategies, and things to look out for.
7.  **Mandatory Disclaimer:** ALWAYS conclude your substantive answers with a clear disclaimer stating that you are an AI assistant, the information is for educational/informational purposes only, it does not constitute medical advice, and the parent should consult a qualified healthcare professional (like their pediatrician) for diagnosis, treatment, or urgent concerns. Tailor the urgency advice (e.g., "seek immediate medical attention if...") based on the context if appropriate, but always defer to real-world professionals.

**Scope of Knowledge:**
Focus on common topics for the 0-1000 day range: feeding (breastfeeding, formula, starting solids), sleep (schedules, regressions, safe sleep), developmental milestones (motor, cognitive, social-emotional), common infant/toddler illnesses (recognizing symptoms, when to call the doctor), behavior (crying, colic, tantrums), introducing routines, parental self-care related to infant care, basic safety.

**Limitations:**
* Do NOT diagnose medical conditions.
* Do NOT prescribe medication or specific treatments.
* Do NOT provide emergency medical advice. Always redirect to emergency services or immediate medical consultation in such cases.
* Clearly state when a question falls outside your expertise or requires in-person medical evaluation.
"""

# Generation Configuration
generation_config = GenerationConfig(
    temperature=0.7, # Adjust for creativity vs. consistency
    top_p=0.95,
    top_k=64,
    max_output_tokens=65536, # Max output specified by model details
    response_mime_type="text/plain",
)

# Safety Settings - Adjust as needed, be cautious with medical advice context
safety_settings = [
    SafetySetting(
        category=HarmCategory.HARM_CATEGORY_HARASSMENT, 
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
    ),
    SafetySetting(
        category=HarmCategory.HARM_CATEGORY_HATE_SPEECH, 
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
    ),
    SafetySetting(
        category=HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT, 
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
    ),
    SafetySetting(
        category=HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT, 
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
    ),
    # Example using different threshold enum:
    # SafetySetting(
    #     category=HarmCategory.HARM_CATEGORY_MEDICAL, 
    #     threshold=SafetySetting.HarmBlockThreshold.BLOCK_ONLY_HIGH
    # ),
]

# --- Chat Session Management ---

# Store active chat sessions in memory (suitable for MVP)
# Key: session_id (string), Value: genai.ChatSession object
active_chats = {}

def start_new_chat(session_id: str):
    """Starts a new chat session with the specified configuration."""
    logger.info(f"Starting new chat session: {session_id}")
    try:
        model = genai.GenerativeModel(
            model_name=MODEL_NAME,
            safety_settings=safety_settings,
            generation_config=generation_config,
            system_instruction=SYSTEM_PROMPT,
            # Enable thinking mode - Requires specific SDK support or parameter name
            # As of google-generativeai 0.7.1, direct 'thinking_enabled' isn't obvious.
            # This might be implicitly handled or require a specific API version/flag.
            # We will proceed assuming the model uses its capabilities when appropriate.
            # Consider adding specific tools/function calls if needed later.
        )
        chat_session = model.start_chat(history=[]) # Start with empty history
        active_chats[session_id] = chat_session
        return chat_session
    except Exception as e:
        logger.error(f"Error initializing model or starting chat for session {session_id}: {e}")
        raise

async def send_message(session_id: str, message: str):
    """Sends a message to the chat session and returns the response."""
    if session_id not in active_chats:
        logger.warning(f"Session ID {session_id} not found. Starting new chat.")
        start_new_chat(session_id) # Or handle as an error depending on desired behavior

    chat_session = active_chats[session_id]

    try:
        logger.info(f"Sending message to session {session_id}: '{message[:50]}...'")
        # Use send_message_async for FastAPI's async nature
        response = await chat_session.send_message_async(message)
        logger.info(f"Received response for session {session_id}")

        # Basic check for blocked response due to safety
        if not response.parts:
             logger.warning(f"Response potentially blocked for session {session_id}. Finish reason: {response.prompt_feedback.block_reason}")
             # Consider checking response.candidates[0].finish_reason == "SAFETY"
             if response.prompt_feedback.block_reason:
                 return f"My apologies, but I cannot respond to that due to safety guidelines ({response.prompt_feedback.block_reason}). Could you please rephrase or ask something else?"
             else:
                 # Might be another reason like MAX_TOKENS, RECITATION etc.
                 return "I'm sorry, I encountered an issue generating a response. Please try again."


        # Accessing the text content
        # Iterating through parts is safer if multiple parts could exist
        response_text = "".join(part.text for part in response.parts)

        # Log history count for debugging
        logger.debug(f"Session {session_id} history length: {len(chat_session.history)}")

        return response_text

    except Exception as e:
        logger.error(f"Error during send_message for session {session_id}: {e}")
        # More specific error handling could be added here based on API errors
        # e.g., handle ResourceExhaustedError, InternalServerError, etc.
        return f"Sorry, I encountered an error trying to process your request: {e}"

# Optional: Function to clean up old sessions if needed
# def cleanup_inactive_sessions():
#     # Logic to identify and remove old sessions from active_chats
#     pass 