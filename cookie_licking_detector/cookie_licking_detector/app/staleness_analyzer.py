from typing import Dict
from datetime import datetime, timedelta, timezone
from .config import Config

class StalenessAnalyzer:
    def __init__(self):
        self.config = Config()
    
    def analyze_staleness(self, claim_info: Dict, progress: Dict, user_reliability: float) -> Dict:
        claimed_at = datetime.fromisoformat(claim_info["claimed_at"].replace("Z", "+00:00"))
        now = datetime.now(timezone.utc)
        
        days_since_claim = (now - claimed_at).days
        
        last_activity = progress.get("last_activity")
        if last_activity:
            last_activity_date = datetime.fromisoformat(last_activity.replace("Z", "+00:00"))
            days_since_activity = (now - last_activity_date).days
        else:
            days_since_activity = days_since_claim
        
        staleness_score = self._calculate_staleness_score(
            days_since_claim, 
            days_since_activity,
            user_reliability,
            progress
        )
        
        status = self._get_status(staleness_score)
        risk_level = self._get_risk_level(staleness_score)
        
        grace_period = self._calculate_grace_period(user_reliability)
        
        return {
            "days_stale": days_since_claim,
            "days_inactive": days_since_activity,
            "staleness_score": round(staleness_score, 2),
            "status": status,
            "risk_level": risk_level,
            "exceeds_grace_period": days_since_claim > grace_period,
            "grace_period_days": grace_period
        }
    
    def _calculate_staleness_score(self, days_claim: int, days_inactive: int, 
                                   reliability: float, progress: Dict) -> float:
        time_factor = min(days_claim / 30, 1.0) * 0.4
        
        inactivity_factor = min(days_inactive / 21, 1.0) * 0.3
        
        reliability_factor = (1 - reliability) * 0.2
        
        progress_factor = 0.1
        if not progress.get("has_commits") and not progress.get("has_linked_pr"):
            progress_factor = 0.1
        else:
            progress_factor = 0.0
        
        score = time_factor + inactivity_factor + reliability_factor + progress_factor
        
        return min(score, 1.0)
    
    def _get_status(self, score: float) -> str:
        thresholds = self.config.STALENESS_THRESHOLDS
        
        if score >= thresholds["critical"]:
            return "critical"
        elif score >= thresholds["needs_nudge"]:
            return "needs_nudge"
        elif score >= thresholds["needs_monitoring"]:
            return "needs_monitoring"
        else:
            return "healthy"
    
    def _get_risk_level(self, score: float) -> str:
        if score >= 0.85:
            return "high"
        elif score >= 0.6:
            return "medium"
        else:
            return "low"
    
    def _calculate_grace_period(self, reliability: float) -> int:
        periods = self.config.GRACE_PERIODS
        
        if reliability >= 0.8:
            return periods["high_reliability"]
        elif reliability >= 0.5:
            return periods["moderate_reliability"]
        else:
            return periods["low_reliability"]
