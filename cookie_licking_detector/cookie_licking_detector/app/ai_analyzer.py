from typing import Dict, List
import numpy as np

class AIAnalyzer:
    def __init__(self):
        pass
    
    def analyze_claim(self, issue: Dict, user_profile: Dict, staleness: Dict, progress: Dict) -> Dict:
        risk_score = self._calculate_risk_score(staleness, user_profile, progress, issue)
        
        recommendation = self._generate_recommendation(risk_score, staleness, progress)
        
        reasoning = self._generate_reasoning(issue, user_profile, staleness, progress, risk_score)
        
        sentiment = self._analyze_sentiment(progress.get("user_comments", []))
        
        completion_prob = self._predict_completion_probability(user_profile, staleness, progress)
        
        return {
            "model_used": "lightweight_risk_scorer_v1",
            "recommendation": recommendation["action"],
            "confidence": recommendation["confidence"],
            "risk_score": round(risk_score, 2),
            "priority": recommendation["priority"],
            "reasoning": reasoning,
            "sentiment_analysis": sentiment,
            "predicted_completion_probability": round(completion_prob, 2),
            "predicted_days_to_complete": self._estimate_days_to_complete(user_profile, staleness)
        }
    
    def _calculate_risk_score(self, staleness: Dict, user_profile: Dict, progress: Dict, issue: Dict) -> float:
        staleness_score = staleness["staleness_score"]
        
        reliability = user_profile.get("reliability_metrics", {}).get("reliability_score", 0.5)
        reliability_risk = 1 - reliability
        
        activity = user_profile.get("recent_activity_30d", {})
        activity_score = min((activity.get("commits", 0) + activity.get("prs_opened", 0) * 5) / 50, 1.0)
        activity_risk = 1 - activity_score
        
        has_progress = progress.get("has_commits") or progress.get("has_linked_pr")
        progress_risk = 0.0 if has_progress else 0.3
        
        priority_risk = 0.2 if any(label in ["high-priority", "security", "critical"] 
                                   for label in [l.get("name", "") for l in issue.get("labels", [])]) else 0.0
        
        risk_score = (
            staleness_score * 0.35 +
            reliability_risk * 0.25 +
            activity_risk * 0.2 +
            progress_risk * 0.15 +
            priority_risk * 0.05
        )
        
        return min(risk_score, 1.0)
    
    def _generate_recommendation(self, risk_score: float, staleness: Dict, progress: Dict) -> Dict:
        if risk_score >= 0.85:
            return {
                "action": "send_urgent_nudge",
                "confidence": 0.9,
                "priority": "high"
            }
        elif risk_score >= 0.7:
            return {
                "action": "send_nudge",
                "confidence": 0.8,
                "priority": "medium"
            }
        elif risk_score >= 0.5:
            return {
                "action": "monitor_closely",
                "confidence": 0.7,
                "priority": "low"
            }
        else:
            return {
                "action": "continue_monitoring",
                "confidence": 0.6,
                "priority": "low"
            }
    
    def _generate_reasoning(self, issue: Dict, user_profile: Dict, staleness: Dict, 
                           progress: Dict, risk_score: float) -> List[str]:
        reasoning = []
        
        days_stale = staleness["days_stale"]
        avg_completion = user_profile.get("reliability_metrics", {}).get("avg_completion_days", 14)
        
        if days_stale > avg_completion:
            reasoning.append(f"Issue claimed {days_stale} days ago (exceeds typical {avg_completion}-day completion)")
        
        if staleness["days_inactive"] > 7:
            reasoning.append(f"No activity for {staleness['days_inactive']} days")
        
        reliability = user_profile.get("reliability_metrics", {})
        completion_rate = reliability.get("completion_rate", 0)
        if completion_rate < 0.7:
            reasoning.append(f"User has moderate reliability ({int(completion_rate*100)}% completion rate)")
        
        if not progress.get("has_commits") and not progress.get("has_linked_pr"):
            reasoning.append("No commits or PRs linked to this issue")
        
        labels = [l.get("name", "") for l in issue.get("labels", [])]
        priority_labels = ["high-priority", "security", "critical"]
        if any(label in priority_labels for label in labels):
            reasoning.append("High-priority issue needs attention")
        
        if progress.get("user_comments"):
            last_comment = progress["user_comments"][-1].get("body", "")[:100]
            reasoning.append(f"Last comment: '{last_comment}'")
        
        return reasoning
    
    def _analyze_sentiment(self, comments: List[Dict]) -> Dict:
        if not comments:
            return {
                "last_comment_sentiment": "neutral",
                "sentiment_score": 0.5,
                "commitment_level": "unknown",
                "likely_to_complete": 0.5
            }
        
        last_comment = comments[-1].get("body", "").lower()
        
        positive_words = ["will", "working", "progress", "soon", "almost", "testing", "done"]
        negative_words = ["busy", "can't", "sorry", "blocked", "stuck", "help"]
        
        positive_count = sum(1 for word in positive_words if word in last_comment)
        negative_count = sum(1 for word in negative_words if word in last_comment)
        
        sentiment_score = (positive_count - negative_count + 5) / 10
        sentiment_score = max(0, min(1, sentiment_score))
        
        if sentiment_score > 0.6:
            sentiment = "positive"
            commitment = "high"
        elif sentiment_score > 0.4:
            sentiment = "neutral"
            commitment = "moderate"
        else:
            sentiment = "negative"
            commitment = "low"
        
        return {
            "last_comment_sentiment": sentiment,
            "sentiment_score": round(sentiment_score, 2),
            "commitment_level": commitment,
            "likely_to_complete": round(sentiment_score, 2)
        }
    
    def _predict_completion_probability(self, user_profile: Dict, staleness: Dict, progress: Dict) -> float:
        reliability = user_profile.get("reliability_metrics", {}).get("completion_rate", 0.5)
        
        has_progress = 1.0 if (progress.get("has_commits") or progress.get("has_linked_pr")) else 0.3
        
        activity = user_profile.get("recent_activity_30d", {})
        is_active = 1.0 if activity.get("commits", 0) > 10 else 0.5
        
        staleness_penalty = 1 - (staleness["staleness_score"] * 0.5)
        
        probability = (reliability * 0.4 + has_progress * 0.3 + is_active * 0.2 + staleness_penalty * 0.1)
        
        return max(0, min(1, probability))
    
    def _estimate_days_to_complete(self, user_profile: Dict, staleness: Dict) -> int:
        avg_days = user_profile.get("reliability_metrics", {}).get("avg_completion_days", 14)
        days_already = staleness["days_stale"]
        
        estimated_remaining = max(avg_days - days_already, 3)
        
        return estimated_remaining
