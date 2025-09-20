# simple_app.py - Clean, User-Friendly Stock Screener
import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# Import our modules
from advanced_analytics import StockAnalytics
from enhanced_sentiment import EnhancedSentimentAnalyzer
from ml_predictions import MLPredictor
from enhanced_technical import EnhancedTechnicalAnalysis

# Page config
st.set_page_config(
    page_title="Indian Stock Screener",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize analytics
@st.cache_resource
def get_analytics():
    return {
        'stock_analytics': StockAnalytics(),
        'sentiment_analyzer': EnhancedSentimentAnalyzer(),
        'ml_predictor': MLPredictor(),
        'technical_analyzer': EnhancedTechnicalAnalysis()
    }

analytics = get_analytics()

# Session state
if 'current_step' not in st.session_state:
    st.session_state.current_step = 1
if 'stocks_data' not in st.session_state:
    st.session_state.stocks_data = {}

# Header
st.title("🚀 Indian Stock Screener")
st.markdown("**Professional stock analysis with AI-powered insights**")

# Progress bar
steps = ["📊 Enter Stocks", "🔍 Analysis", "📈 Results", "📋 Report"]
current = st.session_state.current_step
cols = st.columns(4)
for i, step in enumerate(steps):
    with cols[i]:
        if i + 1 <= current:
            st.success(f"✅ {step}")
        elif i + 1 == current:
            st.info(f"🔄 {step}")
        else:
            st.write(f"⏳ {step}")

st.markdown("---")

# Step 1: Enter Stocks
if st.session_state.current_step == 1:
    st.header("📊 Step 1: Enter Stock Symbols")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.write("Enter Indian stock symbols (NSE format):")
        
        # Sample stocks
        sample_stocks = "RELIANCE\nTCS\nINFY\nHDFCBANK\nICICIBANK"
        
        # Stock input with Enter key support
        stocks_input = st.text_area(
            "Stock symbols (one per line):",
            value=sample_stocks,
            height=150,
            help="Enter NSE stock symbols like RELIANCE, TCS, INFY etc. Press Ctrl+Enter to analyze.",
            key="stocks_input"
        )
        
        # Add individual stock input with Enter key
        st.write("**Or add stocks one by one:**")
        col_input, col_add = st.columns([3, 1])
        
        with col_input:
            new_stock = st.text_input(
                "Add single stock:",
                placeholder="e.g., RELIANCE",
                key="single_stock_input"
            )
        
        with col_add:
            st.write("")  # Spacing
            if st.button("➕ Add", key="add_stock_btn") or (new_stock and st.session_state.get('add_stock_enter', False)):
                if new_stock.strip():
                    current_stocks = stocks_input.split('\n') if stocks_input else []
                    if new_stock.upper().strip() not in [s.strip().upper() for s in current_stocks]:
                        current_stocks.append(new_stock.upper().strip())
                        st.session_state.stocks_input = '\n'.join(current_stocks)
                        st.rerun()
                    else:
                        st.warning(f"{new_stock.upper()} already added!")
        
        # Handle Enter key for single stock input - simplified approach
        if new_stock and new_stock.strip():
            # Check if this is a new input (different from last processed)
            if new_stock.upper().strip() != st.session_state.get('last_processed_stock', ''):
                current_stocks = stocks_input.split('\n') if stocks_input else []
                new_symbol = new_stock.upper().strip()
                
                if new_symbol not in [s.strip().upper() for s in current_stocks]:
                    current_stocks.append(new_symbol)
                    st.session_state.stocks_input = '\n'.join(current_stocks)
                    st.session_state.last_processed_stock = new_symbol
                    st.session_state.single_stock_input = ""  # Clear the input
                    st.success(f"✅ Added {new_symbol}")
                    st.rerun()
                else:
                    st.warning(f"⚠️ {new_symbol} already in list!")
                    st.session_state.last_processed_stock = new_symbol
        
        if st.button("🚀 Start Analysis", type="primary", use_container_width=True):
            if stocks_input.strip():
                symbols = [s.strip().upper() for s in stocks_input.split('\n') if s.strip()]
                st.session_state.stocks_data['symbols'] = symbols
                st.session_state.current_step = 2
                st.rerun()
            else:
                st.error("Please enter at least one stock symbol")
    
    with col2:
        st.info("""
        **How to use:**
        1. Enter stock symbols (one per line)
        2. Use NSE format (e.g., RELIANCE, TCS)
        3. Click 'Start Analysis'
        
        **Popular stocks:**
        - RELIANCE (Reliance Industries)
        - TCS (Tata Consultancy)
        - INFY (Infosys)
        - HDFCBANK (HDFC Bank)
        - ICICIBANK (ICICI Bank)
        """)

# Step 2: Analysis
elif st.session_state.current_step == 2:
    st.header("🔍 Step 2: Running Analysis")
    
    symbols = st.session_state.stocks_data.get('symbols', [])
    
    if not symbols:
        st.error("No stocks found. Please go back to Step 1.")
        if st.button("← Back to Step 1"):
            st.session_state.current_step = 1
            st.rerun()
    else:
        st.write(f"Analyzing {len(symbols)} stocks: {', '.join(symbols)}")
        
        # Progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        results = {}
        
        for i, symbol in enumerate(symbols):
            status_text.text(f"Analyzing {symbol}...")
            progress_bar.progress((i + 1) / len(symbols))
            
            try:
                # Get basic stock info
                ticker = yf.Ticker(symbol + ".NS")
                info = ticker.info
                hist = ticker.history(period="6mo")
                
                if not hist.empty:
                    current_price = hist['Close'].iloc[-1]
                    
                    # Calculate basic metrics
                    returns = hist['Close'].pct_change().dropna()
                    volatility = returns.std() * np.sqrt(252) * 100
                    
                    # Get technical analysis with error handling
                    try:
                        tech_analysis = analytics['technical_analyzer'].get_comprehensive_analysis(symbol)
                    except Exception as e:
                        tech_analysis = None
                        st.warning(f"Technical analysis failed for {symbol}: {e}")
                    
                    # Get risk metrics with error handling
                    try:
                        risk_metrics = analytics['stock_analytics'].calculate_risk_metrics(symbol)
                    except Exception as e:
                        risk_metrics = None
                        st.warning(f"Risk analysis failed for {symbol}: {e}")
                    
                    results[symbol] = {
                        'name': info.get('shortName', symbol),
                        'current_price': current_price,
                        'volatility': volatility,
                        'market_cap': info.get('marketCap', 0),
                        'pe_ratio': info.get('forwardPE', 0),
                        'tech_analysis': tech_analysis,
                        'risk_metrics': risk_metrics,
                        'data': hist
                    }
                else:
                    results[symbol] = {'error': 'No data available'}
                    
            except Exception as e:
                results[symbol] = {'error': str(e)}
        
        st.session_state.stocks_data['results'] = results
        status_text.text("✅ Analysis complete!")
        progress_bar.progress(1.0)
        
        if st.button("📈 View Results", type="primary"):
            st.session_state.current_step = 3
            st.rerun()

# Step 3: Results
elif st.session_state.current_step == 3:
    st.header("📈 Step 3: Analysis Results")
    
    results = st.session_state.stocks_data.get('results', {})
    
    if not results:
        st.error("No results found. Please run analysis first.")
        if st.button("← Back to Analysis"):
            st.session_state.current_step = 2
            st.rerun()
    else:
        # Summary table
        st.subheader("📊 Stock Summary")
        
        summary_data = []
        for symbol, data in results.items():
            if 'error' not in data:
                summary_data.append({
                    'Symbol': symbol,
                    'Company': data['name'],
                    'Price (₹)': f"{data['current_price']:.2f}",
                    'Volatility (%)': f"{data['volatility']:.1f}",
                    'PE Ratio': f"{data['pe_ratio']:.1f}" if data['pe_ratio'] else 'N/A',
                    'Market Cap (Cr)': f"{data['market_cap']/10000000:.0f}" if data['market_cap'] else 'N/A'
                })
        
        if summary_data:
            df_summary = pd.DataFrame(summary_data)
            st.dataframe(df_summary, use_container_width=True)
            
            # Individual stock analysis
            st.subheader("🔍 Detailed Analysis")
            
            selected_stock = st.selectbox(
                "Choose a stock for detailed analysis:",
                [s for s in results.keys() if 'error' not in results[s]]
            )
            
            if selected_stock and 'error' not in results[selected_stock]:
                stock_data = results[selected_stock]
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("Current Price", f"₹{stock_data['current_price']:.2f}")
                    st.metric("Volatility", f"{stock_data['volatility']:.1f}%")
                    
                    # Risk metrics
                    if stock_data['risk_metrics']:
                        risk = stock_data['risk_metrics']
                        st.metric("Sharpe Ratio", f"{risk.get('sharpe_ratio', 0):.2f}")
                        st.metric("Max Drawdown", f"{risk.get('max_drawdown', 0)*100:.1f}%")
                
                with col2:
                    # Price chart
                    hist_data = stock_data['data']
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=hist_data.index,
                        y=hist_data['Close'],
                        mode='lines',
                        name='Price',
                        line=dict(color='#1f77b4', width=2)
                    ))
                    fig.update_layout(
                        title=f"{selected_stock} - Price Chart",
                        xaxis_title="Date",
                        yaxis_title="Price (₹)",
                        height=300
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                # Technical indicators with better error handling
                if stock_data.get('tech_analysis'):
                    st.subheader("📊 Technical Indicators")
                    tech = stock_data['tech_analysis']
                    
                    if isinstance(tech, dict) and 'basic_indicators' in tech:
                        basic = tech['basic_indicators']
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            rsi_val = basic.get('RSI', 0)
                            if isinstance(rsi_val, (int, float)):
                                st.metric("RSI", f"{rsi_val:.1f}")
                            else:
                                st.metric("RSI", "N/A")
                        with col2:
                            macd_val = basic.get('MACD', 0)
                            if isinstance(macd_val, (int, float)):
                                st.metric("MACD", f"{macd_val:.3f}")
                            else:
                                st.metric("MACD", "N/A")
                        with col3:
                            bb_val = basic.get('BB_Position', 0)
                            if isinstance(bb_val, (int, float)):
                                st.metric("BB Position", f"{bb_val:.2f}")
                            else:
                                st.metric("BB Position", "N/A")
                else:
                    st.info("Technical analysis not available for this stock")
                
                # ML Prediction
                st.subheader("🤖 AI Price Prediction")
                
                if st.button(f"🔮 Predict {selected_stock} Price (5 days)", key=f"predict_{selected_stock}"):
                    with st.spinner("Running AI models..."):
                        prediction = analytics['ml_predictor'].predict_future_price(selected_stock, 5)
                        
                        if prediction:
                            current = prediction['current_price']
                            predicted = prediction['ensemble_prediction']['predicted_price']
                            change_pct = (predicted - current) / current * 100
                            
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Current Price", f"₹{current:.2f}")
                            with col2:
                                st.metric("Predicted Price (5d)", f"₹{predicted:.2f}")
                            with col3:
                                st.metric("Expected Change", f"{change_pct:+.1f}%")
                        else:
                            st.error("Could not generate prediction for this stock")
                
                # Sentiment Analysis
                st.subheader("💭 Sentiment Analysis")
                
                if st.button(f"📰 Analyze {selected_stock} Sentiment", key=f"sentiment_{selected_stock}"):
                    with st.spinner("Analyzing news sentiment..."):
                        try:
                            sentiment_result = analytics['sentiment_analyzer'].get_comprehensive_sentiment(selected_stock)
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                st.metric("Overall Sentiment", sentiment_result['overall_sentiment'].title())
                                st.metric("Sentiment Score", f"{sentiment_result['sentiment_score']:.3f}")
                            with col2:
                                st.metric("News Articles", sentiment_result['news_count'])
                                
                                # Sentiment breakdown pie chart
                                breakdown = sentiment_result['sentiment_breakdown']
                                if sum(breakdown.values()) > 0:
                                    fig = go.Figure(data=[go.Pie(
                                        labels=list(breakdown.keys()),
                                        values=list(breakdown.values()),
                                        hole=0.3
                                    )])
                                    fig.update_layout(title="Sentiment Distribution", height=250)
                                    st.plotly_chart(fig, use_container_width=True)
                        except Exception as e:
                            st.error(f"Sentiment analysis error: {str(e)}")
        
        # Navigation
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Back to Analysis"):
                st.session_state.current_step = 2
                st.rerun()
        with col2:
            if st.button("📋 Generate Report", type="primary"):
                st.session_state.current_step = 4
                st.rerun()

# Step 4: Report
elif st.session_state.current_step == 4:
    st.header("📋 Step 4: Final Report")
    
    results = st.session_state.stocks_data.get('results', {})
    
    if results:
        # Generate downloadable report
        report_data = []
        for symbol, data in results.items():
            if 'error' not in data:
                report_data.append({
                    'Symbol': symbol,
                    'Company': data['name'],
                    'Current_Price': data['current_price'],
                    'Volatility_Percent': data['volatility'],
                    'PE_Ratio': data['pe_ratio'],
                    'Market_Cap_Cr': data['market_cap']/10000000 if data['market_cap'] else 0
                })
        
        if report_data:
            df_report = pd.DataFrame(report_data)
            
            st.subheader("📊 Complete Analysis Report")
            st.dataframe(df_report, use_container_width=True)
            
            # Download button
            csv = df_report.to_csv(index=False)
            st.download_button(
                label="📥 Download Report (CSV)",
                data=csv,
                file_name=f"stock_analysis_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                type="primary"
            )
            
            st.success("✅ Analysis complete! Your report is ready for download.")
    
    # Start over
    if st.button("🔄 Analyze New Stocks", type="secondary"):
        # Clear session state
        for key in list(st.session_state.keys()):
            if key.startswith('stocks_data') or key == 'current_step':
                del st.session_state[key]
        st.session_state.current_step = 1
        st.rerun()

# Sidebar info
st.sidebar.markdown("---")
st.sidebar.info("""
**🚀 Enhanced Features:**
- Real-time stock data
- AI-powered predictions
- Technical analysis
- Sentiment analysis
- Risk metrics
- Downloadable reports
""")

st.sidebar.markdown("---")
st.sidebar.caption("Indian Stock Screener v2.0")