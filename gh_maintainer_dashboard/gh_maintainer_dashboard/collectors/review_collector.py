from typing import List, Dict
from datetime import datetime
from gh_maintainer_dashboard.core.github_client import GitHubClient
from gh_maintainer_dashboard.models.activity import ReviewActivity, ActivityType


class ReviewCollector:
    def __init__(self, github_client: GitHubClient):
        self.client = github_client
    
    def collect_user_reviews(self, username: str) -> List[ReviewActivity]:
        reviews = []
        
        # Use GraphQL to get contribution data
        try:
            data = self.client.get_user_contributions_graphql(username)
            user = data.get('user', {})
            contribs = user.get('contributionsCollection', {})
            
            # For now, create placeholder reviews based on total count
            # In production, you'd query specific PR reviews
            total_reviews = contribs.get('totalPullRequestReviewContributions', 0)
            
            # Note: This is a simplified version
            # The full implementation would query specific reviews
            
        except Exception as e:
            print(f"GraphQL error, falling back to Events API: {e}")
            # Fall back to Events API
            events = self.client.get_user_events(username)
            for event in events:
                if event.get("type") == "PullRequestReviewEvent":
                    review_data = self._parse_review_event(event)
                    if review_data:
                        reviews.append(review_data)
        
        return reviews

    
    def _parse_review_event(self, event: Dict) -> ReviewActivity:
        payload = event.get("payload", {})
        review = payload.get("review", {})
        pr = payload.get("pull_request", {})
        repo = event.get("repo", {})
        
        return ReviewActivity(
            id=f"review_{event.get('id')}",
            type=ActivityType.REVIEW,
            repository=repo.get("name", "").split("/")[-1],
            repository_full_name=repo.get("name", ""),
            timestamp=datetime.fromisoformat(event.get("created_at", "").replace("Z", "+00:00")),
            title=pr.get("title", ""),
            url=pr.get("html_url", ""),
            pr_number=pr.get("number", 0),
            review_state=review.get("state", ""),
            comments_count=len(review.get("body", "")),
            requested_changes=review.get("state") == "changes_requested",
            metadata={
                "pr_url": pr.get("html_url"),
                "review_id": review.get("id"),
            }
        )
    
    def get_review_stats(self, username: str) -> Dict:
        reviews = self.collect_user_reviews(username)
        
        total_reviews = len(reviews)
        approved = sum(1 for r in reviews if r.review_state == "approved")
        changes_requested = sum(1 for r in reviews if r.requested_changes)
        
        return {
            "total_reviews": total_reviews,
            "approved": approved,
            "changes_requested": changes_requested,
            "approval_rate": approved / total_reviews if total_reviews > 0 else 0,
            "request_changes_rate": changes_requested / total_reviews if total_reviews > 0 else 0,
        }
