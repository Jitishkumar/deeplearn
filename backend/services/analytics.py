"""
Analytics service for generating insights and trends
"""
from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.models.database_models import Build, Project, BuildStatus, BuildMetrics
from backend.models.schemas import (
    ProjectAnalytics, AnalyticsSummary, TrendData
)
from datetime import datetime, timedelta
from typing import List


def calculate_project_analytics(db: Session, project_id: int, days: int = 30) -> ProjectAnalytics:
    """Calculate comprehensive analytics for a project"""
    
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise ValueError("Project not found")
    
    # Get builds from the last N days
    start_date = datetime.now() - timedelta(days=days)
    builds = db.query(Build).filter(
        Build.project_id == project_id,
        Build.created_at >= start_date
    ).all()
    
    # Calculate summary statistics
    total_builds = len(builds)
    success_count = sum(1 for b in builds if b.status == BuildStatus.SUCCESS)
    failure_count = sum(1 for b in builds if b.status == BuildStatus.FAILED)
    
    completed_builds = [b for b in builds if b.duration is not None]
    avg_duration = sum(b.duration for b in completed_builds) / len(completed_builds) if completed_builds else 0
    total_duration = sum(b.duration for b in completed_builds)
    
    success_rate = (success_count / total_builds * 100) if total_builds > 0 else 0
    
    # Calculate daily trends
    trends = []
    for i in range(min(days, 14)):  # Last 14 days
        day = datetime.now() - timedelta(days=i)
        day_start = day.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_start + timedelta(days=1)
        
        day_builds = [b for b in builds if day_start <= b.created_at < day_end]
        day_success = sum(1 for b in day_builds if b.status == BuildStatus.SUCCESS)
        day_completed = [b for b in day_builds if b.duration is not None]
        day_avg_duration = sum(b.duration for b in day_completed) / len(day_completed) if day_completed else 0
        
        trends.append(TrendData(
            date=day_start.strftime("%Y-%m-%d"),
            builds=len(day_builds),
            success_rate=(day_success / len(day_builds) * 100) if day_builds else 0,
            avg_duration=round(day_avg_duration, 2)
        ))
    
    trends.reverse()  # Oldest to newest
    
    # Get top failure reasons
    failed_builds = [b for b in builds if b.status == BuildStatus.FAILED and b.error_message]
    top_failures = list(set(b.error_message for b in failed_builds[:10]))
    
    # Find busiest hours
    hour_counts = {}
    for build in builds:
        hour = build.created_at.hour
        hour_counts[hour] = hour_counts.get(hour, 0) + 1
    
    busiest_hours = sorted(hour_counts.keys(), key=lambda h: hour_counts[h], reverse=True)[:5]
    
    # Generate recommendations
    recommendations = generate_recommendations(
        success_rate=success_rate,
        avg_duration=avg_duration,
        total_builds=total_builds,
        builds=builds
    )
    
    summary = AnalyticsSummary(
        total_builds=total_builds,
        success_count=success_count,
        failure_count=failure_count,
        success_rate=round(success_rate, 2),
        avg_duration=round(avg_duration, 2),
        total_duration=total_duration,
        trends=trends
    )
    
    return ProjectAnalytics(
        project_id=project_id,
        project_name=project.name,
        summary=summary,
        top_failures=top_failures,
        busiest_hours=busiest_hours,
        recommendations=recommendations
    )


def generate_recommendations(
    success_rate: float,
    avg_duration: float,
    total_builds: int,
    builds: List[Build]
) -> List[str]:
    """Generate actionable recommendations based on metrics"""
    recommendations = []
    
    if success_rate < 70:
        recommendations.append("🔴 Low success rate detected. Review recent failures and improve test coverage.")
    elif success_rate < 85:
        recommendations.append("🟡 Success rate could be improved. Consider adding more automated tests.")
    else:
        recommendations.append("✅ Great success rate! Keep up the good work.")
    
    if avg_duration > 600:  # 10 minutes
        recommendations.append("⏱️ Build times are high. Consider caching dependencies and parallelizing tests.")
    elif avg_duration > 300:  # 5 minutes
        recommendations.append("⏱️ Build times are moderate. Look for opportunities to optimize.")
    
    # Check for patterns in failures
    recent_builds = sorted(builds, key=lambda b: b.created_at, reverse=True)[:10]
    recent_failures = sum(1 for b in recent_builds if b.status == BuildStatus.FAILED)
    
    if recent_failures >= 5:
        recommendations.append("⚠️ Multiple recent failures detected. Critical attention needed.")
    
    # Check for weekend builds
    weekend_builds = sum(1 for b in builds if b.created_at.weekday() >= 5)
    if weekend_builds > total_builds * 0.2:
        recommendations.append("📅 High weekend activity. Consider setting up automated scheduled builds.")
    
    if not recommendations:
        recommendations.append("✨ Pipeline is healthy. No immediate actions needed.")
    
    return recommendations
