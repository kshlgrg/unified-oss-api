from typing import List, Dict
from gh_maintainer_dashboard.core.github_client import GitHubClient
from gh_maintainer_dashboard.models.repository import RepositoryData, MaintainerActivity


class RepoCollector:
    def __init__(self, github_client: GitHubClient):
        self.client = github_client
    
    def collect_user_repositories(self, username: str) -> List[RepositoryData]:
        repos_data = []
        repos = self.client.get_user_repos(username)
        
        for repo in repos:
            repo_data = self._parse_repository(repo, username)
            repos_data.append(repo_data)
        
        return repos_data
    
    def _parse_repository(self, repo: Dict, username: str) -> RepositoryData:
        languages = self._extract_languages(repo)
        topics = repo.get("topics", [])
        
        return RepositoryData(
            name=repo.get("name", ""),
            full_name=repo.get("full_name", ""),
            url=repo.get("html_url", ""),
            description=repo.get("description", ""),
            role=self._determine_role(repo, username),
            stars=repo.get("stargazers_count", 0),
            forks=repo.get("forks_count", 0),
            open_issues=repo.get("open_issues_count", 0),
            languages=languages,
            topics=topics,
        )
    
    def _extract_languages(self, repo: Dict) -> List[str]:
        languages = []
        if repo.get("language"):
            languages.append(repo.get("language"))
        return languages
    
    def _determine_role(self, repo: Dict, username: str) -> str:
        permissions = repo.get("permissions", {})
        
        if permissions.get("admin"):
            return "maintainer"
        elif permissions.get("push"):
            return "collaborator"
        else:
            return "contributor"
    
    def get_maintained_repos(self, username: str) -> List[RepositoryData]:
        all_repos = self.collect_user_repositories(username)
        maintained = [repo for repo in all_repos if repo.role in ["maintainer", "collaborator"]]
        return maintained
    
    def get_repo_summary(self, repos: List[RepositoryData]) -> Dict:
        languages_count = {}
        total_stars = 0
        
        for repo in repos:
            for lang in repo.languages:
                languages_count[lang] = languages_count.get(lang, 0) + 1
            total_stars += repo.stars
        
        most_active = max(repos, key=lambda r: r.stars) if repos else None
        
        return {
            "total_repos": len(repos),
            "most_active_repo": most_active.name if most_active else None,
            "repos_by_language": languages_count,
            "total_stars": total_stars,
        }
