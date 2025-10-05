from typing import Dict, List
from datetime import datetime, timedelta, timezone
from .github_client import GitHubClient
from .config import Config

class ProfileAnalyzer:
    def __init__(self, github_token: str = None):
        self.client = GitHubClient(github_token)
        self.config = Config()
    
    def analyze_user_profile(self, username: str) -> Dict:
        print(f"Analyzing GitHub profile: @{username}...")
        
        user_info = self.client.get_user_profile(username)
        repos = self.client.get_user_repos(username)
        events = self.client.get_user_events(username)
        
        languages = self._extract_languages(repos)
        topics = self._extract_topics(repos)
        contribution_stats = self._calculate_contributions(events)
        skill_level = self._determine_skill_level(contribution_stats, repos)
        contribution_style = self._determine_contribution_style(events)
        
        return {
            "username": username,
            "profile_url": user_info.get("html_url"),
            "name": user_info.get("name"),
            "bio": user_info.get("bio"),
            "public_repos": user_info.get("public_repos"),
            "followers": user_info.get("followers"),
            "following": user_info.get("following"),
            "created_at": user_info.get("created_at"),
            
            "analyzed_skills": {
                "languages": languages,
                "topics": topics,
                "skill_level": skill_level,
                "contribution_style": contribution_style
            },
            
            "github_stats": contribution_stats,
            
            "preferences": {
                "preferred_languages": list(languages.keys())[:3],
                "preferred_topics": list(topics)[:5],
                "preferred_complexity": self._map_skill_to_complexity(skill_level)
            }
        }
    
    def _extract_languages(self, repos: List[Dict]) -> Dict:
        language_count = {}
        
        for repo in repos:
            lang = repo.get("language")
            if lang:
                language_count[lang] = language_count.get(lang, 0) + 1
        
        total = sum(language_count.values())
        language_expertise = {
            lang: round(count / total, 2) 
            for lang, count in language_count.items()
        }
        
        return dict(sorted(language_expertise.items(), key=lambda x: x[1], reverse=True))
    
    def _extract_topics(self, repos: List[Dict]) -> List[str]:
        topics = set()
        
        for repo in repos:
            repo_topics = repo.get("topics", [])
            topics.update(repo_topics)
        
        return list(topics)
    
    def _calculate_contributions(self, events: List[Dict]) -> Dict:
        commits = 0
        prs = 0
        issues = 0
        reviews = 0
        
        for event in events:
            event_type = event.get("type")
            
            if event_type == "PushEvent":
                commits += len(event.get("payload", {}).get("commits", []))
            elif event_type == "PullRequestEvent":
                prs += 1
            elif event_type == "IssuesEvent":
                issues += 1
            elif event_type == "PullRequestReviewEvent":
                reviews += 1
        
        total_contributions = commits + prs + issues + reviews
        
        return {
            "total_contributions": total_contributions,
            "commits": commits,
            "prs": prs,
            "issues": issues,
            "reviews": reviews
        }
    
    def _determine_skill_level(self, stats: Dict, repos: List[Dict]) -> str:
        total = stats["total_contributions"]
        
        if total >= 100:
            return "advanced"
        elif total >= 20:
            return "intermediate"
        else:
            return "beginner"
    
    def _determine_contribution_style(self, events: List[Dict]) -> str:
        issue_count = len([e for e in events if e["type"] == "IssuesEvent"])
        pr_count = len([e for e in events if e["type"] == "PullRequestEvent"])
        
        if issue_count > pr_count:
            return "issue_reporter"
        elif pr_count > issue_count * 2:
            return "feature_builder"
        else:
            return "issue_solver"
    
    def _map_skill_to_complexity(self, skill_level: str) -> str:
        mapping = {
            "beginner": "beginner",
            "intermediate": "intermediate",
            "advanced": "advanced"
        }
        return mapping.get(skill_level, "intermediate")
