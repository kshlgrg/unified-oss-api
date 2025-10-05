from typing import Dict, List
from datetime import datetime, timedelta, timezone
from .github_client import GitHubClient

class UserProfiler:
    def __init__(self, github_token: str = None):
        self.client = GitHubClient(github_token)
    
    def get_user_profile(self, username: str, repo: str = None) -> Dict:
        user_info = self.client.get_user_info(username)
        
        claimed_issues = self._get_user_claimed_issues(username, repo)
        
        reliability = self._calculate_reliability(claimed_issues)
        
        recent_activity = self._get_recent_activity(username)
        
        past_performance = self._get_past_performance(username)
        
        return {
            "username": username,
            "name": user_info.get("name"),
            "avatar_url": user_info.get("avatar_url"),
            "profile_url": user_info.get("html_url"),
            "email": user_info.get("email"),
            "location": user_info.get("location"),
            "bio": user_info.get("bio"),
            "followers": user_info.get("followers"),
            "following": user_info.get("following"),
            "public_repos": user_info.get("public_repos"),
            "member_since": user_info.get("created_at"),
            "reliability_metrics": reliability,
            "recent_activity_30d": recent_activity,
            "past_performance": past_performance
        }
    
    def _get_user_claimed_issues(self, username: str, repo: str = None) -> List[Dict]:
        query = f"author:{username} type:issue"
        if repo:
            query += f" repo:{repo}"
        
        return self.client.search_issues(query)
    
    def _calculate_reliability(self, claimed_issues: List[Dict]) -> Dict:
        total = len(claimed_issues)
        completed = len([i for i in claimed_issues if i["state"] == "closed"])
        abandoned = total - completed
        
        completion_rate = completed / total if total > 0 else 0
        reliability_score = completion_rate * 0.7 + (1 - abandoned / max(total, 1)) * 0.3
        
        return {
            "total_issues_claimed": total,
            "completed_issues": completed,
            "abandoned_issues": abandoned,
            "completion_rate": round(completion_rate, 2),
            "reliability_score": round(reliability_score, 2),
            "rating": self._get_rating(reliability_score)
        }
    
    def _get_rating(self, score: float) -> str:
        if score >= 0.8:
            return "excellent"
        elif score >= 0.6:
            return "good"
        elif score >= 0.4:
            return "moderate"
        else:
            return "low"
    
    def _get_recent_activity(self, username: str) -> Dict:
        events = self.client.get_user_events(username)
        
        thirty_days_ago = datetime.now(timezone.utc) - timedelta(days=30)
        
        commits = 0
        prs_opened = 0
        issues_opened = 0
        comments = 0
        
        for event in events:
            event_date = datetime.fromisoformat(event["created_at"].replace("Z", "+00:00"))
            if event_date < thirty_days_ago:
                continue
            
            if event["type"] == "PushEvent":
                commits += len(event.get("payload", {}).get("commits", []))
            elif event["type"] == "PullRequestEvent":
                prs_opened += 1
            elif event["type"] == "IssuesEvent":
                issues_opened += 1
            elif event["type"] in ["IssueCommentEvent", "PullRequestReviewCommentEvent"]:
                comments += 1
        
        return {
            "commits": commits,
            "prs_opened": prs_opened,
            "issues_opened": issues_opened,
            "comments": comments,
            "activity_level": "active" if commits > 10 else "moderate" if commits > 5 else "low"
        }
    
    def _get_past_performance(self, username: str) -> List[Dict]:
        repos = self.client.get_user_repos(username)
        
        performance = []
        for repo in repos[:5]:
            issues = self.client.search_issues(f"author:{username} repo:{repo['full_name']} type:issue is:closed")
            
            if len(issues) > 0:
                performance.append({
                    "repo": repo["full_name"],
                    "issues_completed": len(issues),
                    "quality_rating": "good"
                })
        
        return performance
