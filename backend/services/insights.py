"""
AI-powered insights service
"""
from sqlalchemy.orm import Session
from backend.models.database_models import Build, BuildStatus, BuildMetrics
from backend.models.schemas import InsightsResponse, OptimizationRecommendation
from datetime import datetime, timedelta
from typing import List
import statistics


def generate_insights(db: Session, project_id: int) -> InsightsResponse:
    """Generate AI-powered insights and recommendations"""
    
    # Get recent builds (last 30 days)
    start_date = datetime.now() - timedelta(days=30)
    builds = db.query(Build).filter(
        Build.project_id == project_id,
        Build.created_at >= start_date
    ).all()
    
    if not builds:
        return InsightsResponse(
            recommendations=[],
            anomalies=["No recent builds to analyze"],
            trends={},
            health_score=0.0
        )
    
    # Generate recommendations
    recommendations = []
    
    # Performance recommendations
    perf_rec = analyze_performance(builds)
    if perf_rec:
        recommendations.extend(perf_rec)
    
    # Reliability recommendations
    rel_rec = analyze_reliability(builds)
    if rel_rec:
        recommendations.extend(rel_rec)
    
    # Cost optimization recommendations
    cost_rec = analyze_cost(builds)
    if cost_rec:
        recommendations.extend(cost_rec)
    
    # Detect anomalies
    anomalies = detect_anomalies(builds)
    
    # Calculate trends
    trends = calculate_trends(builds)
    
    # Calculate overall health score (0-100)
    health_score = calculate_health_score(builds)
    
    return InsightsResponse(
        recommendations=recommendations,
        anomalies=anomalies,
        trends=trends,
        health_score=health_score
    )


def analyze_performance(builds: List[Build]) -> List[OptimizationRecommendation]:
    """Analyze performance and suggest optimizations"""
    recommendations = []
    
    completed_builds = [b for b in builds if b.duration is not None]
    if not completed_builds:
        return recommendations
    
    avg_duration = sum(b.duration for b in completed_builds) / len(completed_builds)
    
    if avg_duration > 600:  # More than 10 minutes
        recommendations.append(OptimizationRecommendation(
            category="performance",
            title="Reduce Build Time",
            description="Average build time is over 10 minutes. Consider implementing dependency caching, parallel test execution, and incremental builds.",
            impact="high",
            effort="medium",
            estimated_improvement="30-50% faster builds"
        ))
    
    # Check if build times are increasing
    if len(completed_builds) >= 10:
        recent_avg = sum(b.duration for b in completed_builds[:5]) / 5
        older_avg = sum(b.duration for b in completed_builds[-5:]) / 5
        
        if recent_avg > older_avg * 1.3:  # 30% slower
            recommendations.append(OptimizationRecommendation(
                category="performance",
                title="Build Time Degradation",
                description="Build times have increased by 30% recently. Investigate new dependencies or test additions.",
                impact="medium",
                effort="low",
                estimated_improvement="Restore previous performance levels"
            ))
    
    return recommendations


def analyze_reliability(builds: List[Build]) -> List[OptimizationRecommendation]:
    """Analyze reliability and suggest improvements"""
    recommendations = []
    
    total = len(builds)
    failures = sum(1 for b in builds if b.status == BuildStatus.FAILED)
    success_rate = ((total - failures) / total * 100) if total > 0 else 0
    
    if success_rate < 70:
        recommendations.append(OptimizationRecommendation(
            category="reliability",
            title="Improve Build Stability",
            description=f"Success rate is {success_rate:.1f}%. Focus on fixing flaky tests, improving error handling, and adding pre-commit validation.",
            impact="high",
            effort="high",
            estimated_improvement="Increase success rate to 90%+"
        ))
    
    # Check for flaky tests (builds that fail and succeed alternately)
    if len(builds) >= 5:
        recent_statuses = [b.status for b in builds[:10]]
        alternating = sum(1 for i in range(len(recent_statuses)-1) 
                         if recent_statuses[i] != recent_statuses[i+1])
        
        if alternating >= 4:  # Many status changes
            recommendations.append(OptimizationRecommendation(
                category="reliability",
                title="Flaky Tests Detected",
                description="Build status alternates frequently, suggesting flaky tests. Identify and fix non-deterministic tests.",
                impact="high",
                effort="medium",
                estimated_improvement="More consistent builds"
            ))
    
    return recommendations


def analyze_cost(builds: List[Build]) -> List[OptimizationRecommendation]:
    """Analyze cost and suggest optimizations"""
    recommendations = []
    
    completed_builds = [b for b in builds if b.duration is not None]
    if not completed_builds:
        return recommendations
    
    total_time = sum(b.duration for b in completed_builds)
    total_hours = total_time / 3600
    
    # Estimate compute cost (assuming $0.10 per compute hour)
    estimated_cost = total_hours * 0.10
    
    if estimated_cost > 10:  # More than $10/month
        recommendations.append(OptimizationRecommendation(
            category="cost",
            title="Optimize Build Frequency",
            description=f"Estimated monthly compute cost: ${estimated_cost:.2f}. Consider using build triggers wisely and caching more aggressively.",
            impact="medium",
            effort="low",
            estimated_improvement=f"Save ${estimated_cost * 0.3:.2f}/month"
        ))
    
    # Check for failed builds (wasted compute)
    failed_builds = [b for b in completed_builds if b.status == BuildStatus.FAILED]
    wasted_time = sum(b.duration for b in failed_builds)
    wasted_percentage = (wasted_time / total_time * 100) if total_time > 0 else 0
    
    if wasted_percentage > 20:
        recommendations.append(OptimizationRecommendation(
            category="cost",
            title="Reduce Failed Build Waste",
            description=f"{wasted_percentage:.1f}% of compute time is spent on failed builds. Add pre-build validation to catch issues earlier.",
            impact="medium",
            effort="medium",
            estimated_improvement="Reduce wasted compute by 50%"
        ))
    
    return recommendations


def detect_anomalies(builds: List[Build]) -> List[str]:
    """Detect anomalous patterns in builds"""
    anomalies = []
    
    completed_builds = [b for b in builds if b.duration is not None]
    if len(completed_builds) < 5:
        return anomalies
    
    # Detect duration spikes
    durations = [b.duration for b in completed_builds]
    avg_duration = statistics.mean(durations)
    stdev = statistics.stdev(durations) if len(durations) > 1 else 0
    
    for build in completed_builds[:5]:  # Check recent builds
        if stdev > 0 and build.duration > avg_duration + (2 * stdev):
            anomalies.append(
                f"Build #{build.id} took {build.duration}s (significantly longer than average {avg_duration:.0f}s)"
            )
    
    # Detect unusual failure times
    hour_failures = {}
    for build in builds:
        if build.status == BuildStatus.FAILED:
            hour = build.created_at.hour
            hour_failures[hour] = hour_failures.get(hour, 0) + 1
    
    if hour_failures:
        worst_hour = max(hour_failures, key=hour_failures.get)
        if hour_failures[worst_hour] > len(builds) * 0.15:  # >15% of all builds
            anomalies.append(
                f"High failure rate during hour {worst_hour}:00 - possible infrastructure issue"
            )
    
    return anomalies


def calculate_trends(builds: List[Build]) -> dict:
    """Calculate trend metrics"""
    if not builds:
        return {}
    
    completed = [b for b in builds if b.duration is not None]
    
    # Split into recent and historical
    mid_point = len(builds) // 2
    recent = builds[:mid_point] if mid_point > 0 else builds
    historical = builds[mid_point:] if mid_point > 0 else builds
    
    recent_success_rate = (sum(1 for b in recent if b.status == BuildStatus.SUCCESS) / len(recent) * 100) if recent else 0
    historical_success_rate = (sum(1 for b in historical if b.status == BuildStatus.SUCCESS) / len(historical) * 100) if historical else 0
    
    recent_completed = [b for b in recent if b.duration is not None]
    historical_completed = [b for b in historical if b.duration is not None]
    
    recent_avg_duration = (sum(b.duration for b in recent_completed) / len(recent_completed)) if recent_completed else 0
    historical_avg_duration = (sum(b.duration for b in historical_completed) / len(historical_completed)) if historical_completed else 0
    
    return {
        "success_rate_trend": "improving" if recent_success_rate > historical_success_rate else "declining",
        "success_rate_change": round(recent_success_rate - historical_success_rate, 2),
        "duration_trend": "improving" if recent_avg_duration < historical_avg_duration else "declining",
        "duration_change_seconds": round(recent_avg_duration - historical_avg_duration, 2),
        "build_frequency_per_day": len(builds) / 30  # Last 30 days
    }


def calculate_health_score(builds: List[Build]) -> float:
    """Calculate overall pipeline health score (0-100)"""
    if not builds:
        return 0.0
    
    total = len(builds)
    success = sum(1 for b in builds if b.status == BuildStatus.SUCCESS)
    success_rate = (success / total * 100) if total > 0 else 0
    
    # Base score is success rate
    score = success_rate * 0.7  # 70% weight
    
    # Factor in build times
    completed = [b for b in builds if b.duration is not None]
    if completed:
        avg_duration = sum(b.duration for b in completed) / len(completed)
        # Good: <300s, OK: <600s, Bad: >600s
        if avg_duration < 300:
            score += 20
        elif avg_duration < 600:
            score += 10
        # else: no additional points
    
    # Factor in consistency (lower variance is better)
    if len(completed) > 3:
        durations = [b.duration for b in completed]
        stdev = statistics.stdev(durations)
        avg_duration = statistics.mean(durations)
        coefficient_of_variation = (stdev / avg_duration) if avg_duration > 0 else 1
        
        if coefficient_of_variation < 0.3:
            score += 10
        elif coefficient_of_variation < 0.5:
            score += 5
    
    return min(round(score, 2), 100.0)
