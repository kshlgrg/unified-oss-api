from typing import Dict, List, Optional
from .github_client import GitHubClient
from .config import Config

class RepoSearcher:
    def __init__(self, github_token: str = None):
        self.client = GitHubClient(github_token)
        self.config = Config()
    
    def search_repos(self, user_profile: Dict, intent: str, query: str = "", 
                     filters: Dict = None) -> List[Dict]:
        print(f"\nSearching repositories for intent: {intent}...")
        
        languages = user_profile["analyzed_skills"]["languages"]
        primary_language = list(languages.keys())[0] if languages else "Python"
        
        search_query = self._build_search_query(query, intent, primary_language, filters)
        
        print(f"Search query: {search_query}")
        
        repos = self.client.search_repositories(search_query, per_page=50)
        
        print(f"Found {len(repos)} repositories.")
        
        if len(repos) == 0:
            print("No results. Trying broader search...")
            search_query = f"language:{primary_language} stars:>100"
            print(f"Fallback query: {search_query}")
            repos = self.client.search_repositories(search_query, per_page=50)
            print(f"Found {len(repos)} repositories with fallback.\n")
        
        filtered_repos = self._apply_intent_filters(repos, intent, filters)
        
        print(f"After filtering: {len(filtered_repos)} repositories.\n")
        
        return filtered_repos
    
    def _build_search_query(self, query: str, intent: str, language: str = None, 
                           filters: Dict = None) -> str:
        search_parts = []
        
        if language:
            search_parts.append(f"language:{language}")
        
        if query:
            keywords = query.split()
            for keyword in keywords[:2]:
                search_parts.append(keyword)
        
        if intent == "solve_issues":
            search_parts.append("good-first-issues:>3")
        else:
            search_parts.append("stars:>50")
        
        if filters:
            if filters.get("min_stars"):
                search_parts.append(f"stars:>={filters['min_stars']}")
        
        final_query = " ".join(search_parts) if search_parts else "stars:>100"
        
        return final_query
    
    def _apply_intent_filters(self, repos: List[Dict], intent: str, 
                              custom_filters: Dict = None) -> List[Dict]:
        filtered = []
        
        for repo in repos:
            should_include = True
            
            if intent == "solve_issues":
                if repo.get("open_issues_count", 0) < 3:
                    should_include = False
            
            if custom_filters:
                if custom_filters.get("min_stars"):
                    if repo.get("stargazers_count", 0) < custom_filters["min_stars"]:
                        should_include = False
                
                if custom_filters.get("max_stars"):
                    if repo.get("stargazers_count", 0) > custom_filters["max_stars"]:
                        should_include = False
            
            if should_include:
                filtered.append(repo)
        
        return filtered
