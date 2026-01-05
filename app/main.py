"""FastAPI main application entry point."""

import logging
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from app.routes import registration, questionnaire, evaluation
from app.services.session_manager import SessionManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize session manager
session_manager = SessionManager()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    # Startup
    logger.info("Starting ADHD Screening Expert System")
    await session_manager.initialize()
    logger.info("Session manager initialized")
    yield
    # Shutdown
    logger.info("Shutting down application")
    await session_manager.cleanup()

# Initialize FastAPI app
app = FastAPI(
    title="ADHD Screening Expert System",
    description="Clinical decision-support system for ADHD differential diagnosis",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal server error: {str(exc)}"}
    )

# Templates
templates = Jinja2Templates(directory="app/templates")

# Include API routers
logger.info("Loading API routes")
app.include_router(registration.router, prefix="/api", tags=["registration"])
app.include_router(questionnaire.router, prefix="/api", tags=["questionnaire"])
app.include_router(evaluation.router, prefix="/api", tags=["evaluation"])
logger.info("API routes loaded successfully")

# Frontend page routes (HTML templates)
@app.get("/")
async def root(request: Request):
    """Root endpoint - welcome page."""
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

@app.get("/registration")
async def registration_page(request: Request):
    """Registration form page."""
    return templates.TemplateResponse(
        "registration.html",
        {"request": request}
    )

@app.get("/questionnaire")
async def questionnaire_page(request: Request):
    """Questionnaire page."""
    return templates.TemplateResponse(
        "questionnaire.html",
        {"request": request}
    )

@app.get("/results")
async def results_page(request: Request):
    """Results page."""
    return templates.TemplateResponse(
        "result.html",
        {"request": request}
    )

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": "1.0.0"}

# Mount static files at the end
app.mount("/static", StaticFiles(directory="static"), name="static")

logger.info("Application startup complete")
