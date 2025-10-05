from typing import Dict, List
import numpy as np

class AIPredictor:
    def __init__(self):
        pass
    
    def predict_capabilities(self, user_profile: Dict) -> Dict:
        skills = user_profile["analyzed_skills"]
        stats = user_profile["github_stats"]
        
        skill_level = skills["skill_level"]
        total_contributions = stats["total_contributions"]
        
        complexity_handling = self._calculate_complexity_handling(skill_level, total_contributions)
        
        contribution_types = self._predict_contribution_types(skills["contribution_style"], stats)
        
        best_fit_topics = self._predict_best_topics(skills["topics"], skills["languages"])
        
        confidence = self._calculate_prediction_confidence(total_contributions)
        
        return {
            "can_handle_complexity": complexity_handling,
            "suggested_contribution_types": contribution_types,
            "best_fit_topics": best_fit_topics,
            "confidence": round(confidence, 2),
            "skill_assessment": {
                "level": skill_level,
                "strengths": self._identify_strengths(user_profile),
                "recommended_growth_areas": self._suggest_growth_areas(skill_level)
            }
        }
    
    def _calculate_complexity_handling(self, skill_level: str, contributions: int) -> Dict:
        base_scores = {
            "beginner": {"beginner": 0.95, "intermediate": 0.40, "advanced": 0.10},
            "intermediate": {"beginner": 1.0, "intermediate": 0.75, "advanced": 0.40},
            "advanced": {"beginner": 1.0, "intermediate": 0.95, "advanced": 0.80}
        }
        
        scores = base_scores.get(skill_level, base_scores["intermediate"])
        
        contribution_boost = min(contributions / 200, 0.15)
        
        return {
            level: round(min(score + contribution_boost, 1.0), 2)
            for level, score in scores.items()
        }
    
    def _predict_contribution_types(self, style: str, stats: Dict) -> List[str]:
        style_mapping = {
            "issue_solver": ["bug_fixes", "issue_resolution", "documentation"],
            "feature_builder": ["new_features", "enhancements", "refactoring"],
            "issue_reporter": ["bug_reporting", "feature_requests", "testing"]
        }
        
        base_types = style_mapping.get(style, ["bug_fixes", "documentation"])
        
        if stats["reviews"] > 5:
            base_types.append("code_review")
        
        return base_types
    
    def _predict_best_topics(self, topics: List[str], languages: Dict) -> List[str]:
        topic_categories = {
            "backend": ["api", "backend", "server", "database"],
            "frontend": ["frontend", "ui", "react", "vue", "angular"],
            "devops": ["docker", "kubernetes", "ci-cd", "deployment"],
            "ml": ["machine-learning", "ai", "data-science", "ml"],
            "web": ["web", "web-development", "webapp"]
        }
        
        best_topics = []
        
        for category, keywords in topic_categories.items():
            if any(keyword in topic.lower() for topic in topics for keyword in keywords):
                best_topics.append(category)
        
        if "Python" in languages:
            best_topics.extend(["backend", "ml", "automation"])
        if "JavaScript" in languages or "TypeScript" in languages:
            best_topics.extend(["frontend", "web"])
        
        return list(set(best_topics))[:5]
    
    def _calculate_prediction_confidence(self, contributions: int) -> float:
        if contributions >= 100:
            return 0.90
        elif contributions >= 50:
            return 0.80
        elif contributions >= 20:
            return 0.70
        else:
            return 0.60
    
    def _identify_strengths(self, profile: Dict) -> List[str]:
        strengths = []
        
        stats = profile["github_stats"]
        skills = profile["analyzed_skills"]
        
        if stats["prs"] > 10:
            strengths.append("Strong PR contribution history")
        
        if stats["reviews"] > 5:
            strengths.append("Code review experience")
        
        if len(skills["languages"]) >= 3:
            strengths.append("Multi-language proficiency")
        
        if stats["total_contributions"] > 50:
            strengths.append("Consistent contributor")
        
        return strengths
    
    def _suggest_growth_areas(self, skill_level: str) -> List[str]:
        suggestions = {
            "beginner": [
                "Start with documentation improvements",
                "Focus on good first issues",
                "Learn project contribution workflows"
            ],
            "intermediate": [
                "Tackle medium complexity issues",
                "Contribute new features",
                "Review others' pull requests"
            ],
            "advanced": [
                "Lead feature development",
                "Mentor new contributors",
                "Contribute to architecture discussions"
            ]
        }
        
        return suggestions.get(skill_level, suggestions["intermediate"])
