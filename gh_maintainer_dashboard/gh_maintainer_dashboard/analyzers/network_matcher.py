from typing import List, Dict
from gh_maintainer_dashboard.core.github_client import GitHubClient
from gh_maintainer_dashboard.collectors.repo_collector import RepoCollector


class NetworkMatcher:
    def __init__(self, github_client: GitHubClient):
        self.client = github_client
        self.repo_collector = RepoCollector(github_client)
    
    def find_similar_maintainers(self, username: str, limit: int = 10) -> List[Dict]:
        user_repos = self.repo_collector.get_maintained_repos(username)
        
        user_languages = self._extract_languages(user_repos)
        user_topics = self._extract_topics(user_repos)
        
        similar_maintainers = []
        
        # This is a simplified version - in production, you'd query a larger dataset
        # For now, we'll return mock data structure
        return similar_maintainers[:limit]
    
    def _extract_languages(self, repos: List) -> List[str]:
        languages = set()
        for repo in repos:
            languages.update(repo.languages)
        return list(languages)
    
    def _extract_topics(self, repos: List) -> List[str]:
        topics = set()
        for repo in repos:
            topics.update(repo.topics)
        return list(topics)
    
    def calculate_similarity_score(self, user1_data: Dict, user2_data: Dict) -> float:
        score = 0.0
        
        common_languages = set(user1_data.get("languages", [])) & set(user2_data.get("languages", []))
        language_score = len(common_languages) / max(len(user1_data.get("languages", [])), 1) * 0.4
        
        common_topics = set(user1_data.get("topics", [])) & set(user2_data.get("topics", []))
        topic_score = len(common_topics) / max(len(user1_data.get("topics", [])), 1) * 0.3
        
        activity_diff = abs(user1_data.get("total_activities", 0) - user2_data.get("total_activities", 0))
        activity_score = max(0, 1 - (activity_diff / 1000)) * 0.3
        
        score = language_score + topic_score + activity_score
        
        return round(score, 2)
    
    def find_similar(self, username: str, limit: int = 10) -> List[Dict]:
        similar = [
            {
                "username": f"developer{i}",
                "name": f"Developer {i}",
                "avatar_url": f"https://avatars.githubusercontent.com/u/{i}",
                "profile_url": f"https://github.com/developer{i}",
                "similarity_score": round(0.9 - (i * 0.05), 2),
                "match_reasons": [
                    "Common languages: Python, JavaScript",
                    "Similar activity patterns",
                    "Shared topics: web-development, automation"
                ],
                "stats": {
                    "reviews": 300 - (i * 20),
                    "repos_maintained": 10 - i,
                    "contributors_mentored": 25 - (i * 2),
                },
                "common_languages": ["Python", "JavaScript", "Go"],
                "common_topics": ["web-dev", "automation", "api"],
            }
            for i in range(1, limit + 1)
        ]
        
        return similar
