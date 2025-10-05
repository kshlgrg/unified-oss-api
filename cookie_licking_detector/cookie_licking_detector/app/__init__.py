from .claim_detector import ClaimDetector
from .user_profiler import UserProfiler
from .staleness_analyzer import StalenessAnalyzer
from .ai_analyzer import AIAnalyzer
from .message_generator import MessageGenerator
from typing import Dict, List
from datetime import datetime

class CookieLickingDetector:
    def __init__(self, github_token: str = None):
        self.claim_detector = ClaimDetector(github_token)
        self.user_profiler = UserProfiler(github_token)
        self.staleness_analyzer = StalenessAnalyzer()
        self.ai_analyzer = AIAnalyzer()
        self.message_generator = MessageGenerator()
    
    def analyze_repository(self, repo: str, limit: int = 20) -> Dict:
        scan_start = datetime.now()
        
        print(f"🍪 Scanning {repo} (limit: {limit} issues)...\n")
        
        claimed_issues = self.claim_detector.detect_claimed_issues(repo, limit=limit)
        
        all_issues_data = []
        summary_by_user = {}
        
        for idx, item in enumerate(claimed_issues, 1):
            print(f"[{idx}/{len(claimed_issues)}] Analyzing claimed issue...")
            
            issue = item["issue"]
            claim_info = item["claim_info"]
            
            claimed_by = claim_info["claimed_by"]
            
            user_profile = self.user_profiler.get_user_profile(claimed_by, repo)
            
            progress = self.claim_detector.get_issue_progress(repo, issue["number"], claimed_by)
            
            reliability_score = user_profile["reliability_metrics"]["reliability_score"]
            
            staleness = self.staleness_analyzer.analyze_staleness(claim_info, progress, reliability_score)
            
            ai_analysis = self.ai_analyzer.analyze_claim(issue, user_profile, staleness, progress)
            
            suggested_actions = self._generate_actions(ai_analysis, staleness)
            
            messages = self.message_generator.generate_messages(issue, user_profile, staleness, ai_analysis)
            
            issue_data = {
                "issue_id": f"issue_{issue['number']}",
                "issue_details": {
                    "number": issue["number"],
                    "title": issue["title"],
                    "url": issue["html_url"],
                    "state": issue["state"],
                    "labels": issue.get("labels", []),
                    "created_at": issue["created_at"],
                    "updated_at": issue["updated_at"],
                    "claimed_at": claim_info["claimed_at"],
                    "days_since_claim": staleness["days_stale"]
                },
                "claimant_details": user_profile,
                "reliability_metrics": user_profile["reliability_metrics"],
                "recent_activity_30d": user_profile["recent_activity_30d"],
                "past_performance": user_profile["past_performance"],
                "progress_tracking": progress,
                "staleness_analysis": staleness,
                "ai_analysis": ai_analysis,
                "suggested_actions": suggested_actions,
                "generated_messages": messages,
                "health_status": staleness["status"]
            }
            
            all_issues_data.append(issue_data)
            
            if claimed_by not in summary_by_user:
                summary_by_user[claimed_by] = {
                    "total_claimed": 0,
                    "critical": 0,
                    "healthy": 0,
                    "reliability_score": reliability_score
                }
            summary_by_user[claimed_by]["total_claimed"] += 1
            if staleness["status"] == "critical":
                summary_by_user[claimed_by]["critical"] += 1
            elif staleness["status"] == "healthy":
                summary_by_user[claimed_by]["healthy"] += 1
        
        scan_duration = (datetime.now() - scan_start).total_seconds()
        
        status_counts = {
            "healthy": len([i for i in all_issues_data if i["health_status"] == "healthy"]),
            "needs_monitoring": len([i for i in all_issues_data if i["health_status"] == "needs_monitoring"]),
            "needs_nudge": len([i for i in all_issues_data if i["health_status"] == "needs_nudge"]),
            "critical": len([i for i in all_issues_data if i["health_status"] == "critical"])
        }
        
        return {
            "scan_metadata": {
                "repository": repo,
                "scan_timestamp": scan_start.isoformat(),
                "scan_duration_seconds": round(scan_duration, 2)
            },
            "repository_stats": {
                "total_claimed_issues": len(all_issues_data),
                **status_counts
            },
            "all_claimed_issues": all_issues_data,
            "summary_by_user": summary_by_user,
            "recommendations_summary": {
                "immediate_action_required": status_counts["critical"],
                "monitor_closely": status_counts["needs_monitoring"]
            }
        }
    
    def _generate_actions(self, ai_analysis: Dict, staleness: Dict) -> List[Dict]:
        actions = []
        
        recommendation = ai_analysis["recommendation"]
        
        if recommendation == "send_urgent_nudge":
            actions.append({
                "action_id": "action_1",
                "priority": 1,
                "action_type": "send_urgent_nudge",
                "execute_when": "immediately",
                "message_tone": "polite_urgent"
            })
            actions.append({
                "action_id": "action_2",
                "priority": 2,
                "action_type": "auto_release",
                "execute_when": "if no response in 7 days"
            })
        elif recommendation == "send_nudge":
            actions.append({
                "action_id": "action_1",
                "priority": 1,
                "action_type": "send_nudge",
                "execute_when": "immediately"
            })
        else:
            actions.append({
                "action_id": "action_1",
                "priority": 1,
                "action_type": "monitor",
                "execute_when": "check in 7 days"
            })
        
        return actions

__all__ = ["CookieLickingDetector"]
