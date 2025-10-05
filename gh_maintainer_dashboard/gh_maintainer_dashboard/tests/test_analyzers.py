import pytest
from unittest.mock import Mock, MagicMock
from gh_maintainer_dashboard.analyzers.activity_analyzer import ActivityAnalyzer
from gh_maintainer_dashboard.analyzers.sentiment_analyzer import SentimentAnalyzer
from gh_maintainer_dashboard.core.github_client import GitHubClient


class TestSentimentAnalyzer:
    def setup_method(self):
        self.analyzer = SentimentAnalyzer()
    
    def test_analyze_positive_text(self):
        text = "Great work! This is an excellent contribution."
        result = self.analyzer.analyze_text(text)
        
        assert result["tone"] == "positive"
        assert result["sentiment_score"] > 0.5
    
    def test_analyze_negative_text(self):
        text = "This code is terrible and needs major refactoring."
        result = self.analyzer.analyze_text(text)
        
        assert result["tone"] == "negative"
        assert result["sentiment_score"] < 0.5
    
    def test_analyze_neutral_text(self):
        text = "Please update the documentation."
        result = self.analyzer.analyze_text(text)
        
        assert result["tone"] in ["neutral", "positive"]
    
    def test_analyze_comments_list(self):
        comments = [
            "Great work!",
            "Needs improvement.",
            "This looks good.",
        ]
        result = self.analyzer.analyze_comments(comments)
        
        assert "overall_tone" in result
        assert "sentiment_score" in result
        assert 0 <= result["sentiment_score"] <= 1


class TestActivityAnalyzer:
    def setup_method(self):
        self.mock_client = Mock(spec=GitHubClient)
        self.analyzer = ActivityAnalyzer(self.mock_client)
    
    def test_calculate_activity_breakdown(self):
        review_stats = {"total_reviews": 100, "approval_rate": 0.8, "request_changes_rate": 0.2}
        issue_stats = {"total_issue_activities": 50, "opened": 30, "closed": 20}
        comment_stats = {"total_comments": 200, "pr_comments": 120, "issue_comments": 80, "mentorship_interactions": 30, "avg_word_count": 50}
        commit_stats = {"total_commits": 150, "ci_fixes": 10, "documentation_commits": 20}
        
        breakdown = self.analyzer._calculate_activity_breakdown(
            review_stats, issue_stats, comment_stats, commit_stats
        )
        
        assert "code_reviews" in breakdown
        assert "issue_management" in breakdown
        assert breakdown["code_reviews"]["count"] == 100
        assert breakdown["issue_management"]["count"] == 50
