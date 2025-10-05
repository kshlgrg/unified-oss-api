import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import OSSDiscoveryEngine
import json
from dotenv import load_dotenv

load_dotenv()

engine = OSSDiscoveryEngine(github_token=os.getenv("GITHUB_TOKEN"))

username = "kshlgrg"  # Replace with your username
intent = "solve_issues"
query = "Python"
filters = {
    "min_stars": 100
}

print(f"Discovering projects for @{username}...")

result = engine.discover_projects(
    username=username,
    intent=intent,
    query=query,
    filters=filters,
    limit=5
)

print(f"{'='*80}")
print(f"  📊 DISCOVERY RESULTS")
print(f"{'='*80}\n")

print(f"User: @{result['user_profile']['username']}")
print(f"Skill Level: {result['user_profile']['analyzed_skills']['skill_level']}")
print(f"Primary Languages: {list(result['user_profile']['analyzed_skills']['languages'].keys())[:3]}")
print(f"AI Confidence: {result['ai_predictions']['confidence']}")

print(f"\n{'='*80}")
print(f"  🎯 TOP RECOMMENDATIONS")
print(f"{'='*80}\n")

for project in result["recommended_projects"]:
    print(f"#{project['rank']} {project['repo']['name']}")
    print(f"   Match Score: {project['match_score']}")
    print(f"   ⭐ {project['repo']['stars']} | 🍴 {project['repo']['forks']} | 🐛 {project['repo']['open_issues']} issues")
    print(f"   Language: {project['repo']['language']}")
    print(f"   {project['why_recommended']}")
    
    if project['recommended_issues']:
        print(f"   📋 Suggested Issues:")
        for issue in project['recommended_issues'][:2]:
            print(f"      • #{issue['number']}: {issue['title'][:50]}...")
    
    print()

print(f"{'='*80}")
print(f"  💾 SAVING FULL REPORT")
print(f"{'='*80}\n")

with open("discovery_report.json", "w") as f:
    json.dump(result, f, indent=2)

print("✅ Full report saved to: discovery_report.json\n")
