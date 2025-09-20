# enhanced_sentiment.py
import pandas as pd
import numpy as np
import requests
from textblob import TextBlob
import yfinance as yf
from datetime import datetime, timedelta
import re
import time

class EnhancedSentimentAnalyzer:
    def __init__(self):
        self.news_sources = {
            'newsapi': 'https://newsapi.org/v2/everything',
            'reddit': 'https://www.reddit.com/r/IndiaInvestments/search.json'
        }
    
    def get_stock_news(self, symbol, days_back=7):
        """Get recent news for a stock from multiple free sources"""
        news_items = []
        
        # Try NewsAPI (free tier: 100 requests/day)
        try:
            news_items.extend(self.get_newsapi_data(symbol, days_back))
        except Exception as e:
            print(f"NewsAPI error: {e}")
        
        # Try Reddit (no API key needed)
        try:
            news_items.extend(self.get_reddit_data(symbol, days_back))
        except Exception as e:
            print(f"Reddit error: {e}")
        
        return news_items
    
    def get_newsapi_data(self, symbol, days_back):
        """Get news from NewsAPI (requires free API key)"""
        # Note: User needs to set NEWSAPI_KEY environment variable
        import os
        api_key = os.getenv('NEWSAPI_KEY')
        
        if not api_key:
            return []
        
        from_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
        
        params = {
            'q': f'{symbol} OR "{symbol} stock" OR "{symbol} share"',
            'from': from_date,
            'sortBy': 'publishedAt',
            'language': 'en',
            'apiKey': api_key
        }
        
        response = requests.get(self.news_sources['newsapi'], params=params)
        if response.status_code == 200:
            articles = response.json().get('articles', [])
            return [{'title': article['title'], 'description': article['description'], 
                    'source': 'NewsAPI', 'publishedAt': article['publishedAt']} 
                   for article in articles if article['title'] and article['description']]
        
        return []
    
    def get_reddit_data(self, symbol, days_back):
        """Get Reddit posts (no API key needed)"""
        try:
            url = f"https://www.reddit.com/r/IndiaInvestments/search.json?q={symbol}&sort=new&limit=10"
            headers = {'User-Agent': 'StockAnalyzer/1.0'}
            
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                posts = []
                
                for post in data.get('data', {}).get('children', []):
                    post_data = post['data']
                    posts.append({
                        'title': post_data['title'],
                        'description': post_data.get('selftext', '')[:200],
                        'source': 'Reddit',
                        'publishedAt': datetime.fromtimestamp(post_data['created_utc']).isoformat()
                    })
                
                return posts
        except Exception as e:
            print(f"Reddit API error: {e}")
        
        return []
    
    def analyze_sentiment_textblob(self, text):
        """Analyze sentiment using TextBlob (free, no API key needed)"""
        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity  # -1 to 1
            subjectivity = blob.sentiment.subjectivity  # 0 to 1
            
            # Convert to categorical
            if polarity > 0.1:
                sentiment = 'positive'
            elif polarity < -0.1:
                sentiment = 'negative'
            else:
                sentiment = 'neutral'
            
            return {
                'sentiment': sentiment,
                'polarity': polarity,
                'subjectivity': subjectivity,
                'confidence': abs(polarity)
            }
        except Exception as e:
            return {'sentiment': 'neutral', 'polarity': 0, 'subjectivity': 0, 'confidence': 0}
    
    def analyze_sentiment_vader(self, text):
        """Analyze sentiment using VADER (free, good for social media)"""
        try:
            from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
            analyzer = SentimentIntensityAnalyzer()
            
            scores = analyzer.polarity_scores(text)
            
            # Determine overall sentiment
            if scores['compound'] >= 0.05:
                sentiment = 'positive'
            elif scores['compound'] <= -0.05:
                sentiment = 'negative'
            else:
                sentiment = 'neutral'
            
            return {
                'sentiment': sentiment,
                'compound': scores['compound'],
                'positive': scores['pos'],
                'negative': scores['neg'],
                'neutral': scores['neu']
            }
        except ImportError:
            # Fallback to TextBlob if VADER not installed
            return self.analyze_sentiment_textblob(text)
    
    def get_comprehensive_sentiment(self, symbol):
        """Get comprehensive sentiment analysis for a stock"""
        news_items = self.get_stock_news(symbol)
        
        if not news_items:
            return {
                'overall_sentiment': 'neutral',
                'sentiment_score': 0,
                'news_count': 0,
                'sentiment_breakdown': {'positive': 0, 'negative': 0, 'neutral': 0}
            }
        
        sentiments = []
        sentiment_breakdown = {'positive': 0, 'negative': 0, 'neutral': 0}
        
        for item in news_items:
            text = f"{item['title']} {item['description']}"
            
            # Use both TextBlob and VADER for better accuracy
            textblob_result = self.analyze_sentiment_textblob(text)
            vader_result = self.analyze_sentiment_vader(text)
            
            # Combine results (weighted average)
            combined_score = (textblob_result['polarity'] + vader_result['compound']) / 2
            
            if combined_score > 0.1:
                sentiment = 'positive'
            elif combined_score < -0.1:
                sentiment = 'negative'
            else:
                sentiment = 'neutral'
            
            sentiments.append(combined_score)
            sentiment_breakdown[sentiment] += 1
        
        # Calculate overall metrics
        overall_score = np.mean(sentiments) if sentiments else 0
        
        if overall_score > 0.1:
            overall_sentiment = 'positive'
        elif overall_score < -0.1:
            overall_sentiment = 'negative'
        else:
            overall_sentiment = 'neutral'
        
        return {
            'overall_sentiment': overall_sentiment,
            'sentiment_score': overall_score,
            'news_count': len(news_items),
            'sentiment_breakdown': sentiment_breakdown,
            'recent_news': news_items[:5]  # Return top 5 recent news items
        }
    
    def get_market_sentiment_indicators(self, symbols):
        """Calculate market-wide sentiment indicators"""
        try:
            # VIX-like calculation using Nifty options (if available)
            nifty = yf.download("^NSEI", period="1mo")
            
            if nifty.empty:
                return {}
            
            # Calculate implied volatility proxy
            returns = nifty['Close'].pct_change().dropna()
            current_vol = returns.rolling(20).std().iloc[-1] * np.sqrt(252)
            
            # Fear & Greed indicators
            indicators = {}
            
            # Market momentum (20-day vs 50-day MA)
            sma_20 = nifty['Close'].rolling(20).mean().iloc[-1]
            sma_50 = nifty['Close'].rolling(50).mean().iloc[-1]
            indicators['momentum_signal'] = 'bullish' if sma_20 > sma_50 else 'bearish'
            
            # Volatility regime
            vol_percentile = (current_vol - returns.rolling(252).std().min()) / (returns.rolling(252).std().max() - returns.rolling(252).std().min())
            if vol_percentile > 0.8:
                indicators['volatility_regime'] = 'high_fear'
            elif vol_percentile < 0.2:
                indicators['volatility_regime'] = 'complacency'
            else:
                indicators['volatility_regime'] = 'normal'
            
            # Breadth indicator (% of stocks above their 20-day MA)
            above_ma_count = 0
            total_count = 0
            
            for symbol in symbols[:10]:  # Sample to avoid rate limits
                try:
                    stock_data = yf.download(symbol + ".NS", period="1mo")
                    if not stock_data.empty:
                        current_price = stock_data['Close'].iloc[-1]
                        ma_20 = stock_data['Close'].rolling(20).mean().iloc[-1]
                        if current_price > ma_20:
                            above_ma_count += 1
                        total_count += 1
                except:
                    continue
            
            if total_count > 0:
                breadth_ratio = above_ma_count / total_count
                if breadth_ratio > 0.7:
                    indicators['market_breadth'] = 'strong'
                elif breadth_ratio < 0.3:
                    indicators['market_breadth'] = 'weak'
                else:
                    indicators['market_breadth'] = 'mixed'
            
            return indicators
            
        except Exception as e:
            print(f"Error calculating market sentiment: {e}")
            return {}