from .milestone_detector import MilestoneDetector
from .post_generator import PostGenerator
from .cli_formatter import CLIFormatter
from typing import Dict, List

class MilestoneCelebrations:
    def __init__(self, github_token: str = None):
        self.detector = MilestoneDetector(github_token)
        self.post_generator = PostGenerator()
        self.formatter = CLIFormatter()
    
    def get_milestone_sections(self, username: str, repos: List[str] = None) -> Dict:
        sections = {}
        
        personal_milestones = self.detector.detect_user_milestones(username)
        personal_upcoming = self.detector.predict_next_milestones(username)
        
        sections["Personal Achievements"] = {
            "type": "personal",
            "username": username,
            "milestones": personal_milestones,
            "upcoming": personal_upcoming
        }
        
        if repos:
            for repo in repos:
                repo_name = repo.split("/")[-1] if "/" in repo else repo
                
                user_in_repo = self.detector.detect_user_milestones(username, repo)
                upcoming_in_repo = self.detector.predict_next_milestones(username, repo)
                repo_milestones = self.detector.detect_repo_milestones(repo)
                
                sections[f"Repository: {repo_name}"] = {
                    "type": "repository",
                    "repo": repo,
                    "milestones": user_in_repo + repo_milestones,
                    "upcoming": upcoming_in_repo
                }
        
        return {
            "username": username,
            "sections": sections,
            "total_sections": len(sections)
        }
    
    def display_milestone_table(self, username: str, repos: List[str] = None) -> str:
        data = self.get_milestone_sections(username, repos)
        return self.formatter.format_milestones_table(data)

__all__ = ["MilestoneCelebrations"]
