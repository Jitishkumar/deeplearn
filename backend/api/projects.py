"""
Project management endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from backend.database.base import get_db
from backend.models import schemas
from backend.models.database_models import User, Project, Build
from backend.utils.auth import get_current_active_user

router = APIRouter(prefix="/api/v1/projects", tags=["projects"])


@router.post("", response_model=schemas.Project, status_code=status.HTTP_201_CREATED)
def create_project(
    project: schemas.ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new project"""
    # Check if project name already exists for this user
    existing = db.query(Project).filter(
        Project.owner_id == current_user.id,
        Project.name == project.name
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Project with this name already exists"
        )
    
    db_project = Project(
        **project.dict(),
        owner_id=current_user.id
    )
    
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    
    return db_project


@router.get("", response_model=List[schemas.Project])
def list_projects(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """List all projects for current user"""
    projects = db.query(Project).filter(
        Project.owner_id == current_user.id
    ).offset(skip).limit(limit).all()
    
    return projects


@router.get("/{project_id}", response_model=schemas.Project)
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific project"""
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.owner_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    return project


@router.put("/{project_id}", response_model=schemas.Project)
def update_project(
    project_id: int,
    project_update: schemas.ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update a project"""
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.owner_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    for key, value in project_update.dict().items():
        setattr(project, key, value)
    
    db.commit()
    db.refresh(project)
    
    return project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete a project"""
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.owner_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    db.delete(project)
    db.commit()
    
    return None


@router.get("/{project_id}/analytics", response_model=schemas.ProjectAnalytics)
def get_project_analytics(
    project_id: int,
    days: int = 30,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get analytics for a project"""
    from backend.services.analytics import calculate_project_analytics
    
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.owner_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    analytics = calculate_project_analytics(db, project_id, days)
    return analytics
