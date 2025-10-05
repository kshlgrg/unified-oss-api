from typing import Dict, List
from datetime import datetime
from .github_client import GitHubClient
from .config import Config

class MilestoneDetector:
    def __init__(self, github_token: str = None):
        self.client = GitHubClient(github_token)
        self.config = Config()
    
    def detect_user_milestones(self, username: str, repo: str = None) -> List[Dict]:
        milestones = []
        
        prs = self.client.get_user_prs(username, repo)
        pr_count = len(prs)
        milestones.extend(self._check_threshold("pr_merged", pr_count))
        
        issues = self.client.get_user_issues(username, repo)
        issue_count = len(issues)
        milestones.extend(self._check_threshold("issues", issue_count))
        
        return milestones
    
    def detect_repo_milestones(self, repo: str) -> List[Dict]:
        milestones = []
        
        repo_data = self.client.get_repo_stats(repo)
        
        stars = repo_data.get("stargazers_count", 0)
        milestones.extend(self._check_threshold("stars", stars))
        
        forks = repo_data.get("forks_count", 0)
        milestones.extend(self._check_threshold("forks", forks))
        
        return milestones
    
    def predict_next_milestones(self, username: str, repo: str = None) -> List[Dict]:
        predictions = []
        
        prs = self.client.get_user_prs(username, repo)
        pr_count = len(prs)
        
        issues = self.client.get_user_issues(username, repo)
        issue_count = len(issues)
        
        next_pr = self._find_next_threshold("pr_merged", pr_count)
        if next_pr:
            predictions.append({
                "type": "pr_merged",
                "current": pr_count,
                "next_milestone": next_pr,
                "remaining": next_pr - pr_count,
                "icon": self.config.MILESTONE_ICONS.get(f"pr_merged_{next_pr}", {}).get("icon", "🎯"),
                "title": self.config.MILESTONE_ICONS.get(f"pr_merged_{next_pr}", {}).get("title", f"{next_pr} PRs")
            })
        
        next_issue = self._find_next_threshold("issues", issue_count)
        if next_issue:
            predictions.append({
                "type": "issues",
                "current": issue_count,
                "next_milestone": next_issue,
                "remaining": next_issue - issue_count,
                "icon": self.config.MILESTONE_ICONS.get(f"issues_{next_issue}", {}).get("icon", "🐛"),
                "title": self.config.MILESTONE_ICONS.get(f"issues_{next_issue}", {}).get("title", f"{next_issue} Issues")
            })
        
        return predictions
    
    def _check_threshold(self, milestone_type: str, count: int) -> List[Dict]:
        milestones = []
        thresholds = self.config.MILESTONE_THRESHOLDS.get(milestone_type, [])
        
        for threshold in thresholds:
            if count >= threshold:
                milestone = self._create_milestone(f"{milestone_type}_{threshold}", count)
                if milestone:
                    milestones.append(milestone)
        
        return milestones
    
    def _find_next_threshold(self, milestone_type: str, current_count: int) -> int:
        thresholds = self.config.MILESTONE_THRESHOLDS.get(milestone_type, [])
        for threshold in thresholds:
            if current_count < threshold:
                return threshold
        return None
    
    def _create_milestone(self, milestone_key: str, count: int) -> Dict:
        icon_data = self.config.MILESTONE_ICONS.get(milestone_key)
        if not icon_data:
            return None
        
        return {
            "id": f"m_{milestone_key}_{int(datetime.now().timestamp())}",
            "type": milestone_key,
            "icon": icon_data["icon"],
            "title": icon_data["title"],
            "count": count,
            "achieved_at": datetime.now().isoformat(),
            "celebrated": False
        }
