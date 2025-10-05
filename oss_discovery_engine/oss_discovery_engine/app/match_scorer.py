from typing import Dict, List
from .config import Config

class MatchScorer:
    def __init__(self):
        self.config = Config()
    
    def calculate_match_score(self, repo: Dict, user_profile: Dict, 
                              intent: str) -> Dict:
        weights = self.config.MATCH_WEIGHTS
        
        language_score = self._calculate_language_match(repo, user_profile)
        complexity_score = self._calculate_complexity_match(repo, user_profile)
        topic_score = self._calculate_topic_match(repo, user_profile)
        activity_score = self._calculate_activity_score(repo)
        intent_score = self._calculate_intent_score(repo, intent)
        
        total_score = (
            language_score * weights["language_match"] +
            complexity_score * weights["complexity_match"] +
            topic_score * weights["topic_match"] +
            activity_score * weights["activity_score"] +
            intent_score * weights["intent_score"]
        )
        
        match_reasons = self._generate_match_reasons(
            language_score, complexity_score, topic_score, 
            activity_score, intent_score, user_profile
        )
        
        return {
            "total_score": round(total_score, 2),
            "breakdown": {
                "language_match": round(language_score, 2),
                "complexity_match": round(complexity_score, 2),
                "topic_match": round(topic_score, 2),
                "activity_score": round(activity_score, 2),
                "intent_score": round(intent_score, 2)
            },
            "match_reasons": match_reasons
        }
    
    def _calculate_language_match(self, repo: Dict, user_profile: Dict) -> float:
        repo_language = repo.get("language", "").lower()
        user_languages = [lang.lower() for lang in user_profile["analyzed_skills"]["languages"].keys()]
        
        if repo_language in user_languages:
            index = user_languages.index(repo_language)
            return 1.0 - (index * 0.1)
        
        return 0.3
    
    def _calculate_complexity_match(self, repo: Dict, user_profile: Dict) -> float:
        skill_level = user_profile["analyzed_skills"]["skill_level"]
        stars = repo.get("stargazers_count", 0)
        
        if skill_level == "beginner":
            if 100 <= stars <= 5000:
                return 1.0
            elif stars < 100:
                return 0.7
            else:
                return 0.4
        elif skill_level == "intermediate":
            if 1000 <= stars <= 20000:
                return 1.0
            else:
                return 0.6
        else:
            return 0.8
    
    def _calculate_topic_match(self, repo: Dict, user_profile: Dict) -> float:
        repo_topics = [t.lower() for t in repo.get("topics", [])]
        user_topics = [t.lower() for t in user_profile["analyzed_skills"]["topics"]]
        
        if not repo_topics:
            return 0.5
        
        matches = len(set(repo_topics) & set(user_topics))
        
        return min(matches / 3, 1.0)
    
    def _calculate_activity_score(self, repo: Dict) -> float:
        open_issues = repo.get("open_issues_count", 0)
        has_license = repo.get("license") is not None
        
        score = 0.5
        
        if open_issues > 0:
            score += 0.3
        
        if has_license:
            score += 0.2
        
        return min(score, 1.0)
    
    def _calculate_intent_score(self, repo: Dict, intent: str) -> float:
        if intent == "solve_issues":
            open_issues = repo.get("open_issues_count", 0)
            return min(open_issues / 20, 1.0)
        elif intent == "fork_and_build":
            forks = repo.get("forks_count", 0)
            return min(forks / 100, 1.0)
        
        return 0.5
    
    def _generate_match_reasons(self, lang_score: float, comp_score: float, 
                                topic_score: float, activity_score: float, 
                                intent_score: float, user_profile: Dict) -> List[str]:
        reasons = []
        
        if lang_score >= 0.8:
            primary_lang = list(user_profile["analyzed_skills"]["languages"].keys())[0]
            reasons.append(f"✅ {primary_lang} expertise matches")
        
        if comp_score >= 0.8:
            reasons.append("✅ Complexity level matches skill")
        
        if topic_score >= 0.6:
            reasons.append("✅ Topics align with interests")
        
        if activity_score >= 0.7:
            reasons.append("✅ Active and well-maintained")
        
        if intent_score >= 0.7:
            reasons.append("✅ Good opportunities available")
        
        return reasons
