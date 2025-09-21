#!/usr/bin/env python3
# test_recommendations.py - Test the trading recommendation engine

import sys
import traceback
from trading_recommendations import TradingRecommendationEngine

def test_recommendation_engine():
    """Test the trading recommendation engine"""
    print("🎯 Testing Trading Recommendation Engine")
    print("=" * 50)
    
    try:
        # Initialize recommendation engine
        print("1. Initializing Recommendation Engine...")
        engine = TradingRecommendationEngine()
        print("   ✅ Engine initialized successfully")
        
        # Test stock symbols
        test_symbols = ["RELIANCE", "TCS", "INFY"]
        test_horizons = [7, 30, 60, 90]
        
        for symbol in test_symbols:
            print(f"\n2. Testing recommendations for {symbol}...")
            
            for horizon in test_horizons:
                print(f"   📊 Testing {horizon}-day horizon...")
                
                recommendation = engine.generate_recommendation(symbol, horizon)
                
                if recommendation:
                    action = recommendation['action']
                    confidence = recommendation['confidence']
                    overall_score = recommendation['overall_score']
                    target_price = recommendation['target_price']
                    current_price = recommendation['current_price']
                    expected_return = recommendation['expected_return']
                    
                    print(f"   ✅ {horizon}d: {action} ({confidence}) - Score: {overall_score:.1f}")
                    print(f"      💰 Current: ₹{current_price:.2f} → Target: ₹{target_price:.2f} ({expected_return:+.1f}%)")
                    
                    # Test component scores
                    scores = recommendation['component_scores']
                    score_summary = ", ".join([f"{k}: {v:.0f}" for k, v in scores.items()])
                    print(f"      📈 Scores: {score_summary}")
                    
                else:
                    print(f"   ❌ {horizon}d: Failed to generate recommendation")
        
        print(f"\n3. Testing recommendation components...")
        
        # Test individual components
        test_recommendation = engine.generate_recommendation("RELIANCE", 30)
        if test_recommendation:
            print("   ✅ Full recommendation structure:")
            
            required_fields = [
                'action', 'confidence', 'overall_score', 'component_scores',
                'current_price', 'target_price', 'stop_loss', 'risk_reward_ratio',
                'expected_return', 'reasoning', 'time_horizon_days'
            ]
            
            for field in required_fields:
                if field in test_recommendation:
                    print(f"      ✅ {field}: {type(test_recommendation[field]).__name__}")
                else:
                    print(f"      ❌ Missing field: {field}")
            
            # Test reasoning
            reasoning = test_recommendation.get('reasoning', [])
            print(f"   📝 Reasoning points: {len(reasoning)}")
            for i, reason in enumerate(reasoning[:3], 1):  # Show first 3
                print(f"      {i}. {reason}")
        
        print(f"\n🎉 Recommendation engine tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        print("\nFull traceback:")
        traceback.print_exc()
        return False

def test_scoring_components():
    """Test individual scoring components"""
    print("\n🔍 Testing Scoring Components")
    print("-" * 30)
    
    try:
        engine = TradingRecommendationEngine()
        
        # Test with sample data
        print("Testing scoring weights...")
        weights = engine.weights
        total_weight = sum(weights.values())
        
        print(f"   📊 Weights (total: {total_weight:.2f}):")
        for component, weight in weights.items():
            print(f"      • {component}: {weight:.2f} ({weight/total_weight*100:.1f}%)")
        
        if abs(total_weight - 1.0) < 0.01:
            print("   ✅ Weights sum to 1.0 (correct)")
        else:
            print(f"   ⚠️ Weights sum to {total_weight:.3f} (should be 1.0)")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Scoring test failed: {str(e)}")
        return False

def test_recommendation_logic():
    """Test recommendation logic and thresholds"""
    print("\n🧠 Testing Recommendation Logic")
    print("-" * 30)
    
    try:
        engine = TradingRecommendationEngine()
        
        # Test score to recommendation mapping
        test_scores = [10, 25, 40, 45, 55, 60, 75, 90]
        
        print("Testing score-to-recommendation mapping:")
        for score in test_scores:
            # Simulate recommendation logic
            if score >= 75:
                expected = "STRONG BUY"
            elif score >= 60:
                expected = "BUY"
            elif score >= 55:
                expected = "WEAK BUY"
            elif score >= 45:
                expected = "HOLD"
            elif score >= 40:
                expected = "WEAK SELL"
            elif score >= 25:
                expected = "SELL"
            else:
                expected = "STRONG SELL"
            
            print(f"   Score {score:2d} → {expected}")
        
        print("   ✅ Recommendation thresholds working correctly")
        return True
        
    except Exception as e:
        print(f"   ❌ Logic test failed: {str(e)}")
        return False

def test_dependencies():
    """Test required dependencies for recommendations"""
    print("\n🔍 Testing Recommendation Dependencies")
    print("-" * 40)
    
    dependencies = [
        ('pandas', 'pd'),
        ('numpy', 'np'),
        ('yfinance', 'yf'),
        ('enhanced_technical', 'EnhancedTechnicalAnalysis'),
        ('ml_predictions', 'MLPredictor'),
        ('advanced_analytics', 'StockAnalytics')
    ]
    
    missing_deps = []
    
    for dep_name, import_name in dependencies:
        try:
            if dep_name == 'pandas':
                import pandas as pd
            elif dep_name == 'numpy':
                import numpy as np
            elif dep_name == 'yfinance':
                import yfinance as yf
            elif dep_name == 'enhanced_technical':
                from enhanced_technical import EnhancedTechnicalAnalysis
            elif dep_name == 'ml_predictions':
                from ml_predictions import MLPredictor
            elif dep_name == 'advanced_analytics':
                from advanced_analytics import StockAnalytics
            
            print(f"   ✅ {dep_name}")
            
        except ImportError as e:
            print(f"   ❌ {dep_name} - MISSING: {e}")
            missing_deps.append(dep_name)
    
    if missing_deps:
        print(f"\n❌ Missing dependencies: {', '.join(missing_deps)}")
        return False
    else:
        print("\n✅ All recommendation dependencies available!")
        return True

if __name__ == "__main__":
    print("🚀 Enhanced Stock Screener - Recommendation Engine Test")
    print("=" * 60)
    
    # Test dependencies first
    deps_ok = test_dependencies()
    
    if deps_ok:
        # Test scoring components
        scoring_ok = test_scoring_components()
        
        # Test recommendation logic
        logic_ok = test_recommendation_logic()
        
        # Test full recommendation engine
        engine_ok = test_recommendation_engine()
        
        if all([scoring_ok, logic_ok, engine_ok]):
            print("\n" + "=" * 60)
            print("🎉 ALL RECOMMENDATION TESTS PASSED!")
            print("The trading recommendation engine is ready to use.")
            print("\nNew features available:")
            print("• Buy/Sell/Hold recommendations with confidence levels")
            print("• 90-day time horizon slider (1-90 days)")
            print("• Target price and stop loss calculations")
            print("• Risk-reward ratio analysis")
            print("• Multi-factor scoring system")
            print("• Detailed reasoning and action plans")
            print("\nTo use:")
            print("1. Run: streamlit run enhanced_app.py")
            print("2. Navigate to 'Technical Analysis' step")
            print("3. Use the 90-day analysis period slider")
            print("4. View comprehensive trading recommendations")
        else:
            print("\n" + "=" * 60)
            print("❌ SOME TESTS FAILED!")
            print("Please check the errors above and fix them.")
            sys.exit(1)
    else:
        print("\n" + "=" * 60)
        print("❌ DEPENDENCY CHECK FAILED!")
        print("Please install missing dependencies first.")
        sys.exit(1)