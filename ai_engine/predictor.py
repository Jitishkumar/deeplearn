"""
AI Predictor for build failure and duration prediction
"""
import os
import joblib
import numpy as np
from typing import Dict, Tuple, Optional
from pathlib import Path
from backend.config import settings


class BuildPredictor:
    """Predict build outcomes using ML models"""
    
    def __init__(self):
        self.model_path = Path(settings.ML_MODEL_PATH)
        self.failure_model = None
        self.duration_model = None
        self.failure_scaler = None
        self.duration_scaler = None
        
        self._load_models()
    
    def _load_models(self):
        """Load pre-trained models if they exist"""
        try:
            failure_model_file = self.model_path / "failure_prediction_model.pkl"
            if failure_model_file.exists():
                self.failure_model = joblib.load(failure_model_file)
                print("✓ Loaded failure prediction model")
            
            duration_model_file = self.model_path / "duration_prediction_model.pkl"
            if duration_model_file.exists():
                self.duration_model = joblib.load(duration_model_file)
                print("✓ Loaded duration prediction model")
            
            # Load scalers
            failure_scaler_file = self.model_path / "failure_scaler.pkl"
            if failure_scaler_file.exists():
                self.failure_scaler = joblib.load(failure_scaler_file)
            
            duration_scaler_file = self.model_path / "duration_scaler.pkl"
            if duration_scaler_file.exists():
                self.duration_scaler = joblib.load(duration_scaler_file)
                
        except Exception as e:
            print(f"Note: Could not load models: {e}")
            print("Models will be trained when sufficient data is available")
    
    def predict_failure(
        self,
        files_changed: int,
        lines_changed: int,
        test_coverage: float = 80.0,
        complexity: float = 5.0,
        hour_of_day: int = 12,
        previous_failures: int = 0,
        **kwargs
    ) -> Dict:
        """
        Predict if a build will fail
        
        Returns:
            dict with prediction results including probability and risk level
        """
        # Create feature vector
        features = np.array([[
            files_changed,
            lines_changed,
            test_coverage,
            complexity,
            hour_of_day,
            previous_failures
        ]])
        
        # If model exists, use it; otherwise use heuristic
        if self.failure_model and self.failure_scaler:
            features_scaled = self.failure_scaler.transform(features)
            prediction_proba = self.failure_model.predict_proba(features_scaled)[0]
            failure_probability = float(prediction_proba[1])  # Probability of failure
            will_fail = failure_probability > settings.PREDICTION_CONFIDENCE_THRESHOLD
        else:
            # Heuristic-based prediction when no model
            failure_probability = self._heuristic_failure_prediction(
                files_changed, lines_changed, test_coverage, complexity, previous_failures
            )
            will_fail = failure_probability > 0.5
        
        # Determine risk level
        if failure_probability < 0.3:
            risk_level = "low"
        elif failure_probability < 0.6:
            risk_level = "medium"
        else:
            risk_level = "high"
        
        # Generate recommendation
        recommendation = self._generate_failure_recommendation(
            failure_probability, files_changed, lines_changed, test_coverage
        )
        
        # Identify key risk factors
        factors = {
            "files_changed": files_changed > 15,
            "large_change": lines_changed > 500,
            "low_coverage": test_coverage < 70,
            "high_complexity": complexity > 7,
            "recent_failures": previous_failures > 2
        }
        
        return {
            "will_fail": will_fail,
            "failure_probability": round(failure_probability, 3),
            "confidence": 0.85 if self.failure_model else 0.65,
            "risk_level": risk_level,
            "recommendation": recommendation,
            "factors": factors
        }
    
    def predict_duration(
        self,
        files_changed: int,
        lines_changed: int,
        test_count: int = 50,
        language: str = "python",
        **kwargs
    ) -> Dict:
        """
        Predict build duration in seconds
        
        Returns:
            dict with duration estimate and confidence interval
        """
        # Create feature vector
        features = np.array([[
            files_changed,
            lines_changed,
            test_count,
            self._language_to_numeric(language)
        ]])
        
        # If model exists, use it; otherwise use heuristic
        if self.duration_model and self.duration_scaler:
            features_scaled = self.duration_scaler.transform(features)
            estimated_duration = int(self.duration_model.predict(features_scaled)[0])
            confidence = 0.85
        else:
            # Heuristic-based prediction
            estimated_duration = self._heuristic_duration_prediction(
                files_changed, lines_changed, test_count, language
            )
            confidence = 0.70
        
        # Calculate confidence interval (±15%)
        margin = int(estimated_duration * 0.15)
        range_min = max(30, estimated_duration - margin)
        range_max = estimated_duration + margin
        
        factors = {
            "files_impact": files_changed * 5,
            "lines_impact": lines_changed // 10,
            "test_impact": test_count * 2,
            "language_factor": self._get_language_factor(language)
        }
        
        return {
            "estimated_duration": estimated_duration,
            "confidence": confidence,
            "range_min": range_min,
            "range_max": range_max,
            "factors": factors
        }
    
    def _heuristic_failure_prediction(
        self,
        files_changed: int,
        lines_changed: int,
        test_coverage: float,
        complexity: float,
        previous_failures: int
    ) -> float:
        """Heuristic-based failure prediction when no ML model"""
        risk_score = 0.0
        
        # File changes factor
        if files_changed > 20:
            risk_score += 0.25
        elif files_changed > 10:
            risk_score += 0.15
        elif files_changed > 5:
            risk_score += 0.05
        
        # Lines changed factor
        if lines_changed > 1000:
            risk_score += 0.25
        elif lines_changed > 500:
            risk_score += 0.15
        elif lines_changed > 200:
            risk_score += 0.05
        
        # Test coverage factor
        if test_coverage < 60:
            risk_score += 0.20
        elif test_coverage < 75:
            risk_score += 0.10
        
        # Complexity factor
        if complexity > 8:
            risk_score += 0.15
        elif complexity > 6:
            risk_score += 0.08
        
        # Previous failures factor
        risk_score += min(previous_failures * 0.10, 0.30)
        
        return min(risk_score, 0.95)
    
    def _heuristic_duration_prediction(
        self,
        files_changed: int,
        lines_changed: int,
        test_count: int,
        language: str
    ) -> int:
        """Heuristic-based duration prediction"""
        base_duration = 60  # 1 minute base
        
        # Add time based on files
        base_duration += files_changed * 8
        
        # Add time based on lines
        base_duration += lines_changed // 20
        
        # Add time based on tests
        base_duration += test_count * 2
        
        # Language multiplier
        multiplier = self._get_language_factor(language)
        base_duration = int(base_duration * multiplier)
        
        return min(base_duration, 1800)  # Max 30 minutes
    
    def _language_to_numeric(self, language: str) -> int:
        """Convert language to numeric value"""
        language_map = {
            "python": 1,
            "nodejs": 2,
            "java": 3,
            "go": 4,
            "ruby": 5,
            "php": 6,
            "other": 7
        }
        return language_map.get(language.lower(), 7)
    
    def _get_language_factor(self, language: str) -> float:
        """Get duration multiplier for language"""
        factors = {
            "python": 1.0,
            "nodejs": 0.9,
            "java": 1.5,
            "go": 0.8,
            "ruby": 1.1,
            "php": 1.0,
            "other": 1.0
        }
        return factors.get(language.lower(), 1.0)
    
    def _generate_failure_recommendation(
        self,
        failure_probability: float,
        files_changed: int,
        lines_changed: int,
        test_coverage: float
    ) -> str:
        """Generate actionable recommendation"""
        if failure_probability < 0.3:
            return "Build looks healthy. Proceed with confidence."
        elif failure_probability < 0.6:
            recommendations = []
            if files_changed > 15:
                recommendations.append("Consider breaking changes into smaller commits")
            if test_coverage < 75:
                recommendations.append("Improve test coverage before deploying")
            if lines_changed > 500:
                recommendations.append("Large changeset detected - review carefully")
            
            return " | ".join(recommendations) if recommendations else "Monitor build closely"
        else:
            return "HIGH RISK: Review changes thoroughly, add tests, and consider manual testing first"


# Global predictor instance
_predictor = None

def get_predictor() -> BuildPredictor:
    """Get or create global predictor instance"""
    global _predictor
    if _predictor is None:
        _predictor = BuildPredictor()
    return _predictor
