from gh_maintainer_dashboard.core.github_client import GitHubClient
from gh_maintainer_dashboard.models.maintainer import MaintainerProfile
from gh_maintainer_dashboard.models.repository import RepositoryData
from gh_maintainer_dashboard.analyzers.activity_analyzer import ActivityAnalyzer

__version__ = "0.1.0"
__all__ = [
    "GitHubClient",
    "MaintainerProfile", 
    "RepositoryData",
    "ActivityAnalyzer",
]


class MaintainerDashboard:
    def __init__(self, github_token: str = None):
        from gh_maintainer_dashboard.core.config import Config
        
        self.config = Config(github_token=github_token)
        self.github_client = GitHubClient(self.config)
        self.activity_analyzer = ActivityAnalyzer(self.github_client)
        
    def get_profile(self, username: str) -> dict:
        from gh_maintainer_dashboard.analyzers.activity_analyzer import ActivityAnalyzer
        
        analyzer = ActivityAnalyzer(self.github_client)
        return analyzer.get_full_profile(username)
    
    def export_cv(self, username: str, format: str = "json") -> dict:
        from gh_maintainer_dashboard.exporters.cv_generator import CVGenerator
        
        generator = CVGenerator(self.github_client)
        return generator.generate_cv(username, format)
    
    def find_similar_maintainers(self, username: str, limit: int = 10) -> list:
        from gh_maintainer_dashboard.analyzers.network_matcher import NetworkMatcher
        
        matcher = NetworkMatcher(self.github_client)
        return matcher.find_similar(username, limit)
    
    def get_repositories(self, username: str) -> dict:
        from gh_maintainer_dashboard.analyzers.repo_analyzer import RepoAnalyzer
        
        analyzer = RepoAnalyzer(self.github_client)
        return analyzer.get_repository_breakdown(username)
    
    def get_timeline(self, username: str, period: str = "30d") -> dict:
        from gh_maintainer_dashboard.analyzers.timeline_analyzer import TimelineAnalyzer
        
        analyzer = TimelineAnalyzer(self.github_client)
        return analyzer.get_activity_timeline(username, period)
