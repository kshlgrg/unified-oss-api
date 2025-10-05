import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


class Config:
    def __init__(self, github_token: Optional[str] = None):
        self.github_token = github_token or os.getenv("GITHUB_TOKEN")
        if not self.github_token:
            raise ValueError("GitHub token is required. Set GITHUB_TOKEN environment variable or pass it to Config.")
        
        self.redis_host = os.getenv("REDIS_HOST", "localhost")
        self.redis_port = int(os.getenv("REDIS_PORT", "6379"))
        self.redis_db = int(os.getenv("REDIS_DB", "0"))
        self.cache_ttl = int(os.getenv("CACHE_TTL", "3600"))
        self.api_rate_limit = int(os.getenv("API_RATE_LIMIT", "5000"))
        
        self.github_api_url = "https://api.github.com"
        self.github_graphql_url = "https://api.github.com/graphql"
