from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import asyncio
import logging
from datetime import datetime
from dotenv import load_dotenv
from backend.agents.workflow import EbookWorkflow

load_dotenv(dotenv_path="backend/.env")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('backend/ebook_generator.log'),
        logging.StreamHandler()
    ]
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerateRequest(BaseModel):
    topic: str

# Mount static directory for serving generated PDFs
app.mount("/static", StaticFiles(directory="backend/static"), name="static")

@app.post("/api/generate")
async def generate_ebook(request: GenerateRequest):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="API Key not configured on server.")
    
    logger = logging.getLogger(__name__)
    logger.info(f"Starting ebook generation for topic: {request.topic}")
    
    workflow = EbookWorkflow(api_key)
    try:
        result = await workflow.run(request.topic)
        logger.info(f"Ebook generation completed successfully: {result.get('filename')}")
        return result
    except Exception as e:
        logger.error(f"Ebook generation failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/logs")
async def get_logs(lines: int = 100):
    """Get the last N lines from the log file."""
    log_file = "backend/ebook_generator.log"
    
    if not os.path.exists(log_file):
        return {"logs": [], "message": "No logs available yet"}
    
    try:
        with open(log_file, 'r') as f:
            all_lines = f.readlines()
            recent_logs = all_lines[-lines:] if len(all_lines) > lines else all_lines
            return {
                "logs": [line.strip() for line in recent_logs],
                "total_lines": len(all_lines),
                "showing": len(recent_logs)
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read logs: {str(e)}")

@app.get("/")
async def read_root():
    return {"message": "AI Ebook Generator API. Frontend runs on port 3000."}
