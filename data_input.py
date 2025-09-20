import streamlit as st
import pandas as pd

# --- Modern App Header and Welcome ---
st.markdown("""
# <span style='vertical-align: middle;'>📈</span> Indian Stock Screener
<small>Modern, actionable analytics for Indian equities</small>
""", unsafe_allow_html=True)

st.info("""
**How it works:**  
1. Paste NSE symbols or upload a CSV.  
2. Screen by fundamentals.  
3. Chart and analyze with technicals, sentiment, and 90-day projection.  
4. Download everything to Excel.
""")

st.markdown("---")

with st.expander("See Example Stock Symbols"):
    st.code("RELIANCE\nTCS\nINFY\nHDFCBANK\nASIANPAINT")

st.markdown(
    "<sub style='color:#888;'>This tool is for research/education. Not investment advice.</sub>", 
    unsafe_allow_html=True
)

# ---- Main Step 1 logic ----

def run():
    st.markdown("### Step 1: Enter Stock Symbols and Upload Data")

    st.write("Enter up to 100 Indian stock symbols (one per line), or upload a CSV file with a column named **symbol**.")

    # Paste symbols
    symbols_text = st.text_area(
        "Paste stock symbols (NSE/BSE, one per line):", 
        height=200, 
        key="symbols_text"
    )

    # Or upload CSV
    uploaded_file = st.file_uploader(
        "Or upload a CSV file of symbols (column name: 'symbol')", 
        type=["csv"], 
        key="symbols_csv"
    )

    # Handle symbols from text area or file
    symbols = []
    if symbols_text:
        symbols = [s.strip().upper() for s in symbols_text.splitlines() if s.strip()]
    elif uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            if 'symbol' in df.columns:
                symbols = df['symbol'].astype(str).str.strip().str.upper().tolist()
        except Exception as e:
            st.error(f"Could not read CSV: {e}")

    if not symbols:
        st.info("Please enter or upload at least one stock symbol.")
        st.stop()

    st.session_state['symbols'] = symbols

    st.success(f"Loaded {len(symbols)} stock symbol{'s' if len(symbols) != 1 else ''}.")

    # Optional extra data upload block
    st.markdown("### Optional: Upload extra company data (e.g., capex, free cash flow)")

# Only call run() from app.py, not at import
