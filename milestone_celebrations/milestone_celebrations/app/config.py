import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    
    MILESTONE_THRESHOLDS = {
        "pr_merged": [1, 5, 10, 25, 50, 100],
        "issues": [1, 5, 10, 25, 50, 100],
        "stars": [10, 50, 100, 500, 1000, 5000],
        "forks": [10, 50, 100, 500, 1000]
    }
    
    MILESTONE_ICONS = {
        "pr_merged_1": {"icon": "🚀", "title": "First Pull Request Merged!"},
        "pr_merged_5": {"icon": "🎯", "title": "5 Pull Requests Merged!"},
        "pr_merged_10": {"icon": "🎉", "title": "10 Pull Requests Merged!"},
        "pr_merged_25": {"icon": "⭐", "title": "25 Pull Requests Merged!"},
        "pr_merged_50": {"icon": "🏆", "title": "50 Pull Requests Merged!"},
        "pr_merged_100": {"icon": "💯", "title": "100 Pull Requests Merged!"},
        
        "issues_1": {"icon": "🐛", "title": "First Issue Opened!"},
        "issues_5": {"icon": "📝", "title": "5 Issues Opened!"},
        "issues_10": {"icon": "📊", "title": "10 Issues Opened!"},
        "issues_25": {"icon": "📈", "title": "25 Issues Opened!"},
        "issues_50": {"icon": "🎖️", "title": "50 Issues Opened!"},
        "issues_100": {"icon": "🏅", "title": "100 Issues Opened!"},
        
        "stars_10": {"icon": "⭐", "title": "10 Stars!"},
        "stars_50": {"icon": "🌟", "title": "50 Stars!"},
        "stars_100": {"icon": "✨", "title": "100 Stars!"},
        "stars_500": {"icon": "💫", "title": "500 Stars!"},
        "stars_1000": {"icon": "🌠", "title": "1000 Stars!"},
        "stars_5000": {"icon": "🎆", "title": "5000 Stars!"},
        
        "forks_10": {"icon": "🔱", "title": "10 Forks!"},
        "forks_50": {"icon": "🔰", "title": "50 Forks!"},
        "forks_100": {"icon": "⚡", "title": "100 Forks!"},
        "forks_500": {"icon": "🚀", "title": "500 Forks!"},
        "forks_1000": {"icon": "🎯", "title": "1000 Forks!"}
    }
