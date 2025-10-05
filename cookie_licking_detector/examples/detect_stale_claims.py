import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import CookieLickingDetector
import json
from dotenv import load_dotenv

load_dotenv()

detector = CookieLickingDetector(github_token=os.getenv("GITHUB_TOKEN"))

repo = "microsoft/vscode"

print(f"\n{'='*80}")
print(f"  🍪 COOKIE-LICKING DETECTOR")
print(f"{'='*80}\n")

result = detector.analyze_repository(repo, limit=5)

print(f"\n{'='*80}")
print(f"  📊 RESULTS")
print(f"{'='*80}\n")

stats = result["repository_stats"]
print(f"Claimed Issues Found: {stats['total_claimed_issues']}")

if stats['total_claimed_issues'] > 0:
    print(f"  ✅ Healthy: {stats['healthy']}")
    print(f"  🟡 Needs Monitoring: {stats['needs_monitoring']}")
    print(f"  🟠 Needs Nudge: {stats['needs_nudge']}")
    print(f"  🔴 Critical: {stats['critical']}")
    
    with open("report.json", "w") as f:
        json.dump(result, f, indent=2)
    
    print(f"\n✅ Full report saved to report.json")
else:
    print("No claimed issues in first 5 issues.")

print(f"\n{'='*80}\n")
