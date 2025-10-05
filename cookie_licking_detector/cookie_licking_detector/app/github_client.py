import requests
from typing import Dict, List, Optional
from datetime import datetime
from .config import Config

class GitHubClient:
    def __init__(self, token: str = None):
        self.token = token or Config.GITHUB_TOKEN
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }
    
    def get_repo_issues(self, repo: str, state: str = "open") -> List[Dict]:
        url = f"{self.base_url}/repos/{repo}/issues"
        params = {"state": state, "per_page": 100}
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_issue_comments(self, repo: str, issue_number: int) -> List[Dict]:
        url = f"{self.base_url}/repos/{repo}/issues/{issue_number}/comments"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def get_issue_events(self, repo: str, issue_number: int) -> List[Dict]:
        url = f"{self.base_url}/repos/{repo}/issues/{issue_number}/events"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def get_user_info(self, username: str) -> Dict:
        url = f"{self.base_url}/users/{username}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def get_user_repos(self, username: str) -> List[Dict]:
        url = f"{self.base_url}/users/{username}/repos"
        params = {"per_page": 100}
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_user_events(self, username: str) -> List[Dict]:
        url = f"{self.base_url}/users/{username}/events"
        params = {"per_page": 100}
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()
    
    def search_issues(self, query: str) -> List[Dict]:
        url = f"{self.base_url}/search/issues"
        params = {"q": query, "per_page": 100}
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json().get("items", [])
    
    def get_pull_requests(self, repo: str, state: str = "open") -> List[Dict]:
        url = f"{self.base_url}/repos/{repo}/pulls"
        params = {"state": state, "per_page": 100}
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_commits(self, repo: str, author: str = None) -> List[Dict]:
        url = f"{self.base_url}/repos/{repo}/commits"
        params = {"per_page": 100}
        if author:
            params["author"] = author
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()
