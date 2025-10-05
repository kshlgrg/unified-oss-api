from app import MilestoneCelebrations
import os
from dotenv import load_dotenv

load_dotenv()

mc = MilestoneCelebrations(github_token=os.getenv("GITHUB_TOKEN"))

username = "torvalds"
repos = ["torvalds/linux"]

print("\n" + "🎉"*40)
print("  MILESTONE CELEBRATIONS - CLI DASHBOARD")
print("🎉"*40)

output = mc.display_milestone_table(username, repos)
print(output)

print("\n" + "="*80)
