# enhanced_app.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta

# Import our enhanced modules
from advanced_analytics import StockAnalytics
from enhanced_sentiment import EnhancedSentimentAnalyzer
from ml_predictions import MLPredictor
from enhanced_technical import EnhancedTechnicalAnalysis

# Import original modules
import data_input
import fundamental

# App configuration
st.set_page_config(
    page_title="Enhanced Indian Stock Screener",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize enhanced analytics classes
@st.cache_resource
def get_analytics_instances():
    return {
        'stock_analytics': StockAnalytics(),
        'sentiment_analyzer': EnhancedSentimentAnalyzer(),
        'ml_predictor': MLPredictor(),
        'technical_analyzer': EnhancedTechnicalAnalysis()
    }

analytics = get_analytics_instances()

# Session state initialization
if 'step' not in st.session_state:
    st.session_state['step'] = 1
if 'symbols' not in st.session_state:
    st.session_state['symbols'] = []
if 'fundamental_results' not in st.session_state:
    st.session_state['fundamental_results'] = []
if 'selected_stocks' not in st.session_state:
    st.session_state['selected_stocks'] = []

# Enhanced sidebar navigation
st.sidebar.title("🚀 Enhanced Stock Screener")
st.sidebar.markdown("---")

# Progress indicator
progress_steps = [
    "📊 Input & Data",
    "🔍 Fundamental Analysis", 
    "🎯 Stock Selection",
    "📈 Technical Analysis",
    "🤖 ML Predictions",
    "💭 Sentiment Analysis",
    "🔬 Advanced Analytics",
    "📋 Summary Report"
]

# Show current step
current_step = st.session_state.get('step', 1)
st.sidebar.markdown(f"**Current Step: {current_step}/8**")
st.sidebar.progress(current_step / 8)
st.sidebar.markdown("---")

choice = st.sidebar.radio("Navigation:", progress_steps, index=current_step - 1, key="nav_radio")

# Helper functions
def set_step(n):
    st.session_state['step'] = n

def create_enhanced_chart(symbol, analysis_type="comprehensive"):
    """Create enhanced interactive charts"""
    try:
        import yfinance as yf
        ticker = yf.Ticker(symbol + ".NS")
        df = ticker.history(period="6mo")
        
        if df.empty:
            st.error(f"No data available for {symbol}")
            return
        
        # Create subplots
        fig = make_subplots(
            rows=4, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.05,
            subplot_titles=('Price & Volume', 'RSI', 'MACD', 'Volume'),
            row_heights=[0.5, 0.15, 0.15, 0.2]
        )
        
        # Price candlestick
        fig.add_trace(go.Candlestick(
            x=df.index,
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            name='Price'
        ), row=1, col=1)
        
        # Moving averages
        sma_20 = df['Close'].rolling(20).mean()
        sma_50 = df['Close'].rolling(50).mean()
        
        fig.add_trace(go.Scatter(
            x=df.index, y=sma_20,
            line=dict(color='orange', width=1),
            name='SMA 20'
        ), row=1, col=1)
        
        fig.add_trace(go.Scatter(
            x=df.index, y=sma_50,
            line=dict(color='red', width=1),
            name='SMA 50'
        ), row=1, col=1)
        
        # RSI
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        fig.add_trace(go.Scatter(
            x=df.index, y=rsi,
            line=dict(color='purple'),
            name='RSI'
        ), row=2, col=1)
        
        # RSI levels
        fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
        fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)
        
        # MACD
        ema_12 = df['Close'].ewm(span=12).mean()
        ema_26 = df['Close'].ewm(span=26).mean()
        macd = ema_12 - ema_26
        signal = macd.ewm(span=9).mean()
        histogram = macd - signal
        
        fig.add_trace(go.Scatter(
            x=df.index, y=macd,
            line=dict(color='blue'),
            name='MACD'
        ), row=3, col=1)
        
        fig.add_trace(go.Scatter(
            x=df.index, y=signal,
            line=dict(color='red'),
            name='Signal'
        ), row=3, col=1)
        
        # Volume
        fig.add_trace(go.Bar(
            x=df.index, y=df['Volume'],
            name='Volume',
            marker_color='lightblue'
        ), row=4, col=1)
        
        fig.update_layout(
            title=f"{symbol} - Enhanced Technical Analysis",
            xaxis_rangeslider_visible=False,
            height=800
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error creating chart for {symbol}: {e}")

# Page logic
if choice == progress_steps[0]:  # Input & Data
    set_step(1)
    st.header("📊 Stock Input & Data Collection")
    
    # Stock input with Enter key functionality
    st.subheader("Enter Stock Symbols")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Initialize symbols in session state if not exists
        if 'input_symbols' not in st.session_state:
            st.session_state.input_symbols = "RELIANCE\nTCS\nINFY\nHDFCBANK\nICICIBANK"
        
        symbols_text = st.text_area(
            "Stock symbols (NSE format, one per line):",
            value=st.session_state.input_symbols,
            height=150,
            key="symbols_textarea"
        )
        
        # Single stock input with Enter key support
        col_input, col_add = st.columns([3, 1])
        with col_input:
            single_stock = st.text_input(
                "Add individual stock:",
                placeholder="e.g., RELIANCE",
                key="single_stock"
            )
        
        with col_add:
            st.write("")  # Spacing
            add_clicked = st.button("➕ Add")
        
        # Handle adding single stock
        if (add_clicked or single_stock) and single_stock.strip():
            current_symbols = symbols_text.split('\n') if symbols_text else []
            new_symbol = single_stock.upper().strip()
            
            if new_symbol not in [s.strip().upper() for s in current_symbols]:
                current_symbols.append(new_symbol)
                st.session_state.input_symbols = '\n'.join(current_symbols)
                st.session_state.single_stock = ""  # Clear input
                st.rerun()
            else:
                st.warning(f"{new_symbol} already in the list!")
        
        # Process symbols button
        if st.button("🚀 Process Stocks", type="primary"):
            symbols = [s.strip().upper() for s in symbols_text.split('\n') if s.strip()]
            if symbols:
                st.session_state.symbols = symbols
                st.session_state.input_symbols = symbols_text
                st.success(f"✅ {len(symbols)} stocks ready for analysis")
                set_step(2)
                st.rerun()
            else:
                st.error("Please enter at least one stock symbol")
    
    with col2:
        st.info("""
        **Instructions:**
        1. Enter NSE stock symbols
        2. One symbol per line
        3. Use format: RELIANCE, TCS, etc.
        4. Click 'Process Stocks' to continue
        
        **Popular Stocks:**
        - RELIANCE (Reliance Industries)
        - TCS (Tata Consultancy)
        - INFY (Infosys)
        - HDFCBANK (HDFC Bank)
        - ICICIBANK (ICICI Bank)
        """)
        
        # Show current symbols
        if st.session_state.get('symbols'):
            st.success(f"**Ready:** {len(st.session_state.symbols)} stocks")
            for symbol in st.session_state.symbols:
                st.write(f"• {symbol}")

elif choice == progress_steps[1]:  # Fundamental Analysis
    set_step(2)
    st.header("🔍 Fundamental Analysis")
    
    symbols = st.session_state.get('symbols', [])
    if not symbols:
        st.warning("Please add stocks first in Step 1")
        if st.button("← Go to Step 1"):
            set_step(1)
            st.rerun()
    else:
        st.write(f"Analyzing {len(symbols)} stocks: {', '.join(symbols)}")
        
        if st.button("📊 Run Fundamental Analysis"):
            progress_bar = st.progress(0)
            results = []
            
            for i, symbol in enumerate(symbols):
                progress_bar.progress((i + 1) / len(symbols))
                
                try:
                    import yfinance as yf
                    ticker = yf.Ticker(symbol + ".NS")
                    info = ticker.info
                    
                    result = {
                        'symbol': symbol,
                        'name': info.get('shortName', symbol),
                        'market_cap': info.get('marketCap', 0),
                        'pe_ratio': info.get('forwardPE', 0),
                        'price': info.get('currentPrice', 0),
                        'sector': info.get('sector', 'Unknown')
                    }
                    results.append(result)
                    
                except Exception as e:
                    st.error(f"Error analyzing {symbol}: {e}")
            
            st.session_state.fundamental_results = results
            
            if results:
                df = pd.DataFrame(results)
                st.dataframe(df, use_container_width=True)
                st.success("✅ Fundamental analysis complete!")

elif choice == progress_steps[2]:  # Stock Selection
    set_step(3)
    st.header("🎯 Stock Selection for Advanced Analysis")
    
    if st.session_state['fundamental_results']:
        st.write("Select stocks for advanced technical and ML analysis:")
        
        # Display fundamental results in a nice table
        df_results = pd.DataFrame(st.session_state['fundamental_results'])
        st.dataframe(df_results, use_container_width=True)
        
        selected = st.multiselect(
            "Choose stocks for advanced analysis:",
            [row['symbol'] for row in st.session_state['fundamental_results']],
            default=[row['symbol'] for row in st.session_state['fundamental_results'][:5]]
        )
        
        st.session_state['selected_stocks'] = selected
        
        if selected:
            st.success(f"Selected {len(selected)} stocks for advanced analysis")
            
            # Quick anomaly detection
            if st.button("🔍 Quick Anomaly Detection"):
                with st.spinner("Detecting unusual stock behavior..."):
                    anomalies = analytics['stock_analytics'].detect_anomalies(selected)
                    
                    if anomalies:
                        st.subheader("🚨 Anomaly Detection Results")
                        for symbol, result in anomalies.items():
                            if result['is_anomaly']:
                                st.warning(f"**{symbol}** shows unusual behavior (Score: {result['anomaly_score']:.3f})")
                            else:
                                st.success(f"**{symbol}** shows normal behavior")
    else:
        st.warning("No fundamental results yet. Please run the fundamental analysis first.")

elif choice == progress_steps[3]:  # Technical Analysis
    set_step(4)
    st.header("📈 Enhanced Technical Analysis")
    
    selected_stocks = st.session_state.get('selected_stocks', [])
    if not selected_stocks:
        st.warning("Please select stocks first.")
    else:
        selected_stock = st.selectbox("Choose stock for technical analysis:", selected_stocks)
        
        if selected_stock:
            col1, col2 = st.columns([2, 1])
            
            with col1:
                create_enhanced_chart(selected_stock)
            
            with col2:
                st.subheader("Technical Indicators")
                
                with st.spinner("Calculating advanced indicators..."):
                    tech_analysis = analytics['technical_analyzer'].get_comprehensive_analysis(selected_stock)
                    
                    if tech_analysis:
                        # Basic indicators
                        st.write("**Basic Indicators:**")
                        basic = tech_analysis['basic_indicators']
                        for key, value in basic.items():
                            if isinstance(value, float):
                                st.metric(key, f"{value:.2f}")
                        
                        # Support/Resistance
                        st.write("**Support & Resistance:**")
                        sr = tech_analysis['support_resistance']
                        st.write(f"Current Price: ₹{sr['current_price']:.2f}")
                        if sr['resistance_levels']:
                            st.write(f"Resistance: {[f'₹{r:.2f}' for r in sr['resistance_levels']]}")
                        if sr['support_levels']:
                            st.write(f"Support: {[f'₹{s:.2f}' for s in sr['support_levels']]}")
                        
                        # Trend analysis
                        st.write("**Trend Analysis:**")
                        trend = tech_analysis['trend_analysis']
                        st.write(f"Direction: {trend['direction'].upper()}")
                        st.write(f"Strength: {trend['strength']:.2f}")
                        st.write(f"ADX: {trend['adx']:.2f}")

elif choice == progress_steps[4]:  # ML Predictions
    set_step(5)
    st.header("🤖 Machine Learning Predictions")
    
    selected_stocks = st.session_state.get('selected_stocks', [])
    if not selected_stocks:
        st.warning("Please select stocks first.")
    else:
        selected_stock = st.selectbox("Choose stock for ML prediction:", selected_stocks)
        prediction_days = st.slider("Prediction horizon (days):", 1, 30, 5)
        
        if st.button("🔮 Generate ML Prediction"):
            with st.spinner("Training ML models and generating predictions..."):
                prediction = analytics['ml_predictor'].predict_future_price(selected_stock, prediction_days)
                
                if prediction:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("Prediction Results")
                        current_price = prediction['current_price']
                        ensemble_pred = prediction['ensemble_prediction']
                        
                        st.metric(
                            "Current Price", 
                            f"₹{current_price:.2f}"
                        )
                        
                        st.metric(
                            f"Predicted Price ({prediction_days}d)",
                            f"₹{ensemble_pred['predicted_price']:.2f}",
                            f"{ensemble_pred['predicted_return']*100:.2f}%"
                        )
                        
                        # Confidence indicator
                        confidence = analytics['ml_predictor'].get_prediction_confidence(selected_stock)
                        st.metric("Model Confidence", f"{confidence*100:.1f}%")
                    
                    with col2:
                        st.subheader("Model Performance")
                        perf_df = pd.DataFrame(prediction['model_performance']).T
                        st.dataframe(perf_df)
                        
                        # Individual model predictions
                        st.subheader("Individual Models")
                        for model_name, pred_data in prediction['individual_models'].items():
                            st.write(f"**{model_name.title()}**: ₹{pred_data['predicted_price']:.2f} ({pred_data['predicted_return']*100:+.2f}%)")

elif choice == progress_steps[5]:  # Sentiment Analysis
    set_step(6)
    st.header("💭 Enhanced Sentiment Analysis")
    
    selected_stocks = st.session_state.get('selected_stocks', [])
    if not selected_stocks:
        st.warning("Please select stocks first.")
    else:
        # Market sentiment overview
        st.subheader("📊 Market Sentiment Overview")
        
        if st.button("🌡️ Analyze Market Sentiment"):
            with st.spinner("Analyzing market sentiment indicators..."):
                market_sentiment = analytics['sentiment_analyzer'].get_market_sentiment_indicators(selected_stocks)
                
                if market_sentiment:
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Momentum Signal", market_sentiment.get('momentum_signal', 'N/A'))
                    
                    with col2:
                        st.metric("Volatility Regime", market_sentiment.get('volatility_regime', 'N/A'))
                    
                    with col3:
                        st.metric("Market Breadth", market_sentiment.get('market_breadth', 'N/A'))
        
        st.markdown("---")
        
        # Individual stock sentiment
        st.subheader("📰 Individual Stock Sentiment")
        selected_stock = st.selectbox("Choose stock for sentiment analysis:", selected_stocks)
        
        if st.button("📈 Analyze Stock Sentiment"):
            with st.spinner(f"Analyzing sentiment for {selected_stock}..."):
                sentiment_result = analytics['sentiment_analyzer'].get_comprehensive_sentiment(selected_stock)
                
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    st.metric("Overall Sentiment", sentiment_result['overall_sentiment'].title())
                    st.metric("Sentiment Score", f"{sentiment_result['sentiment_score']:.3f}")
                    st.metric("News Articles", sentiment_result['news_count'])
                
                with col2:
                    # Sentiment breakdown
                    breakdown = sentiment_result['sentiment_breakdown']
                    if sum(breakdown.values()) > 0:
                        fig = go.Figure(data=[go.Pie(
                            labels=list(breakdown.keys()),
                            values=list(breakdown.values()),
                            hole=0.3
                        )])
                        fig.update_layout(title="Sentiment Distribution")
                        st.plotly_chart(fig, use_container_width=True)
                
                # Recent news
                if sentiment_result.get('recent_news'):
                    st.subheader("📰 Recent News")
                    for news in sentiment_result['recent_news']:
                        with st.expander(f"{news['source']}: {news['title'][:50]}..."):
                            st.write(news['description'])
                            st.caption(f"Published: {news['publishedAt']}")
                else:
                    st.info("No recent news found for this stock.")

elif choice == progress_steps[6]:  # Advanced Analytics
    set_step(7)
    st.header("🔬 Advanced Analytics Dashboard")
    
    selected_stocks = st.session_state.get('selected_stocks', [])
    if not selected_stocks:
        st.warning("Please select stocks first.")
    else:
        tab1, tab2, tab3 = st.tabs(["🎯 Stock Clustering", "⚠️ Risk Analysis", "🔍 Pattern Detection"])
        
        with tab1:
            st.subheader("Stock Clustering Analysis")
            
            if st.button("🎯 Cluster Stocks"):
                with st.spinner("Clustering stocks by characteristics..."):
                    clusters = analytics['stock_analytics'].cluster_stocks(selected_stocks)
                    
                    if clusters:
                        for cluster_id, stocks in clusters.items():
                            st.write(f"**Cluster {cluster_id + 1}:** {', '.join(stocks)}")
        
        with tab2:
            st.subheader("Risk Analysis")
            selected_stock = st.selectbox("Choose stock for risk analysis:", selected_stocks, key="risk_stock")
            
            if st.button("📊 Calculate Risk Metrics"):
                with st.spinner("Calculating comprehensive risk metrics..."):
                    risk_metrics = analytics['stock_analytics'].calculate_risk_metrics(selected_stock)
                    
                    if risk_metrics:
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.metric("Annual Return", f"{risk_metrics['annual_return']*100:.2f}%")
                            st.metric("Annual Volatility", f"{risk_metrics['annual_volatility']*100:.2f}%")
                            st.metric("Sharpe Ratio", f"{risk_metrics['sharpe_ratio']:.2f}")
                            st.metric("Beta", f"{risk_metrics['beta']:.2f}")
                        
                        with col2:
                            st.metric("Sortino Ratio", f"{risk_metrics['sortino_ratio']:.2f}")
                            st.metric("Max Drawdown", f"{risk_metrics['max_drawdown']*100:.2f}%")
                            st.metric("VaR (95%)", f"{risk_metrics['var_95']*100:.2f}%")
        
        with tab3:
            st.subheader("Pattern Detection")
            selected_stock = st.selectbox("Choose stock for pattern analysis:", selected_stocks, key="pattern_stock")
            
            if st.button("🔍 Detect Patterns"):
                with st.spinner("Detecting chart patterns..."):
                    tech_analysis = analytics['technical_analyzer'].get_comprehensive_analysis(selected_stock)
                    
                    if tech_analysis and 'patterns' in tech_analysis:
                        patterns = tech_analysis['patterns']
                        
                        for pattern_name, pattern_data in patterns.items():
                            if pattern_data['detected']:
                                st.success(f"**{pattern_name.replace('_', ' ').title()}** detected (Confidence: {pattern_data['confidence']:.2f})")
                            else:
                                st.info(f"No {pattern_name.replace('_', ' ')} pattern detected")

elif choice == progress_steps[7]:  # Summary Report
    set_step(8)
    st.header("📋 Comprehensive Analysis Report")
    
    selected_stocks = st.session_state.get('selected_stocks', [])
    if not selected_stocks:
        st.warning("Please select stocks first.")
    else:
        if st.button("📊 Generate Complete Report"):
            with st.spinner("Generating comprehensive analysis report..."):
                
                report_data = []
                
                for stock in selected_stocks[:5]:  # Limit to 5 stocks for demo
                    try:
                        # Get all analyses
                        tech_analysis = analytics['technical_analyzer'].get_comprehensive_analysis(stock)
                        risk_metrics = analytics['stock_analytics'].calculate_risk_metrics(stock)
                        sentiment = analytics['sentiment_analyzer'].get_comprehensive_sentiment(stock)
                        
                        stock_report = {
                            'Symbol': stock,
                            'RSI': tech_analysis['basic_indicators']['RSI'] if tech_analysis else 'N/A',
                            'MACD': tech_analysis['basic_indicators']['MACD'] if tech_analysis else 'N/A',
                            'Trend': tech_analysis['trend_analysis']['direction'] if tech_analysis else 'N/A',
                            'Annual Return': f"{risk_metrics['annual_return']*100:.2f}%" if risk_metrics else 'N/A',
                            'Volatility': f"{risk_metrics['annual_volatility']*100:.2f}%" if risk_metrics else 'N/A',
                            'Sharpe Ratio': f"{risk_metrics['sharpe_ratio']:.2f}" if risk_metrics else 'N/A',
                            'Sentiment': sentiment['overall_sentiment'].title(),
                            'News Count': sentiment['news_count']
                        }
                        
                        report_data.append(stock_report)
                        
                    except Exception as e:
                        st.error(f"Error analyzing {stock}: {e}")
                
                if report_data:
                    # Display summary table
                    report_df = pd.DataFrame(report_data)
                    st.dataframe(report_df, use_container_width=True)
                    
                    # Download option
                    csv = report_df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Report as CSV",
                        data=csv,
                        file_name=f"stock_analysis_report_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv"
                    )

# Sidebar info
st.sidebar.markdown("---")
st.sidebar.info("""
**Enhanced Features:**
- 🤖 Machine Learning Predictions
- 🔍 Anomaly Detection  
- 📊 Advanced Technical Analysis
- 💭 Multi-source Sentiment
- 🎯 Stock Clustering
- ⚠️ Risk Metrics
- 🔍 Pattern Recognition
""")

st.sidebar.markdown("---")
st.sidebar.caption("Enhanced Stock Screener v2.0")