import requests
from typing import Dict, List, Optional
from .config import Config

class GitHubClient:
    def __init__(self, token: str = None):
        self.token = token or Config.GITHUB_TOKEN
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }
    
    def get_user_profile(self, username: str) -> Dict:
        url = f"{self.base_url}/users/{username}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def get_user_repos(self, username: str) -> List[Dict]:
        url = f"{self.base_url}/users/{username}/repos"
        params = {"per_page": 100, "sort": "updated"}
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_user_events(self, username: str) -> List[Dict]:
        url = f"{self.base_url}/users/{username}/events"
        params = {"per_page": 100}
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()
    
    def search_repositories(self, query: str, language: str = None, 
                           sort: str = "stars", per_page: int = 30) -> List[Dict]:
        url = f"{self.base_url}/search/repositories"
        
        search_query = query
        if language:
            search_query += f" language:{language}"
        
        params = {
            "q": search_query,
            "sort": sort,
            "per_page": per_page
        }
        
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json().get("items", [])
    
    def get_repo_issues(self, repo: str, labels: str = None, state: str = "open") -> List[Dict]:
        url = f"{self.base_url}/repos/{repo}/issues"
        params = {"state": state, "per_page": 100}
        if labels:
            params["labels"] = labels
        
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_repo_details(self, repo: str) -> Dict:
        url = f"{self.base_url}/repos/{repo}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def get_repo_languages(self, repo: str) -> Dict:
        url = f"{self.base_url}/repos/{repo}/languages"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def get_repo_contributors(self, repo: str) -> List[Dict]:
        url = f"{self.base_url}/repos/{repo}/contributors"
        params = {"per_page": 30}
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_repo_commits(self, repo: str, since: str = None) -> List[Dict]:
        url = f"{self.base_url}/repos/{repo}/commits"
        params = {"per_page": 100}
        if since:
            params["since"] = since
        
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()
