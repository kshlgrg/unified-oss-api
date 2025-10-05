import requests
from typing import Dict, List, Optional, Any
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

from gh_maintainer_dashboard.core.config import Config
from gh_maintainer_dashboard.core.cache import CacheManager, cached
from gh_maintainer_dashboard.core.rate_limiter import RateLimiter


class GitHubClient:
    def __init__(self, config: Config):
        self.config = config
        self.cache = CacheManager(ttl=config.cache_ttl)
        self.rate_limiter = RateLimiter(max_calls=config.api_rate_limit)
        
        self.headers = {
            "Authorization": f"Bearer {config.github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        transport = RequestsHTTPTransport(
            url=config.github_graphql_url,
            headers=self.headers,
            use_json=True,
        )
        self.graphql_client = Client(transport=transport, fetch_schema_from_transport=True)
    
    def _make_rest_request(self, endpoint: str, params: Optional[Dict] = None) -> Any:
        self.rate_limiter.wait_if_needed()
        url = f"{self.config.github_api_url}/{endpoint}"
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()
    
    def _make_graphql_request(self, query: str, variables: Optional[Dict] = None) -> Any:
        self.rate_limiter.wait_if_needed()
        return self.graphql_client.execute(gql(query), variable_values=variables)
    
    @cached(ttl=1800)
    def get_user(self, username: str) -> Dict:
        return self._make_rest_request(f"users/{username}")
    
    @cached(ttl=1800)
    def get_user_repos(self, username: str) -> List[Dict]:
        repos = []
        page = 1
        while True:
            batch = self._make_rest_request(f"users/{username}/repos", params={"page": page, "per_page": 100})
            if not batch:
                break
            repos.extend(batch)
            page += 1
        return repos
    
    @cached(ttl=900)
    def get_user_events(self, username: str) -> List[Dict]:
        events = []
        page = 1
        while page <= 3:
            batch = self._make_rest_request(f"users/{username}/events", params={"page": page, "per_page": 100})
            if not batch:
                break
            events.extend(batch)
            page += 1
        return events
    
    @cached(ttl=1800)
    def get_repo_info(self, owner: str, repo: str) -> Dict:
        return self._make_rest_request(f"repos/{owner}/{repo}")
    
    def get_pull_request_reviews(self, owner: str, repo: str, pr_number: int) -> List[Dict]:
        return self._make_rest_request(f"repos/{owner}/{repo}/pulls/{pr_number}/reviews")
    
    def get_issue_comments(self, owner: str, repo: str, issue_number: int) -> List[Dict]:
        return self._make_rest_request(f"repos/{owner}/{repo}/issues/{issue_number}/comments")
    
    def get_user_contributions_graphql(self, username: str) -> Dict:
        query = """
        query($login: String!) {
          user(login: $login) {
            login
            name
            avatarUrl
            bio
            location
            company
            contributionsCollection {
              totalCommitContributions
              totalIssueContributions
              totalPullRequestContributions
              totalPullRequestReviewContributions
              contributionCalendar {
                totalContributions
              }
            }
            repositories(first: 100, ownerAffiliations: [OWNER, COLLABORATOR, ORGANIZATION_MEMBER]) {
              nodes {
                name
                nameWithOwner
                description
                stargazerCount
                forkCount
                primaryLanguage {
                  name
                }
                repositoryTopics(first: 10) {
                  nodes {
                    topic {
                      name
                    }
                  }
                }
              }
            }
          }
        }
        """
        return self._make_graphql_request(query, {"login": username})
