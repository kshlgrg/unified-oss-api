from .profile_analyzer import ProfileAnalyzer
from .ai_predictor import AIPredictor
from .repo_searcher import RepoSearcher
from .match_scorer import MatchScorer
from .health_analyzer import HealthAnalyzer
from .github_client import GitHubClient
from typing import Dict, List

class OSSDiscoveryEngine:
    def __init__(self, github_token: str = None):
        self.profile_analyzer = ProfileAnalyzer(github_token)
        self.ai_predictor = AIPredictor()
        self.repo_searcher = RepoSearcher(github_token)
        self.match_scorer = MatchScorer()
        self.health_analyzer = HealthAnalyzer(github_token)
        self.github_client = GitHubClient(github_token)
    
    def discover_projects(self, username: str, intent: str = "solve_issues", 
                         query: str = "", filters: Dict = None, limit: int = 10) -> Dict:
        print(f"\n{'='*80}")
        print(f"  🔍 OSS DISCOVERY ENGINE")
        print(f"{'='*80}\n")
        
        user_profile = self.profile_analyzer.analyze_user_profile(username)
        
        print("Predicting capabilities with AI...")
        ai_predictions = self.ai_predictor.predict_capabilities(user_profile)
        
        repos = self.repo_searcher.search_repos(user_profile, intent, query, filters)
        
        print(f"Scoring and ranking {len(repos)} repositories...\n")
        
        scored_repos = []
        
        for idx, repo in enumerate(repos[:limit], 1):
            print(f"  [{idx}/{min(limit, len(repos))}] Analyzing {repo['full_name']}...")
            
            match_result = self.match_scorer.calculate_match_score(repo, user_profile, intent)
            
            health_metrics = self.health_analyzer.analyze_repo_health(repo["full_name"])
            
            recommended_issues = []
            if intent == "solve_issues":
                recommended_issues = self._get_recommended_issues(repo["full_name"], user_profile)
            
            scored_repos.append({
                "repo": repo,
                "match_score": match_result["total_score"],
                "match_breakdown": match_result["breakdown"],
                "match_reasons": match_result["match_reasons"],
                "health_metrics": health_metrics,
                "recommended_issues": recommended_issues
            })
        
        scored_repos.sort(key=lambda x: x["match_score"], reverse=True)
        
        print(f"\n✅ Analysis complete!\n")
        
        return {
            "user_profile": user_profile,
            "ai_predictions": ai_predictions,
            "search_intent": {
                "type": intent,
                "query": query,
                "filters_applied": filters or {}
            },
            "recommended_projects": self._format_recommendations(scored_repos[:limit]),
            "summary": {
                "total_repos_analyzed": len(repos),
                "top_matches": len(scored_repos[:limit]),
                "recommendation_confidence": ai_predictions["confidence"]
            }
        }
    
    def _get_recommended_issues(self, repo_full_name: str, user_profile: Dict, limit: int = 3) -> List[Dict]:
        try:
            issues = self.github_client.get_repo_issues(
                repo_full_name, 
                labels="good first issue",
                state="open"
            )
            
            recommended = []
            
            for issue in issues[:limit]:
                recommended.append({
                    "number": issue["number"],
                    "title": issue["title"],
                    "url": issue["html_url"],
                    "labels": [label["name"] for label in issue.get("labels", [])],
                    "created_at": issue["created_at"]
                })
            
            return recommended
        except:
            return []
    
    def _format_recommendations(self, scored_repos: List[Dict]) -> List[Dict]:
        formatted = []
        
        for idx, item in enumerate(scored_repos, 1):
            repo = item["repo"]
            
            formatted.append({
                "rank": idx,
                "match_score": item["match_score"],
                "repo": {
                    "name": repo["full_name"],
                    "url": repo["html_url"],
                    "description": repo.get("description", "No description"),
                    "stars": repo["stargazers_count"],
                    "forks": repo["forks_count"],
                    "language": repo.get("language", "Unknown"),
                    "topics": repo.get("topics", []),
                    "open_issues": repo["open_issues_count"],
                    "last_updated": repo["updated_at"],
                    "license": repo.get("license", {}).get("name", "No license")
                },
                "match_reasons": item["match_reasons"],
                "health_metrics": item["health_metrics"],
                "recommended_issues": item["recommended_issues"],
                "why_recommended": self._generate_recommendation_text(item)
            })
        
        return formatted
    
    def _generate_recommendation_text(self, item: Dict) -> str:
        repo = item["repo"]
        reasons = item["match_reasons"]
        
        text = f"Great match for your skills! "
        
        if len(reasons) > 0:
            text += " ".join(reasons[:2])
        
        if item["recommended_issues"]:
            text += f" {len(item['recommended_issues'])} good first issues available."
        
        return text

__all__ = ["OSSDiscoveryEngine"]
