import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import OSSDiscoveryEngine
import json
from dotenv import load_dotenv

load_dotenv()

engine = OSSDiscoveryEngine(github_token=os.getenv("GITHUB_TOKEN"))

result = engine.discover_projects(
    username="torvalds",
    intent="solve_issues",
    query="",
    filters=None,
    limit=3
)

print(f"\nFound {len(result['recommended_projects'])} recommendations")

for p in result['recommended_projects']:
    print(f"  • {p['repo']['name']} (score: {p['match_score']})")

with open("test_report.json", "w") as f:
    json.dump(result, f, indent=2)

print("\n✅ Report saved!")