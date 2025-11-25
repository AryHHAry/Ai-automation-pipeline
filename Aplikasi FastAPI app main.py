from fastapi import FastAPI, BackgroundTasks, Depends
from app.models.llm_model import get_model, predict
from app.schemas.requests import PredictionRequest, PredictionResponse
from app.utils.logging_setup import get_logger
import asyncio

app = FastAPI(
    title="AI Automation Pipeline",
    description="LLM Deployment with FastAPI & Docker",
    version="1.0.0"
)

logger = get_logger(__name__)

@app.on_event("startup")
async def startup_event():
    """Initialize model on startup for efficiency[citation:9]"""
    logger.info("Loading LLM model...")
    await get_model()
    logger.info("Model loaded successfully")

@app.post("/predict", response_model=PredictionResponse)
async def predict_endpoint(
    request: PredictionRequest,
    background_tasks: BackgroundTasks
):
    """
    Endpoint for LLM predictions with async processing[citation:8]
    """
    logger.info(f"Received prediction request: {request.prompt[:100]}...")
    
    try:
        # Async prediction
        result = await predict(request)
        
        # Background task for logging
        background_tasks.add_task(
            logger.info, 
            f"Prediction completed for request: {request.prompt[:100]}..."
        )
        
        return PredictionResponse(
            generated_text=result,
            status="success"
        )
    except Exception as e:
        logger.error(f"Prediction failed: {str(e)}")
        return PredictionResponse(
            generated_text="",
            status="error",
            error_message=str(e)
        )

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {"status": "healthy"}