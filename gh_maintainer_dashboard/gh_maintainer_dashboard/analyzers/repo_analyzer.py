from typing import Dict, List
from gh_maintainer_dashboard.core.github_client import GitHubClient
from gh_maintainer_dashboard.collectors.repo_collector import RepoCollector
from gh_maintainer_dashboard.models.repository import RepositoryData


class RepoAnalyzer:
    def __init__(self, github_client: GitHubClient):
        self.client = github_client
        self.repo_collector = RepoCollector(github_client)
    
    def get_repository_breakdown(self, username: str) -> Dict:
        repos = self.repo_collector.get_maintained_repos(username)
        summary = self.repo_collector.get_repo_summary(repos)
        
        return {
            "repositories": [repo.dict() for repo in repos],
            "summary": summary,
        }
    
    def analyze_repository_health(self, repo: RepositoryData) -> Dict:
        health_score = 0.0
        
        if repo.stars > 100:
            health_score += 0.3
        elif repo.stars > 10:
            health_score += 0.15
        
        if repo.forks > 20:
            health_score += 0.2
        elif repo.forks > 5:
            health_score += 0.1
        
        if repo.open_issues < 50:
            health_score += 0.3
        elif repo.open_issues < 100:
            health_score += 0.15
        
        health_score += 0.2
        
        if health_score > 0.7:
            engagement = "high"
        elif health_score > 0.4:
            engagement = "medium"
        else:
            engagement = "low"
        
        return {
            "health_score": round(health_score, 2),
            "community_engagement": engagement,
        }
