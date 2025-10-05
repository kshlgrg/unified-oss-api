from typing import Dict, List
from pydantic import BaseModel, Field


class DailyMetrics(BaseModel):
    date: str
    reviews: int = 0
    issues: int = 0
    comments: int = 0
    commits: int = 0
    mentorship: int = 0
    total: int = 0


class WeeklyMetrics(BaseModel):
    week_start: str
    total_activities: int = 0
    avg_daily_activities: float = 0.0
    peak_day: str = ""
    activities_by_type: Dict[str, int] = Field(default_factory=dict)


class MonthlyMetrics(BaseModel):
    month: str
    total_activities: int = 0
    avg_weekly_activities: float = 0.0
    most_active_repo: str = ""
    activities_by_type: Dict[str, int] = Field(default_factory=dict)


class MetricsData(BaseModel):
    daily_metrics: List[DailyMetrics] = Field(default_factory=list)
    weekly_metrics: List[WeeklyMetrics] = Field(default_factory=list)
    monthly_metrics: List[MonthlyMetrics] = Field(default_factory=list)
    overall_trends: Dict[str, float] = Field(default_factory=dict)
