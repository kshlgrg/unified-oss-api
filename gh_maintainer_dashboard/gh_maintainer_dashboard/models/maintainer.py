from typing import List, Optional, Dict
from datetime import datetime
from pydantic import BaseModel, Field


class MaintainerInfo(BaseModel):
    username: str
    name: Optional[str] = None
    avatar_url: Optional[str] = None
    profile_url: str
    bio: Optional[str] = None
    location: Optional[str] = None
    company: Optional[str] = None


class SummaryStats(BaseModel):
    total_reviews: int = 0
    total_issues_triaged: int = 0
    total_pr_comments: int = 0
    total_issue_comments: int = 0
    mentorship_interactions: int = 0
    documentation_contributions: int = 0
    ci_fixes: int = 0
    total_repos_maintained: int = 0


class ActivityBreakdownItem(BaseModel):
    count: int = 0
    percentage: float = 0.0
    additional_metrics: Dict = Field(default_factory=dict)


class ActivityBreakdown(BaseModel):
    code_reviews: ActivityBreakdownItem = Field(default_factory=ActivityBreakdownItem)
    issue_management: ActivityBreakdownItem = Field(default_factory=ActivityBreakdownItem)
    mentorship: ActivityBreakdownItem = Field(default_factory=ActivityBreakdownItem)
    documentation: ActivityBreakdownItem = Field(default_factory=ActivityBreakdownItem)
    ci_devops: ActivityBreakdownItem = Field(default_factory=ActivityBreakdownItem)
    community_support: ActivityBreakdownItem = Field(default_factory=ActivityBreakdownItem)


class SentimentAnalysis(BaseModel):
    overall_tone: str = "neutral"
    sentiment_score: float = 0.5
    maintainer_temperature: str = "balanced"
    review_strictness: float = 0.5
    positivity_rate: float = 0.5
    recent_trend: str = "stable"


class TimeSeriesDataPoint(BaseModel):
    date: str
    reviews: int = 0
    issues: int = 0
    comments: int = 0
    mentorship: int = 0
    total_activity: int = 0


class TimeSeriesData(BaseModel):
    last_30_days: List[TimeSeriesDataPoint] = Field(default_factory=list)
    weekly_average: Dict[str, float] = Field(default_factory=dict)


class Milestone(BaseModel):
    id: str
    type: str
    title: str
    description: str
    achieved_at: datetime
    badge_icon: str
    shareable: bool = True


class ResponseMetrics(BaseModel):
    avg_first_response_hours: float = 0.0
    avg_issue_resolution_days: float = 0.0
    weekend_activity_percentage: float = 0.0
    most_active_hours: List[int] = Field(default_factory=list)


class MaintainerProfile(BaseModel):
    maintainer: MaintainerInfo
    summary_stats: SummaryStats = Field(default_factory=SummaryStats)
    activity_breakdown: ActivityBreakdown = Field(default_factory=ActivityBreakdown)
    sentiment_analysis: SentimentAnalysis = Field(default_factory=SentimentAnalysis)
    repositories_maintained: List[Dict] = Field(default_factory=list)
    time_series: TimeSeriesData = Field(default_factory=TimeSeriesData)
    milestones_achieved: List[Milestone] = Field(default_factory=list)
    similar_maintainers: List[Dict] = Field(default_factory=list)
    response_metrics: ResponseMetrics = Field(default_factory=ResponseMetrics)
    cv_export_url: Optional[str] = None
    last_updated: datetime = Field(default_factory=datetime.now)
