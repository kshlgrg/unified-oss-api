import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    
    SKILL_LEVELS = {
        "beginner": {"min_contributions": 0, "max_contributions": 20},
        "intermediate": {"min_contributions": 20, "max_contributions": 100},
        "advanced": {"min_contributions": 100, "max_contributions": float('inf')}
    }
    
    COMPLEXITY_INDICATORS = {
        "beginner": ["good first issue", "beginner friendly", "easy", "documentation"],
        "intermediate": ["enhancement", "feature", "bug"],
        "advanced": ["performance", "architecture", "core", "critical"]
    }
    
    HEALTH_THRESHOLDS = {
        "excellent": {"response_days": 2, "merge_rate": 0.7, "recent_commits_days": 7},
        "good": {"response_days": 7, "merge_rate": 0.5, "recent_commits_days": 30},
        "moderate": {"response_days": 14, "merge_rate": 0.3, "recent_commits_days": 60}
    }
    
    MATCH_WEIGHTS = {
        "language_match": 0.30,
        "complexity_match": 0.20,
        "topic_match": 0.20,
        "activity_score": 0.15,
        "intent_score": 0.15
    }
    
    INTENT_FILTERS = {
        "solve_issues": {
            "min_open_issues": 5,
            "min_good_first_issues": 2,
            "must_have_issues": True
        },
        "fork_and_build": {
            "min_stars": 50,
            "min_forks": 10,
            "must_have_issues": False
        }
    }
