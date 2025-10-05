from typing import List, Dict
from datetime import datetime
from gh_maintainer_dashboard.core.github_client import GitHubClient
from gh_maintainer_dashboard.models.activity import CommitActivity, ActivityType


class CommitCollector:
    def __init__(self, github_client: GitHubClient):
        self.client = github_client
    
    def collect_user_commits(self, username: str) -> List[CommitActivity]:
        commits = []
        events = self.client.get_user_events(username)
        
        for event in events:
            if event.get("type") == "PushEvent":
                commit_data = self._parse_push_event(event)
                commits.extend(commit_data)
        
        return commits
    
    def _parse_push_event(self, event: Dict) -> List[CommitActivity]:
        payload = event.get("payload", {})
        commits_data = payload.get("commits", [])
        repo = event.get("repo", {})
        
        commits = []
        for commit in commits_data:
            commits.append(CommitActivity(
                id=f"commit_{commit.get('sha')}",
                type=ActivityType.COMMIT,
                repository=repo.get("name", "").split("/")[-1],
                repository_full_name=repo.get("name", ""),
                timestamp=datetime.fromisoformat(event.get("created_at", "").replace("Z", "+00:00")),
                title=commit.get("message", "").split("\n")[0],
                url=commit.get("url", ""),
                sha=commit.get("sha", ""),
                message=commit.get("message", ""),
                metadata={
                    "commit_url": commit.get("url"),
                }
            ))
        
        return commits
    
    def categorize_commits(self, commits: List[CommitActivity]) -> Dict:
        ci_keywords = ["ci", "travis", "github actions", "workflow", "pipeline", "build"]
        doc_keywords = ["readme", "docs", "documentation", "comment"]
        
        ci_commits = []
        doc_commits = []
        regular_commits = []
        
        for commit in commits:
            message_lower = commit.message.lower()
            
            if any(keyword in message_lower for keyword in ci_keywords):
                ci_commits.append(commit)
            elif any(keyword in message_lower for keyword in doc_keywords):
                doc_commits.append(commit)
            else:
                regular_commits.append(commit)
        
        return {
            "ci_fixes": ci_commits,
            "documentation": doc_commits,
            "regular": regular_commits,
        }
    
    def get_commit_stats(self, username: str) -> Dict:
        commits = self.collect_user_commits(username)
        categorized = self.categorize_commits(commits)
        
        return {
            "total_commits": len(commits),
            "ci_fixes": len(categorized["ci_fixes"]),
            "documentation_commits": len(categorized["documentation"]),
            "regular_commits": len(categorized["regular"]),
        }
