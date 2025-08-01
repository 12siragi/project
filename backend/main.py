from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import os
import logging
from dotenv import load_dotenv
from simple_rag import initialize_simple_rag, query_simple_rag

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = FastAPI(
    title="AskAfrica API",
    description="AI Q&A API powered by local Ollama LLM with RAG capabilities",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class QuestionRequest(BaseModel):
    question: str
    use_rag: bool = False  # New parameter to enable RAG

class QuestionResponse(BaseModel):
    answer: str
    model: str
    source: str = "ollama"  # "ollama" or "book_rag"

# Ollama configuration
OLLAMA_URL = "http://localhost:11434"
MODEL_NAME = os.getenv("OLLAMA_MODEL", "saidgpt")

# Initialize RAG system on startup
@app.on_event("startup")
async def startup_event():
    """Initialize RAG system on startup"""
    logger.info("🚀 Initializing AskAfrica API...")
    
    # Try to initialize RAG system
    try:
        rag_success = initialize_simple_rag()
        if rag_success:
            logger.info("✅ Simple RAG system initialized successfully")
        else:
            logger.warning("⚠️  RAG system not available - will use Ollama only")
    except Exception as e:
        logger.error(f"❌ Error initializing RAG system: {e}")

@app.get("/")
async def root():
    return {"message": "AskAfrica API is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "model": MODEL_NAME}

@app.post("/ask", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest):
    """
    Send a question to the local Ollama LLM or RAG system and return the response.
    """
    try:
        logger.info(f"Processing question: {request.question[:50]}...")
        
        # If RAG is requested and available, use it
        if request.use_rag:
            logger.info("Using simple RAG system for book-specific answer")
            try:
                rag_answer = query_simple_rag(request.question)
                return QuestionResponse(
                    answer=rag_answer,
                    model="simple_rag",
                    source="book_rag"
                )
            except Exception as rag_error:
                logger.error(f"RAG error: {rag_error}")
                # Fall back to Ollama if RAG fails
                logger.info("Falling back to Ollama")
        
        # Use Ollama for general questions or as fallback
        logger.info("Using Ollama for general answer")
        
        async with httpx.AsyncClient(timeout=200.0) as client:
            ollama_payload = {
                "model": MODEL_NAME,
                "prompt": request.question,
                "stream": False
            }
            
            logger.info(f"Sending request to Ollama with model: {MODEL_NAME}")
            
            response = await client.post(
                f"{OLLAMA_URL}/api/generate",
                json=ollama_payload
            )
            
            logger.info(f"Ollama response status: {response.status_code}")
            
            if response.status_code != 200:
                error_detail = f"Ollama API error: {response.status_code}"
                try:
                    error_response = response.json()
                    error_detail += f" - {error_response}"
                except:
                    pass
                raise HTTPException(status_code=500, detail=error_detail)
            
            try:
                ollama_response = response.json()
                answer = ollama_response.get("response", "")
                
                if not answer:
                    raise HTTPException(
                        status_code=500,
                        detail="Ollama returned empty response"
                    )
                
                logger.info(f"Successfully processed question, response length: {len(answer)}")
                
                return QuestionResponse(
                    answer=answer,
                    model=MODEL_NAME,
                    source="ollama"
                )
                
            except Exception as json_error:
                logger.error(f"Error parsing Ollama response: {json_error}")
                raise HTTPException(
                    status_code=500,
                    detail=f"Error parsing Ollama response: {str(json_error)}"
                )
            
    except httpx.ConnectError as e:
        logger.error(f"Connection error to Ollama: {e}")
        raise HTTPException(
            status_code=503,
            detail="Cannot connect to Ollama. Make sure Ollama is running on localhost:11434"
        )
    except httpx.TimeoutException as e:
        logger.error(f"Timeout error: {e}")
        raise HTTPException(
            status_code=504,
            detail="Request to Ollama timed out. Try again."
        )
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)