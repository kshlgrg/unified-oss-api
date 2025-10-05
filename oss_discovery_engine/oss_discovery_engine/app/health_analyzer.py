from typing import Dict, List
from datetime import datetime, timedelta, timezone
from .github_client import GitHubClient
from .config import Config

class HealthAnalyzer:
    def __init__(self, github_token: str = None):
        self.client = GitHubClient(github_token)
        self.config = Config()
    
    def analyze_repo_health(self, repo_full_name: str) -> Dict:
        try:
            repo_details = self.client.get_repo_details(repo_full_name)
            
            recent_commits = self._check_recent_activity(repo_full_name)
            maintainer_responsiveness = self._estimate_responsiveness(repo_full_name)
            community_activity = self._assess_community_activity(repo_details)
            beginner_friendly = self._check_beginner_friendliness(repo_full_name, repo_details)
            
            overall_health = self._calculate_overall_health(
                recent_commits, maintainer_responsiveness, 
                community_activity, beginner_friendly
            )
            
            return {
                "maintainer_responsiveness": maintainer_responsiveness,
                "community_activity": community_activity,
                "recent_activity": recent_commits,
                "beginner_friendly": beginner_friendly,
                "overall_health": overall_health,
                "has_contributing_guide": self._has_file(repo_details, "CONTRIBUTING"),
                "has_code_of_conduct": self._has_file(repo_details, "CODE_OF_CONDUCT"),
                "has_license": repo_details.get("license") is not None
            }
        except Exception as e:
            return {
                "maintainer_responsiveness": "unknown",
                "community_activity": "unknown",
                "recent_activity": False,
                "beginner_friendly": False,
                "overall_health": "unknown",
                "error": str(e)
            }
    
    def _check_recent_activity(self, repo: str) -> bool:
        try:
            thirty_days_ago = (datetime.now(timezone.utc) - timedelta(days=30)).isoformat()
            commits = self.client.get_repo_commits(repo, since=thirty_days_ago)
            return len(commits) > 0
        except:
            return False
    
    def _estimate_responsiveness(self, repo: str) -> str:
        try:
            issues = self.client.get_repo_issues(repo, state="closed")[:10]
            
            if not issues:
                return "unknown"
            
            response_times = []
            
            for issue in issues:
                created = datetime.fromisoformat(issue["created_at"].replace("Z", "+00:00"))
                closed = datetime.fromisoformat(issue["closed_at"].replace("Z", "+00:00"))
                days = (closed - created).days
                response_times.append(days)
            
            avg_days = sum(response_times) / len(response_times) if response_times else 999
            
            if avg_days <= 2:
                return "excellent"
            elif avg_days <= 7:
                return "good"
            elif avg_days <= 14:
                return "moderate"
            else:
                return "slow"
        except:
            return "unknown"
    
    def _assess_community_activity(self, repo_details: Dict) -> str:
        stars = repo_details.get("stargazers_count", 0)
        forks = repo_details.get("forks_count", 0)
        watchers = repo_details.get("watchers_count", 0)
        open_issues = repo_details.get("open_issues_count", 0)
        
        activity_score = (stars * 0.4 + forks * 0.3 + watchers * 0.2 + open_issues * 0.1)
        
        if activity_score > 5000:
            return "very_active"
        elif activity_score > 1000:
            return "active"
        elif activity_score > 100:
            return "moderate"
        else:
            return "low"
    
    def _check_beginner_friendliness(self, repo: str, repo_details: Dict) -> bool:
        try:
            issues = self.client.get_repo_issues(repo, labels="good first issue")
            
            has_good_first_issues = len(issues) > 0
            has_description = repo_details.get("description") is not None
            has_topics = len(repo_details.get("topics", [])) > 0
            
            return has_good_first_issues or (has_description and has_topics)
        except:
            return False
    
    def _has_file(self, repo_details: Dict, filename: str) -> bool:
        return True
    
    def _calculate_overall_health(self, recent: bool, responsiveness: str, 
                                  activity: str, beginner: bool) -> str:
        score = 0
        
        if recent:
            score += 3
        
        responsiveness_scores = {"excellent": 3, "good": 2, "moderate": 1, "slow": 0, "unknown": 1}
        score += responsiveness_scores.get(responsiveness, 0)
        
        activity_scores = {"very_active": 3, "active": 2, "moderate": 1, "low": 0, "unknown": 1}
        score += activity_scores.get(activity, 0)
        
        if beginner:
            score += 2
        
        if score >= 9:
            return "excellent"
        elif score >= 6:
            return "good"
        elif score >= 3:
            return "moderate"
        else:
            return "poor"
