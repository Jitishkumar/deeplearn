"""
Pipeline/Build management endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from backend.database.base import get_db
from backend.models import schemas
from backend.models.database_models import User, Project, Build, BuildStatus
from backend.utils.auth import get_current_active_user
from backend.services.pipeline_executor import execute_pipeline
from datetime import datetime

router = APIRouter(prefix="/api/v1/pipelines", tags=["pipelines"])


@router.post("/trigger", response_model=schemas.Build, status_code=status.HTTP_201_CREATED)
def trigger_pipeline(
    build_request: schemas.BuildCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Trigger a new pipeline build"""
    # Verify project exists and user has access
    project = db.query(Project).filter(
        Project.id == build_request.project_id,
        Project.owner_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Create build record
    build = Build(
        project_id=project.id,
        status=BuildStatus.PENDING,
        branch=build_request.branch,
        commit_hash=build_request.commit_hash,
        triggered_by=build_request.triggered_by or current_user.username,
        config=build_request.config.dict() if build_request.config else None
    )
    
    db.add(build)
    db.commit()
    db.refresh(build)
    
    # Execute pipeline in background
    background_tasks.add_task(execute_pipeline, build.id, db)
    
    return build


@router.get("", response_model=List[schemas.Build])
def list_pipelines(
    project_id: Optional[int] = None,
    status: Optional[BuildStatus] = None,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """List pipeline builds"""
    query = db.query(Build).join(Project).filter(Project.owner_id == current_user.id)
    
    if project_id:
        query = query.filter(Build.project_id == project_id)
    
    if status:
        query = query.filter(Build.status == status)
    
    builds = query.order_by(Build.created_at.desc()).offset(skip).limit(limit).all()
    
    return builds


@router.get("/{build_id}", response_model=schemas.BuildDetail)
def get_pipeline(
    build_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get pipeline build details"""
    build = db.query(Build).join(Project).filter(
        Build.id == build_id,
        Project.owner_id == current_user.id
    ).first()
    
    if not build:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Build not found"
        )
    
    # Format metrics if available
    metrics_dict = None
    if build.metrics:
        metrics_dict = {
            "lines_of_code": build.metrics.lines_of_code,
            "files_changed": build.metrics.files_changed,
            "test_coverage": build.metrics.test_coverage,
            "test_passed": build.metrics.test_passed,
            "test_failed": build.metrics.test_failed
        }
    
    return schemas.BuildDetail(
        **build.__dict__,
        metrics=metrics_dict
    )


@router.delete("/{build_id}/cancel", response_model=schemas.MessageResponse)
def cancel_pipeline(
    build_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Cancel a running pipeline"""
    build = db.query(Build).join(Project).filter(
        Build.id == build_id,
        Project.owner_id == current_user.id
    ).first()
    
    if not build:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Build not found"
        )
    
    if build.status not in [BuildStatus.PENDING, BuildStatus.RUNNING]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can only cancel pending or running builds"
        )
    
    build.status = BuildStatus.CANCELLED
    build.completed_at = datetime.now()
    
    db.commit()
    
    return schemas.MessageResponse(message="Build cancelled successfully")


@router.get("/{build_id}/logs")
def get_pipeline_logs(
    build_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get pipeline logs"""
    build = db.query(Build).join(Project).filter(
        Build.id == build_id,
        Project.owner_id == current_user.id
    ).first()
    
    if not build:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Build not found"
        )
    
    return {
        "build_id": build.id,
        "status": build.status,
        "logs": build.logs or "No logs available yet"
    }
