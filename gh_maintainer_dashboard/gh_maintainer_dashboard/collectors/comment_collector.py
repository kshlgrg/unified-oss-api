from typing import List, Dict
from datetime import datetime
from gh_maintainer_dashboard.core.github_client import GitHubClient
from gh_maintainer_dashboard.models.activity import CommentActivity, ActivityType


class CommentCollector:
    def __init__(self, github_client: GitHubClient):
        self.client = github_client
    
    def collect_user_comments(self, username: str) -> List[CommentActivity]:
        comments = []
        events = self.client.get_user_events(username)
        
        for event in events:
            event_type = event.get("type")
            if event_type in ["IssueCommentEvent", "PullRequestReviewCommentEvent"]:
                comment_data = self._parse_comment_event(event)
                if comment_data:
                    comments.append(comment_data)
        
        return comments
    
    def _parse_comment_event(self, event: Dict) -> CommentActivity:
        payload = event.get("payload", {})
        comment = payload.get("comment", {})
        issue_or_pr = payload.get("issue") or payload.get("pull_request", {})
        repo = event.get("repo", {})
        
        body = comment.get("body", "")
        word_count = len(body.split())
        
        activity_type = ActivityType.PR_COMMENT if "PullRequest" in event.get("type") else ActivityType.ISSUE_COMMENT
        
        return CommentActivity(
            id=f"comment_{event.get('id')}",
            type=activity_type,
            repository=repo.get("name", "").split("/")[-1],
            repository_full_name=repo.get("name", ""),
            timestamp=datetime.fromisoformat(event.get("created_at", "").replace("Z", "+00:00")),
            title=issue_or_pr.get("title", ""),
            url=comment.get("html_url", ""),
            target_number=issue_or_pr.get("number", 0),
            comment_body=body,
            word_count=word_count,
            is_first_time_contributor=self._check_first_time_contributor(issue_or_pr),
            metadata={
                "comment_url": comment.get("html_url"),
                "comment_id": comment.get("id"),
            }
        )
    
    def _check_first_time_contributor(self, issue_or_pr: Dict) -> bool:
        author_association = issue_or_pr.get("author_association", "")
        return author_association in ["FIRST_TIME_CONTRIBUTOR", "FIRST_TIMER"]
    
    def get_comment_stats(self, username: str) -> Dict:
        comments = self.collect_user_comments(username)
        
        total_comments = len(comments)
        pr_comments = sum(1 for c in comments if c.type == ActivityType.PR_COMMENT)
        issue_comments = sum(1 for c in comments if c.type == ActivityType.ISSUE_COMMENT)
        mentorship_comments = sum(1 for c in comments if c.is_first_time_contributor)
        avg_word_count = sum(c.word_count for c in comments) / total_comments if total_comments > 0 else 0
        
        return {
            "total_comments": total_comments,
            "pr_comments": pr_comments,
            "issue_comments": issue_comments,
            "mentorship_interactions": mentorship_comments,
            "avg_word_count": round(avg_word_count, 2),
        }
