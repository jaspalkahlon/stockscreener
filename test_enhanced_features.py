# test_enhanced_features.py
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_imports():
    """Test if all modules can be imported successfully"""
    print("🧪 Testing module imports...")
    
    try:
        from advanced_analytics import StockAnalytics
        print("✅ Advanced Analytics - OK")
    except Exception as e:
        print(f"❌ Advanced Analytics - Error: {e}")
    
    try:
        from enhanced_sentiment import EnhancedSentimentAnalyzer
        print("✅ Enhanced Sentiment - OK")
    except Exception as e:
        print(f"❌ Enhanced Sentiment - Error: {e}")
    
    try:
        from ml_predictions import MLPredictor
        print("✅ ML Predictions - OK")
    except Exception as e:
        print(f"❌ ML Predictions - Error: {e}")
    
    try:
        from enhanced_technical import EnhancedTechnicalAnalysis
        print("✅ Enhanced Technical - OK")
    except Exception as e:
        print(f"❌ Enhanced Technical - Error: {e}")

def test_api_keys():
    """Test API key configuration"""
    print("\n🔑 Testing API keys...")
    
    newsapi_key = os.getenv('NEWSAPI_KEY')
    if newsapi_key:
        print(f"✅ NewsAPI Key - Configured ({newsapi_key[:8]}...)")
    else:
        print("⚠️ NewsAPI Key - Not configured (will use free alternatives)")
    
    hf_key = os.getenv('HF_API_KEY')
    if hf_key:
        print(f"✅ HuggingFace Key - Configured ({hf_key[:8]}...)")
    else:
        print("⚠️ HuggingFace Key - Not configured (will use TextBlob/VADER)")

def test_basic_functionality():
    """Test basic functionality with a sample stock"""
    print("\n🚀 Testing basic functionality...")
    
    try:
        # Test stock analytics
        from advanced_analytics import StockAnalytics
        analytics = StockAnalytics()
        
        # Test with a popular Indian stock
        test_symbol = "RELIANCE"
        print(f"Testing with {test_symbol}...")
        
        # Test feature extraction
        features = analytics.get_enhanced_features(test_symbol, period="3mo")
        if features is not None and not features.empty:
            print(f"✅ Feature extraction - Got {len(features)} data points")
        else:
            print("⚠️ Feature extraction - No data (might be market hours/weekend)")
        
        # Test sentiment analyzer
        from enhanced_sentiment import EnhancedSentimentAnalyzer
        sentiment_analyzer = EnhancedSentimentAnalyzer()
        
        # Test TextBlob sentiment (always works)
        test_text = "This is a great stock with strong fundamentals and good growth prospects"
        sentiment = sentiment_analyzer.analyze_sentiment_textblob(test_text)
        print(f"✅ TextBlob sentiment - {sentiment['sentiment']} (score: {sentiment['polarity']:.2f})")
        
        # Test ML predictor
        from ml_predictions import MLPredictor
        ml_predictor = MLPredictor()
        print("✅ ML Predictor initialized")
        
        # Test technical analyzer
        from enhanced_technical import EnhancedTechnicalAnalysis
        tech_analyzer = EnhancedTechnicalAnalysis()
        print("✅ Technical Analyzer initialized")
        
        print("\n🎉 All basic tests passed! The enhanced features are ready to use.")
        
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")

def test_newsapi():
    """Test NewsAPI functionality"""
    print("\n📰 Testing NewsAPI...")
    
    try:
        from enhanced_sentiment import EnhancedSentimentAnalyzer
        sentiment_analyzer = EnhancedSentimentAnalyzer()
        
        # Test NewsAPI with a simple query
        news_items = sentiment_analyzer.get_newsapi_data("RELIANCE", 7)
        
        if news_items:
            print(f"✅ NewsAPI - Retrieved {len(news_items)} articles")
            if len(news_items) > 0:
                print(f"   Sample: {news_items[0]['title'][:50]}...")
        else:
            print("⚠️ NewsAPI - No articles found (might be rate limited or no recent news)")
            
    except Exception as e:
        print(f"❌ NewsAPI test failed: {e}")

if __name__ == "__main__":
    print("🔧 Enhanced Stock Screener - Feature Test")
    print("=" * 50)
    
    test_imports()
    test_api_keys()
    test_basic_functionality()
    test_newsapi()
    
    print("\n" + "=" * 50)
    print("✨ Test completed! You can now run the enhanced app:")
    print("   streamlit run enhanced_app.py")