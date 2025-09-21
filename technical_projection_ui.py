# technical_projection_ui.py
import streamlit as st
import pandas as pd
from enhanced_technical import EnhancedTechnicalAnalysis
from datetime import datetime, timedelta

def run_technical_projection():
    """Streamlit UI for technical analysis with projections"""
    
    st.header("📈 Technical Analysis with Price Projections")
    st.markdown("---")
    
    # Initialize technical analyzer
    if 'tech_analyzer' not in st.session_state:
        st.session_state.tech_analyzer = EnhancedTechnicalAnalysis()
    
    tech_analyzer = st.session_state.tech_analyzer
    
    # Stock input
    col1, col2 = st.columns([2, 1])
    
    with col1:
        symbol = st.text_input(
            "Enter Stock Symbol (NSE format):",
            value="RELIANCE",
            help="Enter stock symbol without .NS suffix (e.g., RELIANCE, TCS, INFY)"
        )
    
    with col2:
        # Projection days slider
        projection_days = st.slider(
            "Projection Days:",
            min_value=1,
            max_value=30,
            value=15,
            help="Number of days to project into the future"
        )
    
    if not symbol:
        st.warning("Please enter a stock symbol")
        return
    
    # Analysis options
    st.markdown("### Analysis Options")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        show_projections = st.checkbox("Show Price Projections", value=True)
        show_technical = st.checkbox("Show Technical Indicators", value=True)
    
    with col2:
        show_patterns = st.checkbox("Show Pattern Analysis", value=True)
        show_volume = st.checkbox("Show Volume Analysis", value=True)
    
    with col3:
        projection_methods = st.multiselect(
            "Projection Methods:",
            ["trend", "ma_based", "sr_based", "volatility", "ensemble"],
            default=["ensemble", "trend", "sr_based"],
            help="Select which projection methods to display"
        )
    
    # Run analysis button
    if st.button("🔍 Analyze Stock", type="primary"):
        
        with st.spinner(f"Analyzing {symbol}..."):
            try:
                # Get comprehensive analysis
                analysis = tech_analyzer.get_comprehensive_analysis(symbol)
                
                if analysis is None:
                    st.error(f"Could not fetch data for {symbol}. Please check the symbol and try again.")
                    return
                
                # Create projection chart
                if show_projections:
                    fig, projections = tech_analyzer.create_projection_chart(symbol, projection_days)
                    
                    if fig is not None:
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Display projection summary
                        st.markdown("### 📊 Projection Summary")
                        
                        # Filter projections based on user selection
                        filtered_projections = {k: v for k, v in projections.items() 
                                              if k in projection_methods}
                        
                        if filtered_projections:
                            proj_cols = st.columns(len(filtered_projections))
                            
                            for i, (method, proj) in enumerate(filtered_projections.items()):
                                with proj_cols[i]:
                                    current_price = proj['prices'][0] if len(proj['prices']) > 0 else 0
                                    final_price = proj['prices'][-1] if len(proj['prices']) > 0 else 0
                                    price_change = ((final_price - current_price) / current_price * 100) if current_price > 0 else 0
                                    
                                    st.metric(
                                        label=f"{proj['method']}",
                                        value=f"₹{final_price:.2f}",
                                        delta=f"{price_change:+.2f}%"
                                    )
                    else:
                        st.error("Could not generate projection chart")
                
                # Technical indicators summary
                if show_technical and analysis:
                    st.markdown("### 🔧 Technical Indicators")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown("**Basic Indicators**")
                        basic = analysis.get('basic_indicators', {})
                        
                        rsi = basic.get('RSI', 50)
                        rsi_signal = "Overbought" if rsi > 70 else "Oversold" if rsi < 30 else "Neutral"
                        st.metric("RSI", f"{rsi:.1f}", rsi_signal)
                        
                        macd = basic.get('MACD', 0)
                        macd_signal = basic.get('MACD_Signal', 0)
                        macd_trend = "Bullish" if macd > macd_signal else "Bearish"
                        st.metric("MACD", f"{macd:.3f}", macd_trend)
                    
                    with col2:
                        st.markdown("**Advanced Indicators**")
                        advanced = analysis.get('advanced_indicators', {})
                        
                        stoch_k = advanced.get('Stochastic_K', 50)
                        stoch_signal = "Overbought" if stoch_k > 80 else "Oversold" if stoch_k < 20 else "Neutral"
                        st.metric("Stochastic %K", f"{stoch_k:.1f}", stoch_signal)
                        
                        williams_r = advanced.get('Williams_R', -50)
                        williams_signal = "Overbought" if williams_r > -20 else "Oversold" if williams_r < -80 else "Neutral"
                        st.metric("Williams %R", f"{williams_r:.1f}", williams_signal)
                    
                    with col3:
                        st.markdown("**Trend Analysis**")
                        trend = analysis.get('trend_analysis', {})
                        
                        direction = trend.get('direction', 'neutral').title()
                        strength = trend.get('strength', 0.5)
                        st.metric("Trend Direction", direction, f"Strength: {strength:.2f}")
                        
                        adx = trend.get('adx', 25)
                        adx_signal = "Strong" if adx > 40 else "Weak" if adx < 20 else "Moderate"
                        st.metric("ADX", f"{adx:.1f}", adx_signal)
                
                # Support and Resistance
                if analysis:
                    sr_data = analysis.get('support_resistance', {})
                    if sr_data:
                        st.markdown("### 📊 Support & Resistance Levels")
                        
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            current_price = sr_data.get('current_price', 0)
                            st.metric("Current Price", f"₹{current_price:.2f}")
                        
                        with col2:
                            resistance_levels = sr_data.get('resistance_levels', [])
                            if resistance_levels:
                                nearest_resistance = resistance_levels[0]
                                resistance_distance = ((nearest_resistance - current_price) / current_price * 100) if current_price > 0 else 0
                                st.metric("Nearest Resistance", f"₹{nearest_resistance:.2f}", f"{resistance_distance:+.1f}%")
                        
                        with col3:
                            support_levels = sr_data.get('support_levels', [])
                            if support_levels:
                                nearest_support = support_levels[0]
                                support_distance = ((nearest_support - current_price) / current_price * 100) if current_price > 0 else 0
                                st.metric("Nearest Support", f"₹{nearest_support:.2f}", f"{support_distance:+.1f}%")
                
                # Pattern Analysis
                if show_patterns and analysis:
                    patterns = analysis.get('patterns', {})
                    if patterns:
                        st.markdown("### 🔍 Pattern Analysis")
                        
                        pattern_found = False
                        for pattern_name, pattern_data in patterns.items():
                            if isinstance(pattern_data, dict) and pattern_data.get('detected', False):
                                confidence = pattern_data.get('confidence', 0)
                                st.success(f"**{pattern_name.replace('_', ' ').title()}** detected with {confidence:.1%} confidence")
                                pattern_found = True
                        
                        if not pattern_found:
                            st.info("No significant patterns detected in current timeframe")
                
                # Volume Analysis
                if show_volume and analysis:
                    volume_data = analysis.get('volume_analysis', {})
                    if volume_data:
                        st.markdown("### 📊 Volume Analysis")
                        
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            vol_ratio = volume_data.get('current_vs_average', 1)
                            vol_signal = "High" if vol_ratio > 1.5 else "Low" if vol_ratio < 0.5 else "Normal"
                            st.metric("Volume vs Average", f"{vol_ratio:.2f}x", vol_signal)
                        
                        with col2:
                            vol_trend = volume_data.get('volume_trend', 'neutral')
                            st.metric("Volume Trend", vol_trend.title())
                        
                        with col3:
                            obv_trend = volume_data.get('obv_trend', 'neutral')
                            st.metric("OBV Trend", obv_trend.title())
                
                # Trading Insights
                st.markdown("### 💡 Trading Insights")
                
                insights = []
                
                if analysis:
                    # RSI insights
                    rsi = analysis.get('basic_indicators', {}).get('RSI', 50)
                    if rsi > 70:
                        insights.append("🔴 RSI indicates overbought conditions - consider taking profits")
                    elif rsi < 30:
                        insights.append("🟢 RSI indicates oversold conditions - potential buying opportunity")
                    
                    # Trend insights
                    trend = analysis.get('trend_analysis', {})
                    if trend.get('direction') == 'up' and trend.get('strength', 0) > 0.7:
                        insights.append("📈 Strong uptrend detected - momentum is positive")
                    elif trend.get('direction') == 'down' and trend.get('strength', 0) > 0.7:
                        insights.append("📉 Strong downtrend detected - caution advised")
                    
                    # Volume insights
                    volume_data = analysis.get('volume_analysis', {})
                    if volume_data.get('volume_breakout', False):
                        insights.append("🚀 Volume breakout detected - significant price movement likely")
                    
                    # Support/Resistance insights
                    sr_data = analysis.get('support_resistance', {})
                    current_price = sr_data.get('current_price', 0)
                    resistance_levels = sr_data.get('resistance_levels', [])
                    support_levels = sr_data.get('support_levels', [])
                    
                    if resistance_levels and current_price > 0:
                        nearest_resistance = resistance_levels[0]
                        if (nearest_resistance - current_price) / current_price < 0.02:  # Within 2%
                            insights.append("⚠️ Price approaching resistance level - watch for reversal")
                    
                    if support_levels and current_price > 0:
                        nearest_support = support_levels[0]
                        if (current_price - nearest_support) / current_price < 0.02:  # Within 2%
                            insights.append("⚠️ Price approaching support level - watch for bounce or breakdown")
                
                if insights:
                    for insight in insights:
                        st.info(insight)
                else:
                    st.info("📊 Market conditions appear neutral - monitor for clearer signals")
                
                # Disclaimer
                st.markdown("---")
                st.caption("⚠️ **Disclaimer**: This analysis is for educational purposes only and should not be considered as financial advice. Always consult with a qualified financial advisor before making investment decisions.")
                
            except Exception as e:
                st.error(f"An error occurred during analysis: {str(e)}")
                st.info("Please try again or contact support if the issue persists.")

if __name__ == "__main__":
    run_technical_projection()