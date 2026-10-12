"""
Project management endpoints with GitHub integration
"""
from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from typing import List
from backend.database.base import get_db
from backend.models import schemas
from backend.models.database_models import User, Project, Build
from backend.utils.auth import get_current_active_user
from backend.services.github_service import GitHubService, TEST_REPOSITORIES

router = APIRouter(prefix="/api/v1/projects", tags=["projects"])


@router.post("/github", response_model=schemas.Project, status_code=status.HTTP_201_CREATED)
def create_github_project(
    github_data: dict = Body(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a project from a GitHub repository"""
    import logging
    logger = logging.getLogger(__name__)
    
    try:
        repo_url = github_data.get("repository_url")
        if not repo_url:
            raise HTTPException(status_code=400, detail="repository_url is required")
        
        logger.info(f"Creating GitHub project from URL: {repo_url}")
        
        # Get repository info from GitHub
        github_service = GitHubService()
        logger.info("GitHub service initialized")
        
        repo_info = github_service.get_repository_info(repo_url)
        logger.info(f"Got repo info: {repo_info}")
        
        # Check if project already exists
        existing = db.query(Project).filter(
            Project.owner_id == current_user.id,
            Project.name == repo_info["name"]
        ).first()
        
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Project '{repo_info['name']}' already exists"
            )
        
        # Create project with GitHub info
        db_project = Project(
            name=repo_info["name"],
            description=f"GitHub: {repo_info['description'] or 'No description'} | Language: {repo_info['language'] or 'Unknown'} | ⭐ {repo_info['stars']} | 🍴 {repo_info['forks']}",
            repository_url=repo_url,
            owner_id=current_user.id
        )
        
        db.add(db_project)
        db.commit()
        db.refresh(db_project)
        
        logger.info(f"Project created successfully: {db_project.id}")
        return db_project
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to create GitHub project: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create GitHub project: {str(e)}"
        )


@router.get("/github/test-repos")
def get_test_repositories(current_user: User = Depends(get_current_active_user)):
    """Get list of test repositories for demo purposes"""
    return {
        "repositories": TEST_REPOSITORIES,
        "message": "These are demo repositories you can use to test the system with real GitHub code!"
    }


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
