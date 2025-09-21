#!/usr/bin/env python3
# test_projection.py - Test the new projection functionality

import sys
import traceback
from enhanced_technical import EnhancedTechnicalAnalysis

def test_projection_functionality():
    """Test the new projection features"""
    print("🧪 Testing Enhanced Technical Analysis with Projections")
    print("=" * 60)
    
    try:
        # Initialize analyzer
        print("1. Initializing Enhanced Technical Analyzer...")
        analyzer = EnhancedTechnicalAnalysis()
        print("   ✅ Analyzer initialized successfully")
        
        # Test stock symbol
        test_symbol = "RELIANCE"
        projection_days = 15
        
        print(f"\n2. Testing projection for {test_symbol} ({projection_days} days)...")
        
        # Test comprehensive analysis
        print("   📊 Running comprehensive analysis...")
        analysis = analyzer.get_comprehensive_analysis(test_symbol)
        
        if analysis:
            print("   ✅ Comprehensive analysis completed")
            
            # Print basic indicators
            basic = analysis.get('basic_indicators', {})
            print(f"   📈 RSI: {basic.get('RSI', 'N/A'):.2f}" if isinstance(basic.get('RSI'), (int, float)) else "   📈 RSI: N/A")
            print(f"   📈 MACD: {basic.get('MACD', 'N/A'):.3f}" if isinstance(basic.get('MACD'), (int, float)) else "   📈 MACD: N/A")
            
            # Print support/resistance
            sr = analysis.get('support_resistance', {})
            current_price = sr.get('current_price', 0)
            print(f"   💰 Current Price: ₹{current_price:.2f}" if current_price > 0 else "   💰 Current Price: N/A")
            
        else:
            print("   ❌ Comprehensive analysis failed")
            return False
        
        # Test projection chart creation
        print("\n3. Testing projection chart creation...")
        fig, projections = analyzer.create_projection_chart(test_symbol, projection_days)
        
        if fig is not None and projections:
            print("   ✅ Projection chart created successfully")
            
            # Print projection summary
            print(f"\n   📊 Projection Summary ({projection_days} days):")
            for method, proj in projections.items():
                if 'prices' in proj and len(proj['prices']) > 0:
                    current = proj['prices'][0]
                    final = proj['prices'][-1]
                    change = ((final - current) / current * 100) if current > 0 else 0
                    print(f"   • {proj['method']}: ₹{final:.2f} ({change:+.2f}%)")
            
        else:
            print("   ❌ Projection chart creation failed")
            return False
        
        # Test individual projection methods
        print("\n4. Testing individual projection methods...")
        
        import yfinance as yf
        ticker = yf.Ticker(test_symbol + ".NS")
        df = ticker.history(period="6mo")
        
        if not df.empty:
            df = analyzer.add_technical_indicators(df)
            current_price = df['Close'].iloc[-1]
            
            import pandas as pd
            future_dates = pd.date_range(start=df.index[-1] + pd.Timedelta(days=1), 
                                       periods=projection_days, freq='D')
            
            # Test trend projection
            trend_proj = analyzer.trend_projection(df, future_dates, current_price)
            if trend_proj and 'prices' in trend_proj:
                print(f"   ✅ Trend projection: {len(trend_proj['prices'])} data points")
            else:
                print("   ❌ Trend projection failed")
            
            # Test MA projection
            ma_proj = analyzer.ma_projection(df, future_dates, current_price)
            if ma_proj and 'prices' in ma_proj:
                print(f"   ✅ MA projection: {len(ma_proj['prices'])} data points")
            else:
                print("   ❌ MA projection failed")
            
            # Test S/R projection
            sr_proj = analyzer.sr_projection(df, future_dates, current_price)
            if sr_proj and 'prices' in sr_proj:
                print(f"   ✅ S/R projection: {len(sr_proj['prices'])} data points")
            else:
                print("   ❌ S/R projection failed")
            
        print("\n🎉 All projection tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        print("\nFull traceback:")
        traceback.print_exc()
        return False

def test_dependencies():
    """Test required dependencies"""
    print("\n🔍 Testing Dependencies")
    print("-" * 30)
    
    dependencies = [
        ('pandas', 'pd'),
        ('numpy', 'np'),
        ('yfinance', 'yf'),
        ('plotly.graph_objects', 'go'),
        ('plotly.subplots', 'make_subplots'),
        ('streamlit', 'st')
    ]
    
    missing_deps = []
    
    for dep_name, import_name in dependencies:
        try:
            if import_name == 'pd':
                import pandas as pd
            elif import_name == 'np':
                import numpy as np
            elif import_name == 'yf':
                import yfinance as yf
            elif import_name == 'go':
                import plotly.graph_objects as go
            elif import_name == 'make_subplots':
                from plotly.subplots import make_subplots
            elif import_name == 'st':
                import streamlit as st
            
            print(f"   ✅ {dep_name}")
            
        except ImportError:
            print(f"   ❌ {dep_name} - MISSING")
            missing_deps.append(dep_name)
    
    # Test optional dependencies
    optional_deps = [
        ('scipy', 'scipy.stats'),
        ('sklearn', 'sklearn.linear_model')
    ]
    
    print("\n📦 Optional Dependencies:")
    for dep_name, import_path in optional_deps:
        try:
            if dep_name == 'scipy':
                from scipy import stats
            elif dep_name == 'sklearn':
                from sklearn.linear_model import LinearRegression
            
            print(f"   ✅ {dep_name} (enhanced features available)")
            
        except ImportError:
            print(f"   ⚠️  {dep_name} (basic features only)")
    
    if missing_deps:
        print(f"\n❌ Missing required dependencies: {', '.join(missing_deps)}")
        print("Please install them using: pip install " + " ".join(missing_deps))
        return False
    else:
        print("\n✅ All required dependencies are available!")
        return True

if __name__ == "__main__":
    print("🚀 Enhanced Stock Screener - Projection Feature Test")
    print("=" * 60)
    
    # Test dependencies first
    deps_ok = test_dependencies()
    
    if deps_ok:
        # Test projection functionality
        success = test_projection_functionality()
        
        if success:
            print("\n" + "=" * 60)
            print("🎉 ALL TESTS PASSED!")
            print("The projection feature is ready to use.")
            print("\nTo use the new feature:")
            print("1. Run: streamlit run enhanced_app.py")
            print("2. Navigate to 'Technical Analysis' step")
            print("3. Use the projection days slider (1-30 days)")
            print("4. Analyze stocks with multiple projection methods")
        else:
            print("\n" + "=" * 60)
            print("❌ TESTS FAILED!")
            print("Please check the errors above and fix them.")
            sys.exit(1)
    else:
        print("\n" + "=" * 60)
        print("❌ DEPENDENCY CHECK FAILED!")
        print("Please install missing dependencies first.")
        sys.exit(1)