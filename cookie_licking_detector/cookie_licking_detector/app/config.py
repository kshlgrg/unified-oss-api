import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    
    GRACE_PERIODS = {
        "high_reliability": 21,
        "moderate_reliability": 14,
        "low_reliability": 7,
        "first_time_contributor": 14
    }
    
    CLAIM_KEYWORDS = [
        "i'll work on this",
        "i'll take this",
        "i can fix this",
        "assign me",
        "working on it",
        "i got this",
        "let me handle this",
        "i'll handle this"
    ]
    
    STALENESS_THRESHOLDS = {
        "healthy": 0.3,
        "needs_monitoring": 0.5,
        "needs_nudge": 0.7,
        "critical": 0.85
    }
    
    RISK_WEIGHTS = {
        "days_stale": 0.3,
        "days_inactive": 0.25,
        "completion_rate": 0.2,
        "recent_commits": 0.15,
        "issue_priority": 0.1
    }
