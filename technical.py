# technical.py

import os
import streamlit as st
import pandas as pd
import yfinance as yf
import ta
import plotly.graph_objects as go
import numpy as np

def run():
    st.header("Step 4: Technical Analysis")

    selected_stocks = st.session_state.get('selected_stocks', [])
    if not selected_stocks:
        st.warning("No stocks selected. Please select stocks after fundamental screening.")
        return

    # --- Indicator options ---
    INDICATOR_LIST = [
        "RSI (14-day)", 
        "MACD", 
        "SMA (20-day)", 
        "SMA (50-day)", 
        "EMA (20-day)", 
        "Bollinger Bands", 
        "ADX (14-day)",
        "90-day Projection"   # <--- Added
    ]

    st.write("Choose up to 3 technical indicators to overlay on the chart.")
    indicators = st.multiselect(
        "Indicators:", 
        INDICATOR_LIST, 
        default=["RSI (14-day)", "MACD", "SMA (20-day)"],
        max_selections=3,
        key="tech_indicator_choice"
    )

    st.write("Select a stock to analyze:")
    selected = st.selectbox(
        "Stock:", 
        selected_stocks,
        key="selected_tech_stock"
    )

    window_days = st.radio("Chart window:", [90, 180], index=0)

    # Download price data
    try:
        df = yf.download(selected + ".NS", period=f"{window_days}d", interval="1d")
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = [col[0] for col in df.columns]
    except Exception as e:
        st.error(f"Error fetching price data for {selected}: {e}")
        return

    if df.empty:
        st.warning(f"No price data found for {selected}.")
        return

    results = {}

    # RSI
    if "RSI (14-day)" in indicators:
        close_series = df['Close']
        if len(close_series.shape) > 1:
            close_series = close_series.squeeze()
        df['rsi'] = ta.momentum.RSIIndicator(close_series, window=14).rsi()
        results['RSI'] = df['rsi'].iloc[-1]

    # MACD
    if "MACD" in indicators:
        close_series = df['Close']
        if len(close_series.shape) > 1:
            close_series = close_series.squeeze()
        macd = ta.trend.MACD(close_series)
        df['macd'] = macd.macd()
        results['MACD'] = df['macd'].iloc[-1]

    # SMA 20
    if "SMA (20-day)" in indicators:
        close_series = df['Close']
        if len(close_series.shape) > 1:
            close_series = close_series.squeeze()
        df['sma20'] = close_series.rolling(window=20).mean()
        results['SMA 20'] = df['sma20'].iloc[-1]

    # SMA 50
    if "SMA (50-day)" in indicators:
        close_series = df['Close']
        if len(close_series.shape) > 1:
            close_series = close_series.squeeze()
        df['sma50'] = close_series.rolling(window=50).mean()
        results['SMA 50'] = df['sma50'].iloc[-1]

    # EMA 20
    if "EMA (20-day)" in indicators:
        close_series = df['Close']
        if len(close_series.shape) > 1:
            close_series = close_series.squeeze()
        df['ema20'] = close_series.ewm(span=20, adjust=False).mean()
        results['EMA 20'] = df['ema20'].iloc[-1]

    # Bollinger Bands
    if "Bollinger Bands" in indicators:
        close_series = df['Close']
        if len(close_series.shape) > 1:
            close_series = close_series.squeeze()
        bb = ta.volatility.BollingerBands(close_series, window=20)
        df['bb_high'] = bb.bollinger_hband()
        df['bb_low'] = bb.bollinger_lband()
        results['BB High'] = df['bb_high'].iloc[-1]
        results['BB Low'] = df['bb_low'].iloc[-1]

    # ADX
    if "ADX (14-day)" in indicators:
        high_series = df['High']
        low_series = df['Low']
        close_series = df['Close']
        if len(high_series.shape) > 1:
            high_series = high_series.squeeze()
        if len(low_series.shape) > 1:
            low_series = low_series.squeeze()
        if len(close_series.shape) > 1:
            close_series = close_series.squeeze()
        df['adx'] = ta.trend.ADXIndicator(high_series, low_series, close_series, window=14).adx()
        results['ADX'] = df['adx'].iloc[-1]

    # 90-day Projection (Polynomial)
    proj_dates, proj_prices = None, None
    if "90-day Projection" in indicators:
        close_series = df['Close']
        if len(close_series.shape) > 1:
            close_series = close_series.squeeze()
        df_nonan = df.dropna(subset=['Close'])
        X = np.arange(len(df_nonan))
        y = df_nonan['Close'].values
        degree = 2  # Degree-2 polynomial
        coeffs = np.polyfit(X, y, degree)
        future_X = np.arange(len(df_nonan) + 90)
        proj = np.polyval(coeffs, future_X)
        proj_dates = pd.date_range(df_nonan.index[0], periods=len(df_nonan) + 90, freq='B')
        proj_prices = proj

    # --- Main Price Chart with overlays ---
    fig = go.Figure()

    # Candlestick trace
    fig.add_trace(go.Candlestick(
        x=df.index,
        open=df['Open'].values,
        high=df['High'].values,
        low=df['Low'].values,
        close=df['Close'].values,
        name='Price'
    ))

    # Overlay close price as a blue line
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['Close'].values,
        mode='lines',
        name='Close Price',
        line=dict(width=2, color='blue')
    ))

    # Overlay selected price overlays
    if "SMA (20-day)" in indicators:
        fig.add_trace(go.Scatter(x=df.index, y=df['sma20'].values, line=dict(width=1), name="SMA 20"))
    if "SMA (50-day)" in indicators:
        fig.add_trace(go.Scatter(x=df.index, y=df['sma50'].values, line=dict(width=1), name="SMA 50"))
    if "EMA (20-day)" in indicators:
        fig.add_trace(go.Scatter(x=df.index, y=df['ema20'].values, line=dict(width=1), name="EMA 20"))
    if "Bollinger Bands" in indicators:
        fig.add_trace(go.Scatter(x=df.index, y=df['bb_high'].values, line=dict(width=1, dash="dot"), name="BB High"))
        fig.add_trace(go.Scatter(x=df.index, y=df['bb_low'].values, line=dict(width=1, dash="dot"), name="BB Low"))
    # Projection overlay
    if "90-day Projection" in indicators and proj_dates is not None:
        fig.add_trace(go.Scatter(
            x=proj_dates,
            y=proj_prices,
            mode='lines',
            name='90-day Projection',
            line=dict(width=2, color='orange', dash='dash')
        ))

    fig.update_layout(
        title=f"{selected} - Price & Indicators ({window_days} days)",
        xaxis_title="Date",
        yaxis_title="Price",
        xaxis_rangeslider_visible=False
    )
    st.plotly_chart(fig, use_container_width=True)

    # ----- Show RSI, MACD, ADX as separate subcharts if selected -----
    if "RSI (14-day)" in indicators and 'rsi' in df:
        st.markdown("#### RSI (14-day)")
        st.line_chart(df['rsi'])

    if "MACD" in indicators and 'macd' in df:
        st.markdown("#### MACD")
        st.line_chart(df['macd'])

    if "ADX (14-day)" in indicators and 'adx' in df:
        st.markdown("#### ADX (14-day)")
        st.line_chart(df['adx'])

    # --- Technical indicator values and explanations ---
    st.markdown("### Technical Indicator Values")
    for ind, val in results.items():
        interp = interpret_indicator(ind, val)
        st.write(f"**{ind}**: {val:.2f} – {interp}")

    # --- Final Recommendation (Basic logic, expand as needed) ---
    final_rec, reason = simple_technical_recommendation(results)
    st.markdown(f"**Recommendation:** `{final_rec}`")
    st.write(f"Reason: {reason}")

    st.session_state['technical_results'] = {selected: {'results': results, 'rec': final_rec, 'reason': reason}}

def interpret_indicator(name, value):
    if "RSI" in name:
        if value > 70:
            return "Overbought (could signal SELL or caution)"
        elif value < 30:
            return "Oversold (could signal BUY opportunity)"
        else:
            return "Neutral"
    if "MACD" in name:
        if value > 0:
            return "Bullish momentum"
        elif value < 0:
            return "Bearish momentum"
        else:
            return "Neutral"
    if "ADX" in name:
        if value > 25:
            return "Strong trend"
        else:
            return "Weak/sideways"
    return "See overlay on price chart"

def simple_technical_recommendation(results):
    if "RSI" in results and results["RSI"] < 30:
        return "Buy", "RSI is oversold (<30)"
    if "RSI" in results and results["RSI"] > 70:
        return "Sell", "RSI is overbought (>70)"
    if "MACD" in results and results["MACD"] > 0:
        return "Buy", "MACD is positive (bullish momentum)"
    if "MACD" in results and results["MACD"] < 0:
        return "Sell", "MACD is negative (bearish momentum)"
    return "Hold", "Indicators are neutral or mixed"
