from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field
from enum import Enum


class ActivityType(str, Enum):
    REVIEW = "review"
    ISSUE_TRIAGE = "issue_triage"
    PR_COMMENT = "pr_comment"
    ISSUE_COMMENT = "issue_comment"
    COMMIT = "commit"
    MENTORSHIP = "mentorship"
    DOCUMENTATION = "documentation"
    CI_FIX = "ci_fix"
    DISCUSSION = "discussion"


class ActivityRecord(BaseModel):
    id: str
    type: ActivityType
    repository: str
    repository_full_name: str
    timestamp: datetime
    title: Optional[str] = None
    url: Optional[str] = None
    sentiment_score: Optional[float] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        use_enum_values = True


class ReviewActivity(ActivityRecord):
    pr_number: int
    review_state: str
    comments_count: int = 0
    requested_changes: bool = False


class IssueActivity(ActivityRecord):
    issue_number: int
    action: str
    labels_added: list = Field(default_factory=list)
    labels_removed: list = Field(default_factory=list)


class CommentActivity(ActivityRecord):
    target_number: int
    comment_body: str
    is_first_time_contributor: bool = False
    word_count: int = 0


class CommitActivity(ActivityRecord):
    sha: str
    message: str
    files_changed: int = 0
    additions: int = 0
    deletions: int = 0
