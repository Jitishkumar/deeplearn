"""
AI Prediction endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database.base import get_db
from backend.models import schemas
from backend.models.database_models import User, Project, Build, BuildStatus
from backend.utils.auth import get_current_active_user
from ai_engine.predictor import get_predictor
from datetime import datetime

router = APIRouter(prefix="/api/v1/predict", tags=["predictions"])


@router.post("/failure", response_model=schemas.FailurePredictionResponse)
def predict_failure(
    request: schemas.FailurePredictionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Predict if a build will fail"""
    # Verify project access
    project = db.query(Project).filter(
        Project.id == request.project_id,
        Project.owner_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Get recent build history for this project
    recent_builds = db.query(Build).filter(
        Build.project_id == request.project_id,
        Build.status.in_([BuildStatus.SUCCESS, BuildStatus.FAILED])
    ).order_by(Build.created_at.desc()).limit(10).all()
    
    # Count recent failures
    recent_failures = sum(1 for b in recent_builds if b.status == BuildStatus.FAILED)
    
    # Calculate average test coverage from recent builds
    avg_coverage = 80.0
    if recent_builds:
        coverages = [b.metrics.test_coverage for b in recent_builds if b.metrics and b.metrics.test_coverage]
        if coverages:
            avg_coverage = sum(coverages) / len(coverages)
    
    # Get predictor and make prediction
    predictor = get_predictor()
    
    prediction = predictor.predict_failure(
        files_changed=request.files_changed,
        lines_changed=request.lines_changed,
        test_coverage=avg_coverage,
        hour_of_day=request.time_of_day or datetime.now().hour,
        previous_failures=recent_failures
    )
    
    return schemas.FailurePredictionResponse(**prediction)


@router.post("/duration", response_model=schemas.DurationPredictionResponse)
def predict_duration(
    request: schemas.DurationPredictionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Predict build duration"""
    # Verify project access
    project = db.query(Project).filter(
        Project.id == request.project_id,
        Project.owner_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Get predictor and make prediction
    predictor = get_predictor()
    
    prediction = predictor.predict_duration(
        files_changed=request.files_changed,
        lines_changed=request.lines_changed,
        test_count=request.test_count or 50,
        language=request.language.value
    )
    
    return schemas.DurationPredictionResponse(**prediction)


@router.get("/insights/{project_id}", response_model=schemas.InsightsResponse)
def get_insights(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get AI-powered insights and recommendations"""
    from backend.services.insights import generate_insights
    
    # Verify project access
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.owner_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    insights = generate_insights(db, project_id)
    return insights
