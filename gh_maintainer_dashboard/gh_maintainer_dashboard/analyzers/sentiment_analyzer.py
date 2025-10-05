from typing import List, Dict
from textblob import TextBlob


class SentimentAnalyzer:
    def __init__(self):
        pass
    
    def analyze_text(self, text: str) -> Dict:
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        
        if polarity > 0.1:
            tone = "positive"
        elif polarity < -0.1:
            tone = "negative"
        else:
            tone = "neutral"
        
        return {
            "polarity": round(polarity, 2),
            "tone": tone,
            "sentiment_score": round((polarity + 1) / 2, 2),
        }
    
    def analyze_comments(self, comments: List[str]) -> Dict:
        if not comments:
            return {
                "overall_tone": "neutral",
                "sentiment_score": 0.5,
                "positivity_rate": 0.5,
            }
        
        sentiments = [self.analyze_text(comment) for comment in comments]
        
        positive_count = sum(1 for s in sentiments if s["tone"] == "positive")
        negative_count = sum(1 for s in sentiments if s["tone"] == "negative")
        neutral_count = sum(1 for s in sentiments if s["tone"] == "neutral")
        
        avg_sentiment = sum(s["sentiment_score"] for s in sentiments) / len(sentiments)
        
        if avg_sentiment > 0.6:
            overall_tone = "positive"
        elif avg_sentiment < 0.4:
            overall_tone = "negative"
        else:
            overall_tone = "neutral"
        
        return {
            "overall_tone": overall_tone,
            "sentiment_score": round(avg_sentiment, 2),
            "positivity_rate": round(positive_count / len(comments), 2),
            "positive_count": positive_count,
            "negative_count": negative_count,
            "neutral_count": neutral_count,
        }
    
    def calculate_maintainer_temperature(self, review_stats: Dict) -> Dict:
        request_changes_rate = review_stats.get("request_changes_rate", 0)
        approval_rate = review_stats.get("approval_rate", 0)
        
        strictness = request_changes_rate
        
        if strictness > 0.3:
            temperature = "strict"
        elif strictness < 0.1:
            temperature = "lenient"
        else:
            temperature = "balanced"
        
        return {
            "maintainer_temperature": temperature,
            "review_strictness": round(strictness, 2),
        }
    
    def analyze_maintainer_sentiment(self, reviews: List[Dict], comments: List[str]) -> Dict:
        comment_sentiment = self.analyze_comments(comments)
        
        review_stats = {
            "request_changes_rate": sum(1 for r in reviews if r.get("requested_changes")) / len(reviews) if reviews else 0,
            "approval_rate": sum(1 for r in reviews if r.get("review_state") == "approved") / len(reviews) if reviews else 0,
        }
        
        temperature = self.calculate_maintainer_temperature(review_stats)
        
        return {
            "overall_tone": comment_sentiment["overall_tone"],
            "sentiment_score": comment_sentiment["sentiment_score"],
            "maintainer_temperature": temperature["maintainer_temperature"],
            "review_strictness": temperature["review_strictness"],
            "positivity_rate": comment_sentiment["positivity_rate"],
            "recent_trend": "stable",
        }
