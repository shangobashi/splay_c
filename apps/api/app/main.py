"""FastAPI application entry point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.settings import settings

# Create FastAPI application
app = FastAPI(
    title="Splay API",
    description="Shop The Room - AI-powered furniture discovery platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.is_development else ["https://shoptheroom.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "environment": settings.environment,
        "version": "1.0.0",
    }


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Splay API - Shop The Room",
        "tagline": "Shazam for furniture - AI-powered room scanning",
        "version": "1.0.0 MVP",
        "docs": "/docs",
        "health": "/health",
        "features": {
            "auth": "✓ Register/Login (JWT)",
            "scans": "✓ Upload room photos",
            "matching": "✓ AI furniture detection",
            "products": "✓ Product catalog with 60+ items"
        }
    }


# Import and include routers
from app.routes import auth, scans

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(scans.router, prefix="/scans", tags=["Scans"])

# Mount static files for storage
app.mount("/storage", StaticFiles(directory=str(settings.storage_dir)), name="storage")
