"""
FastAPI backend for CE Email Summarization Tool

Provides REST API endpoints for summarizing customer support email threads
using NLP (Hugging Face Transformers).
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from pathlib import Path
import logging
import json

from models import (
    Thread,
    ThreadSummary,
    SummarizeRequest,
    SummarizeResponse,
    ErrorResponse
)
from summarizer import get_summarizer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global instances
summarizer = None
threads_data = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize resources on startup and cleanup on shutdown"""
    global summarizer, threads_data
    logger.info("🚀 Starting CE Email Summarizer API...")

    # Load threads data
    try:
        threads_file = Path(__file__).parent / "threads.json"
        with open(threads_file, 'r') as f:
            threads_data = json.load(f)
        logger.info(f"✓ Loaded {len(threads_data.get('threads', []))} email threads")
    except Exception as e:
        logger.error(f"⚠️  Error loading threads data: {e}")
        threads_data = {"threads": []}

    # Initialize summarizer (loads model)
    try:
        summarizer = get_summarizer()
        logger.info("✓ NLP model loaded successfully")
    except Exception as e:
        logger.error(f"⚠️  Error loading model: {e}")
        logger.info("   API will use fallback summarization")

    yield

    # Cleanup
    logger.info("👋 Shutting down API...")


# Create FastAPI app
app = FastAPI(
    title="CE Email Summarizer API",
    description="AI-powered email thread summarization for customer experience teams",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "http://localhost:3000",  # Alternative frontend port
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint - API health check"""
    return {
        "service": "CE Email Summarizer API",
        "status": "running",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "threads": "/api/threads",
            "summarize": "/api/summarize",
            "docs": "/docs"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": summarizer is not None,
        "threads_loaded": threads_data is not None and len(threads_data.get("threads", [])) > 0,
        "thread_count": len(threads_data.get("threads", [])) if threads_data else 0,
        "service": "ce-email-summarizer"
    }


@app.get("/api/threads")
async def get_threads():
    """
    Get all email threads

    Returns:
        JSON object containing all email threads with metadata
    """
    if threads_data is None:
        raise HTTPException(
            status_code=500,
            detail="Threads data not loaded"
        )

    logger.info(f"📧 Fetching {len(threads_data.get('threads', []))} threads")
    return threads_data


@app.post("/api/summarize", response_model=SummarizeResponse)
async def summarize_thread(request: SummarizeRequest):
    """
    Summarize an email thread using NLP

    Args:
        request: SummarizeRequest containing the thread to summarize

    Returns:
        SummarizeResponse with generated summary

    Raises:
        HTTPException: If summarization fails
    """
    try:
        logger.info(f"📧 Summarizing thread: {request.thread.thread_id}")

        # Validate input
        if not request.thread.messages:
            raise HTTPException(
                status_code=400,
                detail="Thread must contain at least one message"
            )

        # Generate summary
        summary = summarizer.summarize_thread(request.thread)

        logger.info(f"✓ Summary generated for thread: {request.thread.thread_id}")

        return SummarizeResponse(
            success=True,
            summary=summary,
            message="Summary generated successfully"
        )

    except Exception as e:
        logger.error(f"❌ Error summarizing thread: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate summary: {str(e)}"
        )


@app.post("/api/summarize/{thread_id}", response_model=SummarizeResponse)
async def summarize_thread_by_id(thread_id: str, thread: Thread):
    """
    Summarize a specific thread by ID

    Args:
        thread_id: Thread ID to summarize
        thread: Thread data

    Returns:
        SummarizeResponse with generated summary
    """
    # Ensure thread_id matches
    if thread.thread_id != thread_id:
        raise HTTPException(
            status_code=400,
            detail="Thread ID in path does not match thread ID in body"
        )

    return await summarize_thread(SummarizeRequest(thread=thread))


@app.get("/api/models/info")
async def model_info():
    """Get information about loaded NLP models"""
    return {
        "summarization_model": "facebook/bart-large-cnn",
        "model_type": "Transformer (BART)",
        "provider": "Hugging Face",
        "loaded": summarizer is not None,
        "capabilities": [
            "Abstractive summarization",
            "Sentiment analysis (rule-based)",
            "Action item extraction",
            "Priority classification",
            "Issue categorization"
        ]
    }


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error",
            "detail": str(exc)
        }
    )


if __name__ == "__main__":
    import uvicorn

    logger.info("Starting development server...")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
