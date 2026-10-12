"""
Pipeline execution service - runs builds in isolated environments
"""
import subprocess
import os
import time
from datetime import datetime
from sqlalchemy.orm import Session
from backend.models.database_models import Build, BuildStatus, BuildMetrics
from backend.config import settings
from pathlib import Path
import random


def execute_pipeline(build_id: int, db: Session):
    """
    Execute a pipeline build
    This runs in a background task
    """
    # Get fresh session
    from backend.database.base import SessionLocal
    db = SessionLocal()
    
    try:
        build = db.query(Build).filter(Build.id == build_id).first()
        if not build:
            return
        
        # Update status to running
        build.status = BuildStatus.RUNNING
        build.started_at = datetime.now()
        db.commit()
        
        # Create workspace for this build
        workspace = Path(settings.WORKSPACE_PATH) / f"build_{build_id}"
        workspace.mkdir(parents=True, exist_ok=True)
        
        logs = []
        logs.append(f"=== Build #{build_id} Started at {build.started_at} ===\n")
        logs.append(f"Project ID: {build.project_id}\n")
        logs.append(f"Branch: {build.branch}\n")
        logs.append(f"Workspace: {workspace}\n\n")
        
        # Simulate build steps
        success = True
        
        # Step 1: Setup
        logs.append(">>> Step 1: Setting up environment\n")
        time.sleep(1)
        logs.append("Environment variables configured\n")
        logs.append("Dependencies resolved\n\n")
        
        # Step 2: Install dependencies
        logs.append(">>> Step 2: Installing dependencies\n")
        install_result = simulate_step("install", build.project_id)
        logs.append(install_result["output"])
        
        if not install_result["success"]:
            success = False
            logs.append("ERROR: Dependency installation failed\n")
        else:
            logs.append("Dependencies installed successfully\n\n")
        
        # Step 3: Run tests (if install succeeded)
        if success:
            logs.append(">>> Step 3: Running tests\n")
            test_result = simulate_step("test", build.project_id)
            logs.append(test_result["output"])
            
            if not test_result["success"]:
                success = False
                logs.append("ERROR: Tests failed\n")
            else:
                logs.append(f"All tests passed ({test_result.get('test_count', 0)} tests)\n\n")
        
        # Step 4: Build (if tests passed)
        if success:
            logs.append(">>> Step 4: Building application\n")
            build_result = simulate_step("build", build.project_id)
            logs.append(build_result["output"])
            
            if not build_result["success"]:
                success = False
                logs.append("ERROR: Build failed\n")
            else:
                logs.append("Build completed successfully\n\n")
        
        # Calculate duration
        completed_at = datetime.now()
        duration = int((completed_at - build.started_at).total_seconds())
        
        # Update build record
        build.status = BuildStatus.SUCCESS if success else BuildStatus.FAILED
        build.completed_at = completed_at
        build.duration = duration
        build.logs = "".join(logs)
        
        if not success:
            build.error_message = "Build failed during execution. Check logs for details."
        
        # Create build metrics
        metrics = BuildMetrics(
            build_id=build_id,
            lines_of_code=random.randint(1000, 8000),
            files_changed=random.randint(3, 25),
            lines_added=random.randint(50, 400),
            lines_deleted=random.randint(10, 150),
            test_coverage=random.uniform(65, 95),
            test_count=random.randint(20, 150),
            test_passed=random.randint(18, 150) if success else random.randint(10, 100),
            test_failed=0 if success else random.randint(1, 10),
            code_complexity=random.uniform(2.0, 8.0),
            cyclomatic_complexity=random.uniform(3.0, 12.0),
            dependency_count=random.randint(15, 60),
            dependency_changes=random.randint(0, 5),
            hour_of_day=build.started_at.hour,
            day_of_week=build.started_at.weekday(),
            commit_message_length=random.randint(30, 200),
            author=build.triggered_by
        )
        
        db.add(metrics)
        db.commit()
        
        # Update project statistics
        update_project_stats(db, build.project_id)
        
        print(f"✓ Build {build_id} completed with status: {build.status}")
        
    except Exception as e:
        print(f"Error executing pipeline {build_id}: {e}")
        build.status = BuildStatus.FAILED
        build.error_message = f"Internal error: {str(e)}"
        build.completed_at = datetime.now()
        db.commit()
    
    finally:
        db.close()


def simulate_step(step_type: str, project_id: int) -> dict:
    """
    Simulate a build step
    In a real implementation, this would execute actual commands
    """
    # Simulate some processing time
    time.sleep(random.uniform(1, 3))
    
    # Randomly fail some builds for demo purposes (10% failure rate)
    should_fail = random.random() < 0.1
    
    outputs = {
        "install": {
            "success": not should_fail,
            "output": f"Collecting packages...\nInstalled 23 packages successfully\n" if not should_fail else "ERROR: Package conflict detected\n",
        },
        "test": {
            "success": not should_fail,
            "output": f"Running test suite...\n{'Passed: 45/45' if not should_fail else 'Passed: 42/45 FAILED'}\n",
            "test_count": 45
        },
        "build": {
            "success": not should_fail,
            "output": f"Compiling source code...\nBuild {'succeeded' if not should_fail else 'FAILED'}\n",
        }
    }
    
    return outputs.get(step_type, {"success": True, "output": "Step completed\n"})


def update_project_stats(db: Session, project_id: int):
    """Update project statistics after a build"""
    from backend.models.database_models import Project
    from sqlalchemy import func
    
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        return
    
    # Count total builds
    total_builds = db.query(Build).filter(Build.project_id == project_id).count()
    
    # Count successful builds
    success_builds = db.query(Build).filter(
        Build.project_id == project_id,
        Build.status == BuildStatus.SUCCESS
    ).count()
    
    # Update project
    project.total_builds = total_builds
    project.success_rate = (success_builds / total_builds * 100) if total_builds > 0 else 0
    
    db.commit()
