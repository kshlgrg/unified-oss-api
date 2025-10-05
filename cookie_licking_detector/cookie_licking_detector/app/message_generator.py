from typing import Dict

class MessageGenerator:
    def generate_messages(self, issue: Dict, user: Dict, staleness: Dict, 
                         ai_analysis: Dict) -> Dict:
        username = user["username"]
        issue_number = issue["number"]
        issue_title = issue["title"]
        days_stale = staleness["days_stale"]
        
        urgent_nudge = self._generate_urgent_nudge(username, issue_number, issue_title, days_stale, issue)
        help_offer = self._generate_help_offer(username, issue_number)
        auto_release = self._generate_auto_release(username, issue_number)
        
        return {
            "urgent_nudge": {
                "subject": f"Re: Issue #{issue_number} - Status Check",
                "body": urgent_nudge,
                "tags": ["urgent", "status-check"]
            },
            "help_offer": {
                "subject": f"Re: Issue #{issue_number} - Need Help?",
                "body": help_offer,
                "tags": ["help", "support"]
            },
            "auto_release_warning": {
                "subject": f"Re: Issue #{issue_number} - Auto-release Notice",
                "body": auto_release,
                "tags": ["warning", "auto-release"]
            }
        }
    
    def _generate_urgent_nudge(self, username: str, issue_num: int, title: str, 
                               days: int, issue: Dict) -> str:
        labels = [l.get("name", "") for l in issue.get("labels", [])]
        is_priority = any(label in ["high-priority", "security", "critical"] for label in labels)
        
        message = f"Hey @{username}! 👋\n\n"
        message += f"It's been {days} days since you claimed #{issue_num} ({title}). "
        
        if is_priority:
            message += f"This is a high-priority issue. "
        
        message += f"Are you still working on this? Need any help?\n\n"
        message += f"If you're busy, no problem - just let us know so we can keep things moving! 🚀"
        
        return message
    
    def _generate_help_offer(self, username: str, issue_num: int) -> str:
        message = f"Hi @{username}! We haven't heard back about #{issue_num}. "
        message += f"Is there anything blocking you? We're here to help!\n\n"
        message += f"We can:\n"
        message += f"• Pair with you on this\n"
        message += f"• Assign someone to help\n"
        message += f"• Clarify requirements\n\n"
        message += f"Just let us know! 💪"
        
        return message
    
    def _generate_auto_release(self, username: str, issue_num: int) -> str:
        message = f"Hi @{username},\n\n"
        message += f"Just a heads up - if we don't hear back about #{issue_num} in the next 7 days, "
        message += f"we'll unassign it to keep the queue moving.\n\n"
        message += f"If you're still on it, just drop a quick comment! "
        message += f"We're here to help if you need it. 💪"
        
        return message
