from typing import List, Dict
from datetime import datetime
from gh_maintainer_dashboard.core.github_client import GitHubClient
from gh_maintainer_dashboard.models.activity import IssueActivity, ActivityType


class IssueCollector:
    def __init__(self, github_client: GitHubClient):
        self.client = github_client
    
    def collect_user_issue_activities(self, username: str) -> List[IssueActivity]:
        activities = []
        events = self.client.get_user_events(username)
        
        for event in events:
            if event.get("type") == "IssuesEvent":
                activity_data = self._parse_issue_event(event)
                if activity_data:
                    activities.append(activity_data)
        
        return activities
    
    def _parse_issue_event(self, event: Dict) -> IssueActivity:
        payload = event.get("payload", {})
        issue = payload.get("issue", {})
        repo = event.get("repo", {})
        
        return IssueActivity(
            id=f"issue_{event.get('id')}",
            type=ActivityType.ISSUE_TRIAGE,
            repository=repo.get("name", "").split("/")[-1],
            repository_full_name=repo.get("name", ""),
            timestamp=datetime.fromisoformat(event.get("created_at", "").replace("Z", "+00:00")),
            title=issue.get("title", ""),
            url=issue.get("html_url", ""),
            issue_number=issue.get("number", 0),
            action=payload.get("action", ""),
            labels_added=self._extract_labels(issue.get("labels", [])),
            metadata={
                "issue_url": issue.get("html_url"),
                "issue_state": issue.get("state"),
            }
        )
    
    def _extract_labels(self, labels: List[Dict]) -> List[str]:
        return [label.get("name", "") for label in labels]
    
    def get_issue_stats(self, username: str) -> Dict:
        activities = self.collect_user_issue_activities(username)
        
        total_issues = len(activities)
        opened = sum(1 for a in activities if a.action == "opened")
        closed = sum(1 for a in activities if a.action == "closed")
        labeled = sum(1 for a in activities if a.labels_added)
        
        return {
            "total_issue_activities": total_issues,
            "opened": opened,
            "closed": closed,
            "labeled": labeled,
            "closure_rate": closed / opened if opened > 0 else 0,
        }
