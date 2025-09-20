# clean_app.py - Clean, Easy-to-Navigate Stock Screener
import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# Import our modules with fallbacks
try:
    from advanced_analytics import StockAnalytics
    from enhanced_sentiment import EnhancedSentimentAnalyzer
    from ml_predictions import MLPredictor
    from enhanced_technical import EnhancedTechnicalAnalysis
    ADVANCED_FEATURES = True
except ImportError as e:
    print(f"Advanced features not available: {e}")
    ADVANCED_FEATURES = False

# Always import the simple fallback
from simple_technical import SimpleTechnicalAnalysis

# Page config
st.set_page_config(
    page_title="Clean Stock Screener",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize analytics with fallbacks
@st.cache_resource
def get_analytics():
    analytics_dict = {
        'technical_analyzer': SimpleTechnicalAnalysis()  # Always available
    }
    
    if ADVANCED_FEATURES:
        try:
            analytics_dict.update({
                'stock_analytics': StockAnalytics(),
                'sentiment_analyzer': EnhancedSentimentAnalyzer(),
                'ml_predictor': MLPredictor(),
                'enhanced_technical_analyzer': EnhancedTechnicalAnalysis()
            })
        except Exception as e:
            print(f"Error initializing advanced analytics: {e}")
    
    return analytics_dict

analytics = get_analytics()

# Initialize session state
if 'stocks' not in st.session_state:
    st.session_state.stocks = []
if 'current_stock' not in st.session_state:
    st.session_state.current_stock = ""

# Header
st.title("🚀 Clean Indian Stock Screener")
st.markdown("**Simple, fast, and powerful stock analysis**")

# Sidebar - Stock Management
st.sidebar.header("📊 Stock Management")

# Stock input with Enter key support
with st.sidebar:
    st.subheader("Add Stocks")
    
    # Text input for single stock with Enter key detection
    stock_input = st.text_input(
        "Enter stock symbol:",
        placeholder="e.g., RELIANCE",
        key="stock_input",
        help="Press Enter to add stock"
    )
    
    # Add stock button and Enter key handling
    col1, col2 = st.columns(2)
    with col1:
        add_clicked = st.button("➕ Add", use_container_width=True)
    with col2:
        clear_clicked = st.button("🗑️ Clear", use_container_width=True)
    
    # Handle stock addition (both button click and Enter key)
    if stock_input and (add_clicked or stock_input != st.session_state.get('last_input', '')):
        stock_symbol = stock_input.upper().strip()
        if stock_symbol and stock_symbol not in st.session_state.stocks:
            st.session_state.stocks.append(stock_symbol)
            st.session_state.stock_input = ""  # Clear input
            st.success(f"✅ Added {stock_symbol}")
            st.rerun()
        elif stock_symbol in st.session_state.stocks:
            st.warning(f"⚠️ {stock_symbol} already added!")
    
    st.session_state.last_input = stock_input
    
    # Clear all stocks
    if clear_clicked:
        st.session_state.stocks = []
        st.session_state.current_stock = ""
        st.rerun()
    
    # Quick add popular stocks
    st.subheader("Quick Add")
    popular_stocks = ["RELIANCE", "TCS", "INFY", "HDFCBANK", "ICICIBANK", "WIPRO", "LT", "BHARTIARTL"]
    
    cols = st.columns(2)
    for i, stock in enumerate(popular_stocks):
        with cols[i % 2]:
            if st.button(f"+ {stock}", key=f"quick_{stock}", use_container_width=True):
                if stock not in st.session_state.stocks:
                    st.session_state.stocks.append(stock)
                    st.rerun()

# Display current stocks
if st.session_state.stocks:
    st.sidebar.subheader("📋 Current Stocks")
    for i, stock in enumerate(st.session_state.stocks):
        col1, col2 = st.sidebar.columns([3, 1])
        with col1:
            if st.button(f"📈 {stock}", key=f"select_{stock}", use_container_width=True):
                st.session_state.current_stock = stock
                st.rerun()
        with col2:
            if st.button("❌", key=f"remove_{stock}"):
                st.session_state.stocks.remove(stock)
                if st.session_state.current_stock == stock:
                    st.session_state.current_stock = ""
                st.rerun()

# Main content area
if not st.session_state.stocks:
    # Welcome screen
    st.markdown("---")
    st.markdown("""
    ## 👋 Welcome to Clean Stock Screener
    
    **Get started in 3 simple steps:**
    
    1. **Add stocks** using the sidebar (type symbol and press Enter)
    2. **Click on a stock** to analyze it
    3. **Explore** technical analysis, predictions, and sentiment
    
    ### ✨ Features:
    - 📊 Real-time stock data
    - 🤖 AI-powered price predictions  
    - 📈 Advanced technical analysis
    - 💭 News sentiment analysis
    - ⚠️ Risk metrics
    - 📋 Downloadable reports
    
    ### 🚀 Quick Start:
    Try adding popular stocks like **RELIANCE**, **TCS**, or **INFY** using the sidebar!
    """)
    
    # Sample data showcase
    st.subheader("📊 Sample Analysis Preview")
    
    # Create sample chart
    dates = pd.date_range(start='2024-01-01', end='2024-09-20', freq='D')
    sample_prices = 100 + np.cumsum(np.random.randn(len(dates)) * 0.5)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates,
        y=sample_prices,
        mode='lines',
        name='Sample Stock Price',
        line=dict(color='#1f77b4', width=2)
    ))
    fig.update_layout(
        title="Sample Stock Price Chart",
        xaxis_title="Date",
        yaxis_title="Price (₹)",
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)

else:
    # Stock analysis interface
    if not st.session_state.current_stock:
        st.session_state.current_stock = st.session_state.stocks[0]
    
    # Stock selector
    st.markdown("---")
    selected_stock = st.selectbox(
        "📊 Select stock to analyze:",
        st.session_state.stocks,
        index=st.session_state.stocks.index(st.session_state.current_stock) if st.session_state.current_stock in st.session_state.stocks else 0
    )
    
    if selected_stock != st.session_state.current_stock:
        st.session_state.current_stock = selected_stock
        st.rerun()
    
    # Analysis tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Overview", 
        "📈 Technical", 
        "🤖 AI Prediction", 
        "💭 Sentiment", 
        "📋 Report"
    ])
    
    # Get stock data
    @st.cache_data(ttl=300)  # Cache for 5 minutes
    def get_stock_data(symbol):
        try:
            ticker = yf.Ticker(symbol + ".NS")
            info = ticker.info
            hist = ticker.history(period="6mo")
            return info, hist
        except Exception as e:
            st.error(f"Error fetching data for {symbol}: {e}")
            return None, None
    
    info, hist = get_stock_data(selected_stock)
    
    if info is None or hist is None or hist.empty:
        st.error(f"❌ Could not fetch data for {selected_stock}")
    else:
        current_price = hist['Close'].iloc[-1]
        
        # Tab 1: Overview
        with tab1:
            st.subheader(f"📊 {selected_stock} - {info.get('shortName', selected_stock)}")
            
            # Key metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Current Price", f"₹{current_price:.2f}")
            
            with col2:
                change = hist['Close'].pct_change().iloc[-1] * 100
                st.metric("Daily Change", f"{change:+.2f}%")
            
            with col3:
                volume = hist['Volume'].iloc[-1]
                st.metric("Volume", f"{volume:,.0f}")
            
            with col4:
                market_cap = info.get('marketCap', 0)
                if market_cap:
                    st.metric("Market Cap", f"₹{market_cap/10000000:.0f}Cr")
                else:
                    st.metric("Market Cap", "N/A")
            
            # Price chart
            st.subheader("📈 Price Chart (6 Months)")
            
            fig = go.Figure()
            fig.add_trace(go.Candlestick(
                x=hist.index,
                open=hist['Open'],
                high=hist['High'],
                low=hist['Low'],
                close=hist['Close'],
                name=selected_stock
            ))
            
            # Add moving averages
            sma_20 = hist['Close'].rolling(20).mean()
            sma_50 = hist['Close'].rolling(50).mean()
            
            fig.add_trace(go.Scatter(
                x=hist.index, y=sma_20,
                line=dict(color='orange', width=1),
                name='SMA 20'
            ))
            
            fig.add_trace(go.Scatter(
                x=hist.index, y=sma_50,
                line=dict(color='red', width=1),
                name='SMA 50'
            ))
            
            fig.update_layout(
                title=f"{selected_stock} - Price & Moving Averages",
                xaxis_title="Date",
                yaxis_title="Price (₹)",
                height=500,
                xaxis_rangeslider_visible=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Company info
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📋 Company Details")
                st.write(f"**Sector:** {info.get('sector', 'N/A')}")
                st.write(f"**Industry:** {info.get('industry', 'N/A')}")
                st.write(f"**Employees:** {info.get('fullTimeEmployees', 'N/A'):,}")
                st.write(f"**Website:** {info.get('website', 'N/A')}")
            
            with col2:
                st.subheader("💰 Financial Ratios")
                st.write(f"**P/E Ratio:** {info.get('forwardPE', 'N/A')}")
                st.write(f"**P/B Ratio:** {info.get('priceToBook', 'N/A')}")
                st.write(f"**Dividend Yield:** {info.get('dividendYield', 'N/A')}")
                st.write(f"**ROE:** {info.get('returnOnEquity', 'N/A')}")
        
        # Tab 2: Technical Analysis
        with tab2:
            st.subheader(f"📈 Technical Analysis - {selected_stock}")
            
            if st.button("🔍 Run Technical Analysis", key="tech_analysis"):
                with st.spinner("Calculating technical indicators..."):
                    try:
                        tech_analysis = analytics['technical_analyzer'].get_comprehensive_analysis(selected_stock)
                        
                        if tech_analysis:
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.subheader("📊 Key Indicators")
                                basic = tech_analysis.get('basic_indicators', {})
                                
                                # Display indicators in a clean format
                                indicators = [
                                    ("RSI", basic.get('RSI', 0), "0-100"),
                                    ("MACD", basic.get('MACD', 0), "Signal"),
                                    ("Stochastic %K", basic.get('Stoch_K', 0), "0-100"),
                                    ("Williams %R", basic.get('Williams_R', 0), "-100-0"),
                                    ("CCI", basic.get('CCI', 0), "Signal")
                                ]
                                
                                for name, value, range_info in indicators:
                                    if isinstance(value, (int, float)):
                                        st.metric(name, f"{value:.2f}", help=f"Range: {range_info}")
                            
                            with col2:
                                st.subheader("📈 Trend Analysis")
                                trend = tech_analysis.get('trend_analysis', {})
                                
                                direction = trend.get('direction', 'Unknown')
                                strength = trend.get('strength', 0)
                                adx = trend.get('adx', 0)
                                
                                st.metric("Trend Direction", direction.upper())
                                st.metric("Trend Strength", f"{strength:.2f}")
                                st.metric("ADX", f"{adx:.2f}")
                                
                                # Trend interpretation
                                if adx > 25:
                                    st.success("🔥 Strong trend detected")
                                elif adx > 20:
                                    st.info("📈 Moderate trend")
                                else:
                                    st.warning("📊 Weak/sideways trend")
                            
                            # Support and Resistance
                            st.subheader("🎯 Support & Resistance Levels")
                            sr = tech_analysis.get('support_resistance', {})
                            
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                st.metric("Current Price", f"₹{sr.get('current_price', current_price):.2f}")
                            
                            with col2:
                                resistance = sr.get('resistance_levels', [])
                                if resistance:
                                    st.write("**Resistance Levels:**")
                                    for r in resistance[:3]:  # Show top 3
                                        st.write(f"₹{r:.2f}")
                                else:
                                    st.write("**Resistance:** Not detected")
                            
                            with col3:
                                support = sr.get('support_levels', [])
                                if support:
                                    st.write("**Support Levels:**")
                                    for s in support[:3]:  # Show top 3
                                        st.write(f"₹{s:.2f}")
                                else:
                                    st.write("**Support:** Not detected")
                        
                        else:
                            st.error("Could not perform technical analysis")
                            
                    except Exception as e:
                        st.error(f"Technical analysis error: {e}")
        
        # Tab 3: AI Prediction
        with tab3:
            st.subheader(f"🤖 AI Price Prediction - {selected_stock}")
            
            prediction_days = st.slider("Prediction horizon (days):", 1, 30, 5)
            
            if st.button("🔮 Generate AI Prediction", key="ai_prediction"):
                with st.spinner("Training AI models and generating prediction..."):
                    try:
                        prediction = analytics['ml_predictor'].predict_future_price(selected_stock, prediction_days)
                        
                        if prediction:
                            col1, col2, col3 = st.columns(3)
                            
                            current = prediction['current_price']
                            ensemble = prediction['ensemble_prediction']
                            predicted = ensemble['predicted_price']
                            change_pct = ensemble['predicted_return'] * 100
                            
                            with col1:
                                st.metric("Current Price", f"₹{current:.2f}")
                            
                            with col2:
                                st.metric(
                                    f"Predicted Price ({prediction_days}d)",
                                    f"₹{predicted:.2f}",
                                    f"{change_pct:+.2f}%"
                                )
                            
                            with col3:
                                confidence = analytics['ml_predictor'].get_prediction_confidence(selected_stock)
                                st.metric("Model Confidence", f"{confidence*100:.1f}%")
                            
                            # Model performance
                            st.subheader("📊 Model Performance")
                            perf_df = pd.DataFrame(prediction['model_performance']).T
                            st.dataframe(perf_df, use_container_width=True)
                            
                            # Individual model predictions
                            st.subheader("🔍 Individual Model Predictions")
                            for model_name, pred_data in prediction['individual_models'].items():
                                model_price = pred_data['predicted_price']
                                model_return = pred_data['predicted_return'] * 100
                                st.write(f"**{model_name.title()}:** ₹{model_price:.2f} ({model_return:+.2f}%)")
                        
                        else:
                            st.error("Could not generate prediction for this stock")
                            
                    except Exception as e:
                        st.error(f"Prediction error: {e}")
        
        # Tab 4: Sentiment Analysis
        with tab4:
            st.subheader(f"💭 Sentiment Analysis - {selected_stock}")
            
            if st.button("📰 Analyze News Sentiment", key="sentiment_analysis"):
                with st.spinner("Analyzing news sentiment..."):
                    try:
                        sentiment_result = analytics['sentiment_analyzer'].get_comprehensive_sentiment(selected_stock)
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.metric("Overall Sentiment", sentiment_result['overall_sentiment'].title())
                            st.metric("Sentiment Score", f"{sentiment_result['sentiment_score']:.3f}")
                            st.metric("News Articles", sentiment_result['news_count'])
                        
                        with col2:
                            # Sentiment breakdown pie chart
                            breakdown = sentiment_result['sentiment_breakdown']
                            if sum(breakdown.values()) > 0:
                                fig = go.Figure(data=[go.Pie(
                                    labels=list(breakdown.keys()),
                                    values=list(breakdown.values()),
                                    hole=0.3
                                )])
                                fig.update_layout(
                                    title="Sentiment Distribution",
                                    height=300
                                )
                                st.plotly_chart(fig, use_container_width=True)
                        
                        # Recent news
                        if sentiment_result.get('recent_news'):
                            st.subheader("📰 Recent News Headlines")
                            for i, news in enumerate(sentiment_result['recent_news'][:5]):  # Show top 5
                                with st.expander(f"{i+1}. {news['title'][:60]}..."):
                                    st.write(f"**Source:** {news['source']}")
                                    st.write(f"**Published:** {news['publishedAt']}")
                                    st.write(f"**Description:** {news['description']}")
                        else:
                            st.info("No recent news found for this stock")
                            
                    except Exception as e:
                        st.error(f"Sentiment analysis error: {e}")
        
        # Tab 5: Report
        with tab5:
            st.subheader(f"📋 Analysis Report - {selected_stock}")
            
            if st.button("📊 Generate Complete Report", key="generate_report"):
                with st.spinner("Generating comprehensive report..."):
                    try:
                        # Collect all analysis data
                        report_data = {
                            'Symbol': selected_stock,
                            'Company': info.get('shortName', selected_stock),
                            'Current_Price': current_price,
                            'Sector': info.get('sector', 'N/A'),
                            'Market_Cap_Cr': info.get('marketCap', 0) / 10000000 if info.get('marketCap') else 0,
                            'PE_Ratio': info.get('forwardPE', 'N/A'),
                            'Analysis_Date': datetime.now().strftime('%Y-%m-%d %H:%M')
                        }
                        
                        # Add technical analysis
                        try:
                            tech_analysis = analytics['technical_analyzer'].get_comprehensive_analysis(selected_stock)
                            if tech_analysis:
                                basic = tech_analysis.get('basic_indicators', {})
                                trend = tech_analysis.get('trend_analysis', {})
                                
                                report_data.update({
                                    'RSI': basic.get('RSI', 'N/A'),
                                    'MACD': basic.get('MACD', 'N/A'),
                                    'Trend_Direction': trend.get('direction', 'N/A'),
                                    'Trend_Strength': trend.get('strength', 'N/A')
                                })
                        except:
                            pass
                        
                        # Add risk metrics
                        try:
                            risk_metrics = analytics['stock_analytics'].calculate_risk_metrics(selected_stock)
                            if risk_metrics:
                                report_data.update({
                                    'Annual_Return_Pct': risk_metrics.get('annual_return', 0) * 100,
                                    'Volatility_Pct': risk_metrics.get('annual_volatility', 0) * 100,
                                    'Sharpe_Ratio': risk_metrics.get('sharpe_ratio', 'N/A'),
                                    'Max_Drawdown_Pct': risk_metrics.get('max_drawdown', 0) * 100
                                })
                        except:
                            pass
                        
                        # Add sentiment
                        try:
                            sentiment = analytics['sentiment_analyzer'].get_comprehensive_sentiment(selected_stock)
                            report_data.update({
                                'Sentiment': sentiment['overall_sentiment'],
                                'Sentiment_Score': sentiment['sentiment_score'],
                                'News_Count': sentiment['news_count']
                            })
                        except:
                            pass
                        
                        # Display report
                        st.subheader("📊 Complete Analysis Summary")
                        
                        # Convert to DataFrame for display
                        report_df = pd.DataFrame([report_data])
                        st.dataframe(report_df.T, use_container_width=True)
                        
                        # Download button
                        csv = report_df.to_csv(index=False)
                        st.download_button(
                            label="📥 Download Report (CSV)",
                            data=csv,
                            file_name=f"{selected_stock}_analysis_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                            mime="text/csv",
                            type="primary"
                        )
                        
                        st.success("✅ Report generated successfully!")
                        
                    except Exception as e:
                        st.error(f"Report generation error: {e}")

# Footer
st.markdown("---")
st.markdown("**Clean Stock Screener** - Simple, Fast, Powerful | Made with ❤️ using Streamlit")