"""
SQLAlchemy database models
"""
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, JSON, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.database.base import Base
from backend.models.schemas import BuildStatus, PipelineLanguage
import enum


class User(Base):
    """User model"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(200))
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    projects = relationship("Project", back_populates="owner", cascade="all, delete-orphan")


class Project(Base):
    """Project/Repository model"""
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    description = Column(Text)
    repository_url = Column(String(500))
    language = Column(SQLEnum(PipelineLanguage), default=PipelineLanguage.PYTHON)
    branch = Column(String(100), default="main")
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Computed fields
    total_builds = Column(Integer, default=0)
    success_rate = Column(Float, default=0.0)

    # Relationships
    owner = relationship("User", back_populates="projects")
    builds = relationship("Build", back_populates="project", cascade="all, delete-orphan")


class Build(Base):
    """Build/Pipeline execution model"""
    __tablename__ = "builds"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    status = Column(SQLEnum(BuildStatus), default=BuildStatus.PENDING, index=True)
    branch = Column(String(100), default="main")
    commit_hash = Column(String(40))
    triggered_by = Column(String(100), default="manual")
    
    # Timing
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    duration = Column(Integer)  # in seconds
    
    # Results
    error_message = Column(Text)
    logs = Column(Text)
    
    # AI Predictions
    prediction_score = Column(Float)  # failure probability
    predicted_duration = Column(Integer)
    
    # Configuration
    config = Column(JSON)
    
    # Relationships
    project = relationship("Project", back_populates="builds")
    metrics = relationship("BuildMetrics", back_populates="build", uselist=False, cascade="all, delete-orphan")


class BuildMetrics(Base):
    """Build metrics for ML training"""
    __tablename__ = "build_metrics"

    id = Column(Integer, primary_key=True, index=True)
    build_id = Column(Integer, ForeignKey("builds.id"), nullable=False, unique=True)
    
    # Code metrics
    lines_of_code = Column(Integer)
    files_changed = Column(Integer)
    lines_added = Column(Integer)
    lines_deleted = Column(Integer)
    
    # Quality metrics
    test_coverage = Column(Float)
    test_count = Column(Integer)
    test_passed = Column(Integer)
    test_failed = Column(Integer)
    
    # Complexity metrics
    code_complexity = Column(Float)
    cyclomatic_complexity = Column(Float)
    
    # Dependencies
    dependency_count = Column(Integer)
    dependency_changes = Column(Integer)
    
    # Time-based features
    hour_of_day = Column(Integer)  # 0-23
    day_of_week = Column(Integer)  # 0-6
    
    # Other
    commit_message_length = Column(Integer)
    author = Column(String(100))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    build = relationship("Build", back_populates="metrics")


class MLModel(Base):
    """Track ML model versions and performance"""
    __tablename__ = "ml_models"

    id = Column(Integer, primary_key=True, index=True)
    model_type = Column(String(50), nullable=False)  # failure_prediction, duration_prediction
    version = Column(String(20), nullable=False)
    file_path = Column(String(500))
    
    # Performance metrics
    accuracy = Column(Float)
    precision_score = Column(Float)
    recall = Column(Float)
    f1_score = Column(Float)
    mae = Column(Float)  # Mean Absolute Error for duration prediction
    
    # Training info
    training_samples = Column(Integer)
    training_duration = Column(Integer)  # seconds
    features_used = Column(JSON)
    hyperparameters = Column(JSON)
    
    is_active = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class AnomalyLog(Base):
    """Log anomalies detected by the system"""
    __tablename__ = "anomaly_logs"

    id = Column(Integer, primary_key=True, index=True)
    build_id = Column(Integer, ForeignKey("builds.id"))
    anomaly_type = Column(String(100))  # duration_spike, unexpected_failure, etc.
    severity = Column(String(20))  # low, medium, high, critical
    description = Column(Text)
    detected_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    resolved = Column(Boolean, default=False)
    resolution_notes = Column(Text)
