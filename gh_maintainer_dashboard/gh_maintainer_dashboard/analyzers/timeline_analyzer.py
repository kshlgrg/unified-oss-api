from typing import Dict, List
from datetime import datetime
from gh_maintainer_dashboard.core.github_client import GitHubClient
from gh_maintainer_dashboard.collectors.review_collector import ReviewCollector
from gh_maintainer_dashboard.collectors.issue_collector import IssueCollector
from gh_maintainer_dashboard.collectors.comment_collector import CommentCollector
from gh_maintainer_dashboard.utils.date_helpers import DateHelpers
from gh_maintainer_dashboard.utils.metrics_calculator import MetricsCalculator
from gh_maintainer_dashboard.models.metrics import DailyMetrics


class TimelineAnalyzer:
    def __init__(self, github_client: GitHubClient):
        self.client = github_client
        self.review_collector = ReviewCollector(github_client)
        self.issue_collector = IssueCollector(github_client)
        self.comment_collector = CommentCollector(github_client)
        self.date_helpers = DateHelpers()
        self.metrics_calculator = MetricsCalculator()
    
    def get_activity_timeline(self, username: str, period: str = "30d") -> Dict:
        start_date, end_date = self.date_helpers.get_date_range(period)
        
        reviews = self.review_collector.collect_user_reviews(username)
        issues = self.issue_collector.collect_user_issue_activities(username)
        comments = self.comment_collector.collect_user_comments(username)
        
        all_activities = reviews + issues + comments
        
        activities_by_date = self.metrics_calculator.group_by_date(
            [a.dict() for a in all_activities]
        )
        
        date_list = self.date_helpers.generate_date_list(start_date, end_date)
        timeline = []
        
        for date in date_list:
            date_activities = activities_by_date.get(date, [])
            
            daily_metrics = DailyMetrics(
                date=date,
                reviews=sum(1 for a in date_activities if a.get("type") == "review"),
                issues=sum(1 for a in date_activities if a.get("type") == "issue_triage"),
                comments=sum(1 for a in date_activities if a.get("type") in ["pr_comment", "issue_comment"]),
                mentorship=sum(1 for a in date_activities if a.get("is_first_time_contributor")),
            )
            daily_metrics.total = (
                daily_metrics.reviews +
                daily_metrics.issues +
                daily_metrics.comments +
                daily_metrics.mentorship
            )
            
            timeline.append(daily_metrics.dict())
        
        aggregates = self._calculate_aggregates(timeline)
        trends = self._calculate_trends(timeline)
        
        return {
            "timeline": timeline,
            "aggregates": aggregates,
            "trends": trends,
        }
    
    def _calculate_aggregates(self, timeline: List[Dict]) -> Dict:
        total_activities = [day["total"] for day in timeline]
        
        daily_avg = self.metrics_calculator.calculate_average(total_activities)
        weekly_avg = daily_avg * 7
        
        peak_day_data = max(timeline, key=lambda d: d["total"])
        quietest_day_data = min(timeline, key=lambda d: d["total"])
        
        weekend_activities = sum(
            day["total"] for day in timeline
            if self.date_helpers.is_weekend(self.date_helpers.parse_date(day["date"]))
        )
        total = sum(total_activities)
        weekend_percentage = (weekend_activities / total * 100) if total > 0 else 0
        
        return {
            "daily_average": round(daily_avg, 2),
            "weekly_average": round(weekly_avg, 2),
            "peak_day": peak_day_data["date"],
            "peak_activity": peak_day_data["total"],
            "quietest_day": quietest_day_data["date"],
            "weekend_percentage": round(weekend_percentage, 2),
        }
    
    def _calculate_trends(self, timeline: List[Dict]) -> Dict:
        total_activities = [day["total"] for day in timeline]
        
        trend_direction = self.metrics_calculator.calculate_trend(total_activities)
        
        first_half = total_activities[:len(total_activities)//2]
        second_half = total_activities[len(total_activities)//2:]
        
        avg_first = self.metrics_calculator.calculate_average(first_half)
        avg_second = self.metrics_calculator.calculate_average(second_half)
        
        change_percentage = ((avg_second - avg_first) / avg_first * 100) if avg_first > 0 else 0
        
        consistency_score = self._calculate_consistency(total_activities)
        
        return {
            "direction": trend_direction,
            "change_percentage": round(change_percentage, 2),
            "consistency_score": consistency_score,
        }
    
    def _calculate_consistency(self, activities: List[float]) -> float:
        if len(activities) < 2:
            return 1.0
        
        avg = self.metrics_calculator.calculate_average(activities)
        if avg == 0:
            return 0.0
        
        variance = sum((x - avg) ** 2 for x in activities) / len(activities)
        std_dev = variance ** 0.5
        
        coefficient_of_variation = std_dev / avg
        consistency = max(0, 1 - coefficient_of_variation)
        
        return round(consistency, 2)
