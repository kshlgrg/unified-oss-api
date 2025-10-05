from typing import List, Dict, Optional
from pydantic import BaseModel, Field


class MaintainerInfo(BaseModel):
    name: str
    username: str
    title: str = "Open Source Maintainer"
    email: Optional[str] = None
    github_url: str
    location: Optional[str] = None


class ProfessionalSummary(BaseModel):
    total_reviews: int = 0
    total_maintenance_work: int = 0
    repos_maintained: int = 0
    contributors_mentored: int = 0
    years_maintaining: float = 0.0
    summary_text: str = ""


class InvisibleLaborItem(BaseModel):
    category: str
    count: int
    percentage: float


class KeyRepository(BaseModel):
    name: str
    role: str
    duration: str
    contributions: str
    impact: str


class CVData(BaseModel):
    maintainer_info: MaintainerInfo
    professional_summary: ProfessionalSummary
    invisible_labor_breakdown: List[InvisibleLaborItem] = Field(default_factory=list)
    key_repositories: List[KeyRepository] = Field(default_factory=list)
    achievements: List[str] = Field(default_factory=list)
    skills_demonstrated: List[str] = Field(default_factory=list)
    social_share_text: str = ""
    export_formats: Dict[str, str] = Field(default_factory=dict)
