"""Development server runner for Splay API."""
import uvicorn
from app.settings import settings

if __name__ == "__main__":
    print("=" * 50)
    print(" Splay API Server")
    print("=" * 50)
    print()
    print(f"Environment: {settings.environment}")
    print(f"Database: SQLite (no Docker needed!)")
    print()
    print("Starting server...")
    print(f"- API: http://{settings.api_host}:{settings.api_port}")
    print(f"- Docs: http://localhost:{settings.api_port}/docs")
    print()
    print("Press CTRL+C to stop")
    print("=" * 50)
    print()

    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True,
        log_level="info"
    )
