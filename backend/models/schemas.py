"""
Pydantic schemas for API request/response validation
"""
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class BuildStatus(str, Enum):
    """Build status enumeration"""
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"
    TIMEOUT = "timeout"


class PipelineLanguage(str, Enum):
    """Supported programming languages"""
    PYTHON = "python"
    NODEJS = "nodejs"
    JAVA = "java"
    GO = "go"
    RUBY = "ruby"
    PHP = "php"
    OTHER = "other"


# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class User(UserBase):
    id: int
    is_active: bool = True
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# Project Schemas
class ProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    repository_url: Optional[str] = None
    language: PipelineLanguage = PipelineLanguage.PYTHON
    branch: str = "main"


class ProjectCreate(ProjectBase):
    pass


class Project(ProjectBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    total_builds: int = 0
    success_rate: float = 0.0

    class Config:
        from_attributes = True


# Pipeline Configuration Schemas
class BuildStep(BaseModel):
    name: str
    command: str
    timeout: Optional[int] = 300  # seconds
    continue_on_error: bool = False


class PipelineConfig(BaseModel):
    build_steps: List[BuildStep]
    environment_variables: Optional[Dict[str, str]] = {}
    docker_image: Optional[str] = None
    requirements_file: Optional[str] = "requirements.txt"


# Build Schemas
class BuildCreate(BaseModel):
    project_id: int
    branch: str = "main"
    commit_hash: Optional[str] = None
    triggered_by: str = "manual"
    config: Optional[PipelineConfig] = None


class BuildUpdate(BaseModel):
    status: Optional[BuildStatus] = None
    error_message: Optional[str] = None
    duration: Optional[int] = None


class Build(BaseModel):
    id: int
    project_id: int
    status: BuildStatus
    branch: str
    commit_hash: Optional[str] = None
    triggered_by: str
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    duration: Optional[int] = None  # seconds
    error_message: Optional[str] = None
    prediction_score: Optional[float] = None
    created_at: datetime

    class Config:
        from_attributes = True


class BuildDetail(Build):
    logs: Optional[str] = None
    metrics: Optional[Dict[str, Any]] = None
    steps: Optional[List[Dict[str, Any]]] = None


# Build Metrics Schemas
class BuildMetrics(BaseModel):
    build_id: int
    lines_of_code: Optional[int] = None
    files_changed: Optional[int] = None
    test_coverage: Optional[float] = None
    code_complexity: Optional[float] = None
    dependency_count: Optional[int] = None


# Prediction Schemas
class FailurePredictionRequest(BaseModel):
    project_id: int
    branch: str = "main"
    files_changed: int
    lines_changed: int
    commit_message: Optional[str] = None
    author: Optional[str] = None
    time_of_day: Optional[int] = None  # hour of day (0-23)


class FailurePredictionResponse(BaseModel):
    will_fail: bool
    failure_probability: float
    confidence: float
    risk_level: str  # low, medium, high
    recommendation: str
    factors: Dict[str, Any]


class DurationPredictionRequest(BaseModel):
    project_id: int
    language: PipelineLanguage
    files_changed: int
    lines_changed: int
    test_count: Optional[int] = None


class DurationPredictionResponse(BaseModel):
    estimated_duration: int  # seconds
    confidence: float
    range_min: int
    range_max: int
    factors: Dict[str, Any]


# Analytics Schemas
class TrendData(BaseModel):
    date: str
    builds: int
    success_rate: float
    avg_duration: float


class AnalyticsSummary(BaseModel):
    total_builds: int
    success_count: int
    failure_count: int
    success_rate: float
    avg_duration: float
    total_duration: int
    trends: List[TrendData]


class ProjectAnalytics(BaseModel):
    project_id: int
    project_name: str
    summary: AnalyticsSummary
    top_failures: List[str]
    busiest_hours: List[int]
    recommendations: List[str]


# Insights Schemas
class OptimizationRecommendation(BaseModel):
    category: str  # performance, cost, reliability
    title: str
    description: str
    impact: str  # low, medium, high
    effort: str  # low, medium, high
    estimated_improvement: str


class InsightsResponse(BaseModel):
    recommendations: List[OptimizationRecommendation]
    anomalies: List[str]
    trends: Dict[str, Any]
    health_score: float


# Response Models
class MessageResponse(BaseModel):
    message: str
    success: bool = True


class ErrorResponse(BaseModel):
    detail: str
    error_code: Optional[str] = None


# Dashboard Summary
class DashboardSummary(BaseModel):
    total_projects: int
    total_builds_today: int
    active_builds: int
    success_rate_today: float
    avg_build_time: float
    recent_builds: List[Build]
    system_health: str  # healthy, degraded, down
