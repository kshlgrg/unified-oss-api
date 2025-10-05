import requests
from typing import Dict, List
from .config import Config

class GitHubClient:
    def __init__(self, token: str = None):
        self.token = token or Config.GITHUB_TOKEN
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }
    
    def get_user_prs(self, username: str, repo: str = None) -> List[Dict]:
        url = f"{self.base_url}/search/issues"
        query = f"author:{username} type:pr is:merged"
        if repo:
            query += f" repo:{repo}"
        
        params = {"q": query, "per_page": 100}
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json().get("items", [])
    
    def get_user_issues(self, username: str, repo: str = None) -> List[Dict]:
        url = f"{self.base_url}/search/issues"
        query = f"author:{username} type:issue"
        if repo:
            query += f" repo:{repo}"
        
        params = {"q": query, "per_page": 100}
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json().get("items", [])
    
    def get_repo_stats(self, repo: str) -> Dict:
        url = f"{self.base_url}/repos/{repo}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
