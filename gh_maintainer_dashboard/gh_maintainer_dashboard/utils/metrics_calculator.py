from typing import List, Dict
from collections import defaultdict
from datetime import datetime, timedelta


class MetricsCalculator:
    @staticmethod
    def calculate_percentage(part: int, total: int) -> float:
        if total == 0:
            return 0.0
        return round((part / total) * 100, 2)
    
    @staticmethod
    def calculate_average(values: List[float]) -> float:
        if not values:
            return 0.0
        return round(sum(values) / len(values), 2)
    
    @staticmethod
    def calculate_sentiment_score(positive: int, negative: int, neutral: int) -> float:
        total = positive + negative + neutral
        if total == 0:
            return 0.5
        return round((positive + (neutral * 0.5)) / total, 2)
    
    @staticmethod
    def calculate_activity_breakdown(activities: Dict[str, int]) -> Dict[str, Dict]:
        total = sum(activities.values())
        breakdown = {}
        
        for activity_type, count in activities.items():
            breakdown[activity_type] = {
                "count": count,
                "percentage": MetricsCalculator.calculate_percentage(count, total)
            }
        
        return breakdown
    
    @staticmethod
    def calculate_trend(data_points: List[float]) -> str:
        if len(data_points) < 2:
            return "stable"
        
        first_half = sum(data_points[:len(data_points)//2])
        second_half = sum(data_points[len(data_points)//2:])
        
        if second_half > first_half * 1.1:
            return "increasing"
        elif second_half < first_half * 0.9:
            return "decreasing"
        return "stable"
    
    @staticmethod
    def group_by_date(activities: List[Dict], date_key: str = "timestamp") -> Dict[str, List]:
        grouped = defaultdict(list)
        for activity in activities:
            date = activity.get(date_key, "")
            if isinstance(date, datetime):
                date = date.strftime("%Y-%m-%d")
            elif isinstance(date, str):
                date = date.split("T")[0]
            grouped[date].append(activity)
        return dict(grouped)
    
    @staticmethod
    def calculate_response_time(created_at: datetime, responded_at: datetime) -> float:
        if not created_at or not responded_at:
            return 0.0
        delta = responded_at - created_at
        return round(delta.total_seconds() / 3600, 2)
    
    @staticmethod
    def calculate_health_score(metrics: Dict) -> float:
        score = 0.0
        
        activity_score = min(metrics.get("total_activities", 0) / 100, 1.0) * 0.3
        response_score = max(0, 1 - (metrics.get("avg_response_hours", 24) / 48)) * 0.3
        resolution_score = max(0, 1 - (metrics.get("avg_resolution_days", 7) / 14)) * 0.2
        engagement_score = min(metrics.get("contributors", 0) / 50, 1.0) * 0.2
        
        score = activity_score + response_score + resolution_score + engagement_score
        return round(score, 2)
