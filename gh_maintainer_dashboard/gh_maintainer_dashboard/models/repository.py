from typing import List, Optional, Dict
from datetime import datetime
from pydantic import BaseModel, Field


class RepositoryLanguages(BaseModel):
    primary: Optional[str] = None
    all_languages: List[str] = Field(default_factory=list)


class RepositoryTopics(BaseModel):
    topics: List[str] = Field(default_factory=list)


class MaintainerActivity(BaseModel):
    reviews_conducted: int = 0
    issues_triaged: int = 0
    pr_comments: int = 0
    issue_comments: int = 0
    mentorship_interactions: int = 0
    documentation_updates: int = 0
    ci_fixes: int = 0
    time_percentage: float = 0.0
    avg_weekly_hours: float = 0.0


class HealthMetrics(BaseModel):
    health_score: float = 0.0
    contributor_growth: float = 0.0
    avg_issue_resolution_days: float = 0.0
    pr_merge_rate: float = 0.0
    community_engagement: str = "unknown"


class RecentActivity(BaseModel):
    last_review: Optional[datetime] = None
    last_issue_triage: Optional[datetime] = None
    last_commit: Optional[datetime] = None


class RepositoryData(BaseModel):
    name: str
    full_name: str
    url: str
    description: Optional[str] = None
    role: str = "contributor"
    stars: int = 0
    forks: int = 0
    open_issues: int = 0
    languages: List[str] = Field(default_factory=list)
    topics: List[str] = Field(default_factory=list)
    maintainer_activity: MaintainerActivity = Field(default_factory=MaintainerActivity)
    health_metrics: HealthMetrics = Field(default_factory=HealthMetrics)
    recent_activity: RecentActivity = Field(default_factory=RecentActivity)


class RepositorySummary(BaseModel):
    total_repos: int = 0
    most_active_repo: Optional[str] = None
    total_time_invested_hours_monthly: float = 0.0
    repos_by_language: Dict[str, int] = Field(default_factory=dict)
