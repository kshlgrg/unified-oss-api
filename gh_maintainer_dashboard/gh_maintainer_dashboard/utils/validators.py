import re
from typing import Optional


class Validators:
    @staticmethod
    def is_valid_github_username(username: str) -> bool:
        if not username:
            return False
        
        pattern = r'^[a-zA-Z0-9](?:[a-zA-Z0-9]|-(?=[a-zA-Z0-9])){0,38}$'
        return bool(re.match(pattern, username))
    
    @staticmethod
    def is_valid_repo_name(repo_name: str) -> bool:
        if not repo_name or "/" not in repo_name:
            return False
        
        parts = repo_name.split("/")
        if len(parts) != 2:
            return False
        
        owner, repo = parts
        return Validators.is_valid_github_username(owner) and len(repo) > 0
    
    @staticmethod
    def sanitize_username(username: str) -> str:
        return re.sub(r'[^a-zA-Z0-9-]', '', username)
    
    @staticmethod
    def validate_period(period: str) -> bool:
        pattern = r'^\d+[dwmy]$'
        return bool(re.match(pattern, period))
    
    @staticmethod
    def validate_limit(limit: int, min_val: int = 1, max_val: int = 100) -> bool:
        return min_val <= limit <= max_val
