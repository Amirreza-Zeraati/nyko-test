"""FastAPI main application entry point."""

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.routes import registration, questionnaire, evaluation
from app.services.session_manager import SessionManager

# Initialize session manager
session_manager = SessionManager()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    # Startup
    await session_manager.initialize()
    yield
    # Shutdown
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

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="app/templates")

# Include routers
app.include_router(registration.router, prefix="/api", tags=["registration"])
app.include_router(questionnaire.router, prefix="/api", tags=["questionnaire"])
app.include_router(evaluation.router, prefix="/api", tags=["evaluation"])

@app.get("/")
async def root(request: Request):
    """Root endpoint - welcome page."""
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": "1.0.0"}
