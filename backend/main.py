"""
Main FastAPI application
"""
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from backend.config import settings
from backend.database.base import engine, Base
from backend.api import auth, projects, pipelines, predictions, webhooks
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-Powered DevOps Pipeline System with Build Optimization",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "error_code": str(exc.status_code)}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error_code": "500"}
    )


# Health check endpoint
@app.get("/")
def root():
    return {
        "message": "AI-Powered DevOps Pipeline API",
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": "2024-01-01T00:00:00Z",
        "version": settings.APP_VERSION
    }


@app.get("/api/v1/dashboard")
async def get_dashboard():
    """Get dashboard summary"""
    from backend.database.base import SessionLocal
    from backend.models.database_models import Project, Build, BuildStatus
    from datetime import datetime, timedelta
    
    db = SessionLocal()
    try:
        # Get statistics
        total_projects = db.query(Project).count()
        
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        total_builds_today = db.query(Build).filter(Build.created_at >= today_start).count()
        
        active_builds = db.query(Build).filter(
            Build.status.in_([BuildStatus.PENDING, BuildStatus.RUNNING])
        ).count()
        
        # Success rate today
        success_today = db.query(Build).filter(
            Build.created_at >= today_start,
            Build.status == BuildStatus.SUCCESS
        ).count()
        success_rate_today = (success_today / total_builds_today * 100) if total_builds_today > 0 else 0
        
        # Average build time (last 24 hours)
        recent_builds = db.query(Build).filter(
            Build.created_at >= datetime.now() - timedelta(hours=24),
            Build.duration.isnot(None)
        ).all()
        avg_build_time = sum(b.duration for b in recent_builds) / len(recent_builds) if recent_builds else 0
        
        # Recent builds
        recent = db.query(Build).order_by(Build.created_at.desc()).limit(10).all()
        
        return {
            "total_projects": total_projects,
            "total_builds_today": total_builds_today,
            "active_builds": active_builds,
            "success_rate_today": round(success_rate_today, 2),
            "avg_build_time": round(avg_build_time, 2),
            "recent_builds": [
                {
                    "id": b.id,
                    "project_id": b.project_id,
                    "status": b.status.value,
                    "branch": b.branch,
                    "duration": b.duration,
                    "created_at": b.created_at.isoformat()
                }
                for b in recent
            ],
            "system_health": "healthy" if success_rate_today > 80 else "degraded" if success_rate_today > 50 else "down"
        }
    finally:
        db.close()


# Include routers
app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(pipelines.router)
app.include_router(predictions.router)
app.include_router(webhooks.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.main:app",
        host=settings.BACKEND_HOST,
        port=settings.BACKEND_PORT,
        reload=settings.DEBUG,
        reload_dirs=["backend"] if settings.DEBUG else None,
    )
