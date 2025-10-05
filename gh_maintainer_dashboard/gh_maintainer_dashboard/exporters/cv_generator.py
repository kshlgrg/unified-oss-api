from typing import Dict
from gh_maintainer_dashboard.core.github_client import GitHubClient
from gh_maintainer_dashboard.analyzers.activity_analyzer import ActivityAnalyzer
from gh_maintainer_dashboard.models.cv import CVData, MaintainerInfo, ProfessionalSummary, InvisibleLaborItem, KeyRepository


class CVGenerator:
    def __init__(self, github_client: GitHubClient):
        self.client = github_client
        self.activity_analyzer = ActivityAnalyzer(github_client)
    
    def generate_cv(self, username: str, format: str = "json") -> Dict:
        profile = self.activity_analyzer.get_full_profile(username)
        
        cv_data = self._build_cv_data(profile)
        
        if format == "json":
            return cv_data.dict()
        elif format == "markdown":
            from gh_maintainer_dashboard.exporters.markdown_exporter import MarkdownExporter
            exporter = MarkdownExporter()
            return {"content": exporter.export_cv(cv_data)}
        elif format == "linkedin":
            from gh_maintainer_dashboard.exporters.social_exporter import SocialExporter
            exporter = SocialExporter()
            return {"content": exporter.generate_linkedin_text(cv_data)}
        else:
            return cv_data.dict()
    
    def _build_cv_data(self, profile: Dict) -> CVData:
        maintainer = profile["maintainer"]
        summary_stats = profile["summary_stats"]
        activity_breakdown = profile["activity_breakdown"]
        
        maintainer_info = MaintainerInfo(
            name=maintainer.get("name", maintainer["username"]),
            username=maintainer["username"],
            title="Open Source Maintainer",
            github_url=maintainer["profile_url"],
            location=maintainer.get("location"),
        )
        
        total_work = (
            summary_stats["total_reviews"] +
            summary_stats["total_issues_triaged"] +
            summary_stats["total_pr_comments"] +
            summary_stats["total_issue_comments"]
        )
        
        professional_summary = ProfessionalSummary(
            total_reviews=summary_stats["total_reviews"],
            total_maintenance_work=total_work,
            repos_maintained=summary_stats["total_repos_maintained"],
            contributors_mentored=summary_stats["mentorship_interactions"],
            years_maintaining=2.5,
            summary_text=f"Experienced open source maintainer with {summary_stats['total_repos_maintained']} repositories maintained. "
                        f"Conducted {summary_stats['total_reviews']}+ code reviews, mentored {summary_stats['mentorship_interactions']} contributors, "
                        f"and actively engaged in community support.",
        )
        
        invisible_labor = [
            InvisibleLaborItem(
                category=key.replace("_", " ").title(),
                count=value["count"],
                percentage=value["percentage"]
            )
            for key, value in activity_breakdown.items()
        ]
        
        achievements = [
            f"Conducted {summary_stats['total_reviews']}+ code reviews",
            f"Mentored {summary_stats['mentorship_interactions']} contributors",
            f"Managed {summary_stats['total_issues_triaged']} issues",
            f"Maintained {summary_stats['total_repos_maintained']} repositories",
        ]
        
        skills = [
            "Code Review & Quality Assurance",
            "Community Management",
            "Technical Mentorship",
            "Documentation",
            "Issue Triage & Project Management",
        ]
        
        social_share = (
            f"🎉 Celebrating my open source journey! {summary_stats['total_reviews']}+ code reviews, "
            f"{summary_stats['mentorship_interactions']} contributors mentored, and "
            f"{summary_stats['total_repos_maintained']} repos maintained. "
            f"Check out my maintainer profile at {maintainer['profile_url']} #OpenSource #Maintainer"
        )
        
        cv_data = CVData(
            maintainer_info=maintainer_info,
            professional_summary=professional_summary,
            invisible_labor_breakdown=invisible_labor,
            key_repositories=[],
            achievements=achievements,
            skills_demonstrated=skills,
            social_share_text=social_share,
            export_formats={
                "markdown": f"/api/maintainer/{maintainer['username']}/cv?format=markdown",
                "json": f"/api/maintainer/{maintainer['username']}/cv?format=json",
                "linkedin_text": f"/api/maintainer/{maintainer['username']}/cv?format=linkedin",
            }
        )
        
        return cv_data
