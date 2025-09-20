import streamlit as st
import pandas as pd
import yfinance as yf

def run():
    st.header("Step 2: Fundamental Analysis & Scoring")

    symbols = st.session_state.get('symbols', [])
    if not symbols:
        st.warning("No symbols found. Please input stock symbols on the first page.")
        return

    extra_df = st.session_state.get('extra_data')

    results = []
    for sym in symbols:
        try:
            ticker = yf.Ticker(sym + ".NS")
            info = ticker.info

            row = {
                'symbol': sym,
                'company': info.get('shortName', ''),
                'current_price': info.get('currentPrice', None),
                'fifty_two_week_high': info.get('fiftyTwoWeekHigh', None),
                'avg_daily_volume': info.get('averageDailyVolume10Day', None),
                'beta': info.get('beta', None),
                'forward_pe': info.get('forwardPE', None),
            }

            # Merge extra data if available (capex, FCF, etc.)
            if extra_df is not None:
                match = extra_df[extra_df['symbol'].str.upper() == sym]
                if not match.empty:
                    for col in extra_df.columns:
                        if col.lower() != "symbol":
                            row[col.lower()] = match.iloc[0][col]

            # ----- Scoring rules (NO quarter-on-quarter topline growth) -----
            score = 0
            reason = []

            # 1. Capex increase in last 2 years (needs extra data)
            if 'capex_last_2y' in row and pd.notnull(row['capex_last_2y']):
                if row['capex_last_2y'] > 0:
                    score += 2
                    reason.append("Capex increased over 2 years (+2)")

            # 2. Free Cash Flow positive & <25% YoY growth (needs extra data)
            if 'free_cash_flow' in row and pd.notnull(row['free_cash_flow']):
                if row['free_cash_flow'] > 0 and ('fcf_yoy_growth' in row and pd.notnull(row['fcf_yoy_growth']) and row['fcf_yoy_growth'] < 25):
                    score += 2
                    reason.append("Free cash flow positive & <25% YoY growth (+2)")

            # 3. Forward PE < 20
            if row['forward_pe'] is not None and row['forward_pe'] < 20:
                score += 3
                reason.append("Forward PE < 20 (+3)")

            # 4. Beta between 1 and 3
            if row['beta'] is not None and 1 <= row['beta'] <= 3:
                score += 1
                reason.append("Beta 1-3 (+1)")

            # 5. Trading volume > 1 lakh/day
            if row['avg_daily_volume'] is not None and row['avg_daily_volume'] > 100000:
                score += 2
                reason.append("Volume > 1 lakh/day (+2)")

            # 6. Current price < 50% of 52-week high
            if (row['current_price'] is not None and row['fifty_two_week_high'] is not None and
                row['current_price'] < 0.5 * row['fifty_two_week_high']):
                score += 3
                reason.append("Price < 50% of 52-wk high (+3)")

            row['score'] = score
            row['score_reason'] = "; ".join(reason)
            results.append(row)

        except Exception as e:
            results.append({'symbol': sym, 'company': '', 'score': 0, 'score_reason': f"Error: {e}"})

    results = sorted(results, key=lambda x: x.get('score', 0), reverse=True)[:20]
    st.session_state['fundamental_results'] = results

    display_results(results)

def display_results(results):
    st.success(f"Top {len(results)} stocks based on your scoring model:")
    df = pd.DataFrame(results)
    cols = ['symbol', 'company', 'score', 'score_reason']
    extra_cols = [col for col in df.columns if col not in cols]
    st.dataframe(df[cols + extra_cols])
    st.write("You can proceed to the next step using the app sidebar.")