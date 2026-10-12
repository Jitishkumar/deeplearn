"""
Initialize database with tables and sample data
"""
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from backend.database.base import engine, SessionLocal, Base
from backend.models.database_models import User, Project, Build, BuildMetrics, MLModel, AnomalyLog
from backend.utils.auth import get_password_hash
from backend.models.schemas import BuildStatus, PipelineLanguage
from datetime import datetime, timedelta
import random


def create_tables():
    """Create all database tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✓ Tables created successfully")


def create_sample_data():
    """Create sample data for demonstration"""
    db = SessionLocal()
    
    try:
        # Check if data already exists
        if db.query(User).first():
            print("Sample data already exists. Skipping...")
            return
        
        print("Creating sample data...")
        
        # Create demo user
        demo_user = User(
            email="demo@devops-pipeline.com",
            username="demo",
            full_name="Demo User",
            hashed_password=get_password_hash("demo123"),
            is_active=True
        )
        db.add(demo_user)
        db.commit()
        db.refresh(demo_user)
        print(f"✓ Created demo user: {demo_user.username}")
        
        # Create sample projects
        projects_data = [
            {
                "name": "python-web-app",
                "description": "Python Flask web application",
                "language": PipelineLanguage.PYTHON,
                "repository_url": "https://github.com/demo/python-web-app"
            },
            {
                "name": "nodejs-api",
                "description": "Node.js REST API service",
                "language": PipelineLanguage.NODEJS,
                "repository_url": "https://github.com/demo/nodejs-api"
            },
            {
                "name": "java-microservice",
                "description": "Spring Boot microservice",
                "language": PipelineLanguage.JAVA,
                "repository_url": "https://github.com/demo/java-microservice"
            }
        ]
        
        projects = []
        for proj_data in projects_data:
            project = Project(
                owner_id=demo_user.id,
                **proj_data
            )
            db.add(project)
            projects.append(project)
        
        db.commit()
        print(f"✓ Created {len(projects)} sample projects")
        
        # Create sample builds with varying statuses
        build_statuses = [BuildStatus.SUCCESS, BuildStatus.FAILED, BuildStatus.SUCCESS, 
                         BuildStatus.SUCCESS, BuildStatus.TIMEOUT, BuildStatus.SUCCESS]
        
        builds_created = 0
        for project in projects:
            for i in range(20):  # 20 builds per project
                created_time = datetime.now() - timedelta(days=random.randint(0, 30))
                status = random.choice(build_statuses)
                duration = random.randint(60, 600) if status == BuildStatus.SUCCESS else random.randint(30, 300)
                
                build = Build(
                    project_id=project.id,
                    status=status,
                    branch="main" if i % 3 == 0 else f"feature-{i}",
                    commit_hash=f"abc{i:04d}ef",
                    triggered_by="demo" if i % 2 == 0 else "webhook",
                    created_at=created_time,
                    started_at=created_time + timedelta(seconds=5),
                    completed_at=created_time + timedelta(seconds=duration) if status != BuildStatus.PENDING else None,
                    duration=duration if status != BuildStatus.PENDING else None,
                    error_message="Build failed: test_authentication failed" if status == BuildStatus.FAILED else None,
                    prediction_score=random.uniform(0.1, 0.9),
                    predicted_duration=duration + random.randint(-30, 30)
                )
                db.add(build)
                db.commit()
                db.refresh(build)
                
                # Add metrics for completed builds
                if status in [BuildStatus.SUCCESS, BuildStatus.FAILED]:
                    metrics = BuildMetrics(
                        build_id=build.id,
                        lines_of_code=random.randint(500, 5000),
                        files_changed=random.randint(1, 20),
                        lines_added=random.randint(10, 200),
                        lines_deleted=random.randint(0, 100),
                        test_coverage=random.uniform(60, 95),
                        test_count=random.randint(10, 100),
                        test_passed=random.randint(8, 95),
                        test_failed=random.randint(0, 5),
                        code_complexity=random.uniform(1.5, 8.0),
                        dependency_count=random.randint(10, 50),
                        hour_of_day=created_time.hour,
                        day_of_week=created_time.weekday(),
                        commit_message_length=random.randint(20, 150),
                        author="demo"
                    )
                    db.add(metrics)
                
                builds_created += 1
        
        db.commit()
        print(f"✓ Created {builds_created} sample builds with metrics")
        
        # Update project statistics
        for project in projects:
            total = db.query(Build).filter(Build.project_id == project.id).count()
            success = db.query(Build).filter(
                Build.project_id == project.id,
                Build.status == BuildStatus.SUCCESS
            ).count()
            
            project.total_builds = total
            project.success_rate = (success / total * 100) if total > 0 else 0
        
        db.commit()
        print("✓ Updated project statistics")
        
        print("\n" + "="*60)
        print("Sample data created successfully!")
        print("="*60)
        print("\nLogin Credentials:")
        print("  Username: demo")
        print("  Password: demo123")
        print("\nAPI Documentation: http://localhost:8000/docs")
        print("="*60)
        
    except Exception as e:
        print(f"Error creating sample data: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("Initializing database...")
    create_tables()
    create_sample_data()
    print("\n✓ Database initialization complete!")
