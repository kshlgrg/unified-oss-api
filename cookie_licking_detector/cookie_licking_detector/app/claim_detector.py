from typing import Dict, List, Optional
from datetime import datetime
from .github_client import GitHubClient
from .config import Config

class ClaimDetector:
    def __init__(self, github_token: str = None):
        self.client = GitHubClient(github_token)
        self.config = Config()
    
    def detect_claimed_issues(self, repo: str, limit: int = 20) -> List[Dict]:
        claimed_issues = []
        
        issues = self.client.get_repo_issues(repo, state="open")
        
        print(f"Found {len(issues)} open issues. Processing first {limit}...")
        
        for idx, issue in enumerate(issues[:limit], 1):
            if issue.get("pull_request"):
                continue
            
            print(f"  [{idx}/{limit}] Checking issue #{issue['number']}...", end=" ")
            
            claim_info = self._detect_claim(repo, issue)
            if claim_info:
                print(f"✓ Claimed by @{claim_info['claimed_by']}")
                claimed_issues.append({
                    "issue": issue,
                    "claim_info": claim_info
                })
            else:
                print("✗ Not claimed")
        
        print(f"\nFound {len(claimed_issues)} claimed issues.\n")
        return claimed_issues
    
    def _detect_claim(self, repo: str, issue: Dict) -> Optional[Dict]:
        assignees = issue.get("assignees", [])
        if assignees:
            return {
                "claimed_by": assignees[0]["login"],
                "claimed_at": issue.get("updated_at"),
                "claim_method": "assigned"
            }
        
        comments = self.client.get_issue_comments(repo, issue["number"])
        
        for comment in comments:
            comment_body = comment.get("body", "").lower()
            
            for keyword in self.config.CLAIM_KEYWORDS:
                if keyword in comment_body:
                    return {
                        "claimed_by": comment["user"]["login"],
                        "claimed_at": comment["created_at"],
                        "claim_method": "comment",
                        "claim_comment": comment_body[:200]
                    }
        
        return None
    
    def get_issue_progress(self, repo: str, issue_number: int, claimed_by: str) -> Dict:
        prs = self.client.get_pull_requests(repo, state="all")
        linked_prs = [pr for pr in prs if f"#{issue_number}" in pr.get("body", "") or 
                      pr.get("user", {}).get("login") == claimed_by]
        
        commits = self.client.get_commits(repo, author=claimed_by)
        issue_commits = [c for c in commits if f"#{issue_number}" in c["commit"]["message"]]
        
        comments = self.client.get_issue_comments(repo, issue_number)
        user_comments = [c for c in comments if c["user"]["login"] == claimed_by]
        
        last_activity = None
        if user_comments:
            last_activity = user_comments[-1]["created_at"]
        elif issue_commits:
            last_activity = issue_commits[-1]["commit"]["committer"]["date"]
        
        return {
            "has_linked_pr": len(linked_prs) > 0,
            "linked_prs": linked_prs,
            "has_commits": len(issue_commits) > 0,
            "commits": issue_commits,
            "commit_count": len(issue_commits),
            "user_comments": user_comments,
            "comment_count": len(user_comments),
            "last_activity": last_activity
        }
