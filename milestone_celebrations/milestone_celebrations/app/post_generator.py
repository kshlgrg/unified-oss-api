from typing import Dict

class PostGenerator:
    def generate_linkedin_post(self, milestone: Dict, username: str, repo: str = None) -> str:
        icon = milestone["icon"]
        title = milestone["title"]
        
        post = f"{icon} Celebrating @{username}'s achievement: {title}\n\n"
        post += f"Your contributions make our community stronger!\n\n"
        
        if repo:
            post += f"Repository: {repo}\n"
        
        post += f"#OpenSource #GitHub #Milestone"
        
        return post
    
    def generate_twitter_post(self, milestone: Dict, username: str, repo: str = None) -> str:
        icon = milestone["icon"]
        title = milestone["title"]
        
        post = f"{icon} @{username} just achieved: {title}\n\n"
        post += f"#OpenSource #GitHub"
        
        return post
    
    def generate_all_posts(self, milestone: Dict, username: str, repo: str = None) -> Dict:
        return {
            "linkedin": self.generate_linkedin_post(milestone, username, repo),
            "twitter": self.generate_twitter_post(milestone, username, repo)
        }
