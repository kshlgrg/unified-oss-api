import pytest
from unittest.mock import Mock
from datetime import datetime
from gh_maintainer_dashboard.collectors.review_collector import ReviewCollector
from gh_maintainer_dashboard.collectors.issue_collector import IssueCollector
from gh_maintainer_dashboard.core.github_client import GitHubClient


class TestReviewCollector:
    def setup_method(self):
        self.mock_client = Mock(spec=GitHubClient)
        self.collector = ReviewCollector(self.mock_client)
    
    def test_collect_user_reviews(self):
        mock_events = [
            {
                "id": "123",
                "type": "PullRequestReviewEvent",
                "created_at": "2025-10-01T10:00:00Z",
                "repo": {"name": "owner/repo"},
                "payload": {
                    "review": {"id": 1, "state": "approved", "body": "LGTM"},
                    "pull_request": {"number": 42, "title": "Fix bug", "html_url": "https://github.com/owner/repo/pull/42"}
                }
            }
        ]
        
        self.mock_client.get_user_events.return_value = mock_events
        
        reviews = self.collector.collect_user_reviews("testuser")
        
        assert len(reviews) > 0
        assert reviews[0].pr_number == 42
        assert reviews[0].review_state == "approved"


class TestIssueCollector:
    def setup_method(self):
        self.mock_client = Mock(spec=GitHubClient)
        self.collector = IssueCollector(self.mock_client)
    
    def test_collect_user_issue_activities(self):
        mock_events = [
            {
                "id": "456",
                "type": "IssuesEvent",
                "created_at": "2025-10-01T11:00:00Z",
                "repo": {"name": "owner/repo"},
                "payload": {
                    "action": "opened",
                    "issue": {
                        "number": 10,
                        "title": "Bug report",
                        "html_url": "https://github.com/owner/repo/issues/10",
                        "state": "open",
                        "labels": []
                    }
                }
            }
        ]
        
        self.mock_client.get_user_events.return_value = mock_events
        
        activities = self.collector.collect_user_issue_activities("testuser")
        
        assert len(activities) > 0
        assert activities[0].issue_number == 10
        assert activities[0].action == "opened"
