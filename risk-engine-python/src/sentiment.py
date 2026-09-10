import re

def analyze_sentiment(text):
    """
    Performs rule-based sentiment analysis on financial news headlines.
    
    Uses a targeted lexicon to classify text as Bullish, Bearish, or Neutral.
    Returns: Tuple (sentiment_label, status_emoji)
    """
    if not text or text == "No Title":
        return "Neutral", "⚪"
        
    text = text.lower()
    
    bullish_words = [
        'growth', 'surge', 'buy', 'upgrade', 'profit', 'beat', 'bullish', 
        'rally', 'positive', 'gain', 'jump', 'soar', 'expand', 'record high',
        'dividend', 'success', 'opportunity', 'strong'
    ]
    
    bearish_words = [
        'decline', 'drop', 'sell', 'downgrade', 'loss', 'miss', 'bearish', 
        'crash', 'negative', 'fall', 'slump', 'sink', 'contract', 'risk',
        'debt', 'inflation', 'recession', 'weak', 'plunge'
    ]
    
    bull_score = sum(1 for word in bullish_words if re.search(rf'\b{word}\b', text))
    bear_score = sum(1 for word in bearish_words if re.search(rf'\b{word}\b', text))
    
    if bull_score > bear_score:
        return "Bullish", "🟢"
    elif bear_score > bull_score:
        return "Bearish", "🔴"
    else:
        return "Neutral", "⚪"
