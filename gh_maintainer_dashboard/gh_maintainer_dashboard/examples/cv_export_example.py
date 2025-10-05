"""
CV export example for gh-maintainer-dashboard
"""

from gh_maintainer_dashboard import MaintainerDashboard
import os
from dotenv import load_dotenv

load_dotenv()


def main():
    github_token = os.getenv("GITHUB_TOKEN")
    
    if not github_token:
        print("Error: GITHUB_TOKEN not found in environment variables")
        return
    
    dashboard = MaintainerDashboard(github_token=github_token)
    
    username = "octocat"
    
    print(f"Generating CV for {username}...\n")
    
    print("="*50)
    print("JSON Format:")
    print("="*50)
    cv_json = dashboard.export_cv(username, format="json")
    print(f"Name: {cv_json['cv_data']['maintainer_info']['name']}")
    print(f"Total Reviews: {cv_json['cv_data']['professional_summary']['total_reviews']}")
    print(f"Repos Maintained: {cv_json['cv_data']['professional_summary']['repos_maintained']}")
    
    print("\n" + "="*50)
    print("Markdown Format:")
    print("="*50)
    cv_markdown = dashboard.export_cv(username, format="markdown")
    print(cv_markdown['content'])
    
    print("\n" + "="*50)
    print("LinkedIn Format:")
    print("="*50)
    cv_linkedin = dashboard.export_cv(username, format="linkedin")
    print(cv_linkedin['content'])
    
    print("\n" + "="*50)
    print("Social Share Text:")
    print("="*50)
    print(cv_json['cv_data']['social_share_text'])


if __name__ == "__main__":
    main()
