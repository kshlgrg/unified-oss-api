from typing import Dict
from datetime import datetime
from gh_maintainer_dashboard.core.github_client import GitHubClient
from gh_maintainer_dashboard.collectors.review_collector import ReviewCollector
from gh_maintainer_dashboard.collectors.issue_collector import IssueCollector
from gh_maintainer_dashboard.collectors.comment_collector import CommentCollector
from gh_maintainer_dashboard.collectors.commit_collector import CommitCollector
from gh_maintainer_dashboard.collectors.repo_collector import RepoCollector
from gh_maintainer_dashboard.analyzers.sentiment_analyzer import SentimentAnalyzer
from gh_maintainer_dashboard.utils.metrics_calculator import MetricsCalculator
from gh_maintainer_dashboard.models.maintainer import MaintainerProfile, MaintainerInfo, SummaryStats


class ActivityAnalyzer:
    def __init__(self, github_client: GitHubClient):
        self.client = github_client
        self.review_collector = ReviewCollector(github_client)
        self.issue_collector = IssueCollector(github_client)
        self.comment_collector = CommentCollector(github_client)
        self.commit_collector = CommitCollector(github_client)
        self.repo_collector = RepoCollector(github_client)
        self.sentiment_analyzer = SentimentAnalyzer()
        self.metrics_calculator = MetricsCalculator()
    
    def get_full_profile(self, username: str) -> Dict:
        user_data = self.client.get_user(username)
        
        review_stats = self.review_collector.get_review_stats(username)
        issue_stats = self.issue_collector.get_issue_stats(username)
        comment_stats = self.comment_collector.get_comment_stats(username)
        commit_stats = self.commit_collector.get_commit_stats(username)
        
        reviews = self.review_collector.collect_user_reviews(username)
        comments = self.comment_collector.collect_user_comments(username)
        comment_texts = [c.comment_body for c in comments]
        
        sentiment = self.sentiment_analyzer.analyze_maintainer_sentiment(
            [r.dict() for r in reviews],
            comment_texts
        )
        
        repos = self.repo_collector.get_maintained_repos(username)
        
        activity_breakdown = self._calculate_activity_breakdown(
            review_stats, issue_stats, comment_stats, commit_stats
        )
        
        profile = MaintainerProfile(
            maintainer=MaintainerInfo(
                username=username,
                name=user_data.get("name"),
                avatar_url=user_data.get("avatar_url"),
                profile_url=user_data.get("html_url"),
                bio=user_data.get("bio"),
                location=user_data.get("location"),
                company=user_data.get("company"),
            ),
            summary_stats=SummaryStats(
                total_reviews=review_stats["total_reviews"],
                total_issues_triaged=issue_stats["total_issue_activities"],
                total_pr_comments=comment_stats["pr_comments"],
                total_issue_comments=comment_stats["issue_comments"],
                mentorship_interactions=comment_stats["mentorship_interactions"],
                documentation_contributions=commit_stats["documentation_commits"],
                ci_fixes=commit_stats["ci_fixes"],
                total_repos_maintained=len(repos),
            ),
            activity_breakdown=activity_breakdown,
            sentiment_analysis=sentiment,
            repositories_maintained=[r.dict() for r in repos],
        )
        
        return profile.dict()
    
    def _calculate_activity_breakdown(self, review_stats, issue_stats, comment_stats, commit_stats) -> Dict:
        total = (
            review_stats["total_reviews"] +
            issue_stats["total_issue_activities"] +
            comment_stats["total_comments"] +
            commit_stats["total_commits"]
        )
        
        if total == 0:
            return {}
        
        breakdown = {
            "code_reviews": {
                "count": review_stats["total_reviews"],
                "percentage": self.metrics_calculator.calculate_percentage(review_stats["total_reviews"], total),
                "additional_metrics": {
                    "approval_rate": review_stats["approval_rate"],
                    "request_changes_rate": review_stats["request_changes_rate"],
                }
            },
            "issue_management": {
                "count": issue_stats["total_issue_activities"],
                "percentage": self.metrics_calculator.calculate_percentage(issue_stats["total_issue_activities"], total),
                "additional_metrics": {
                    "opened": issue_stats["opened"],
                    "closed": issue_stats["closed"],
                }
            },
            "mentorship": {
                "count": comment_stats["mentorship_interactions"],
                "percentage": self.metrics_calculator.calculate_percentage(comment_stats["mentorship_interactions"], total),
                "additional_metrics": {
                    "avg_word_count": comment_stats["avg_word_count"],
                }
            },
            "documentation": {
                "count": commit_stats["documentation_commits"],
                "percentage": self.metrics_calculator.calculate_percentage(commit_stats["documentation_commits"], total),
            },
            "ci_devops": {
                "count": commit_stats["ci_fixes"],
                "percentage": self.metrics_calculator.calculate_percentage(commit_stats["ci_fixes"], total),
            },
            "community_support": {
                "count": comment_stats["total_comments"],
                "percentage": self.metrics_calculator.calculate_percentage(comment_stats["total_comments"], total),
            }
        }
        
        return breakdown
