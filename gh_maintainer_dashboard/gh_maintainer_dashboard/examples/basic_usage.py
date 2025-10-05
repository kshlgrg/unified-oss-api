"""
Basic usage example for gh-maintainer-dashboard
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
    
    print(f"Fetching maintainer profile for {username}...")
    profile = dashboard.get_profile(username)
    
    print("\n" + "="*50)
    print(f"Maintainer: {profile['maintainer']['name']} (@{profile['maintainer']['username']})")
    print("="*50)
    
    print("\nSummary Statistics:")
    stats = profile['summary_stats']
    print(f"  Total Reviews: {stats['total_reviews']}")
    print(f"  Issues Triaged: {stats['total_issues_triaged']}")
    print(f"  PR Comments: {stats['total_pr_comments']}")
    print(f"  Issue Comments: {stats['total_issue_comments']}")
    print(f"  Mentorship Interactions: {stats['mentorship_interactions']}")
    print(f"  Documentation Contributions: {stats['documentation_contributions']}")
    print(f"  CI Fixes: {stats['ci_fixes']}")
    print(f"  Repos Maintained: {stats['total_repos_maintained']}")
    
    print("\nSentiment Analysis:")
    sentiment = profile['sentiment_analysis']
    print(f"  Overall Tone: {sentiment['overall_tone']}")
    print(f"  Sentiment Score: {sentiment['sentiment_score']}")
    print(f"  Maintainer Temperature: {sentiment['maintainer_temperature']}")
    print(f"  Review Strictness: {sentiment['review_strictness']}")
    
    print("\nActivity Breakdown:")
    for activity_type, data in profile['activity_breakdown'].items():
        print(f"  {activity_type.replace('_', ' ').title()}: {data['count']} ({data['percentage']}%)")
    
    print("\n" + "="*50)


if __name__ == "__main__":
    main()
