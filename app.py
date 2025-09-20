# app.py
import streamlit as st
import os
from dotenv import load_dotenv

# 1. Load environment variables from .env securely
load_dotenv()

# 2. Import your custom modules
import data_input
import fundamental
import technical
import sentiment

# 3. App-wide Streamlit settings
st.set_page_config(
    page_title="Indian Stock Screener (90-Day Horizon)",
    layout="wide",
)

# 4. Session state initialization
if 'step' not in st.session_state:
    st.session_state['step'] = 1
if 'symbols' not in st.session_state:
    st.session_state['symbols'] = []
if 'fundamental_results' not in st.session_state:
    st.session_state['fundamental_results'] = []
if 'selected_stocks' not in st.session_state:
    st.session_state['selected_stocks'] = []
if 'technical_results' not in st.session_state:
    st.session_state['technical_results'] = []
if 'sentiment_results' not in st.session_state:
    st.session_state['sentiment_results'] = []

# 5. Page navigation logic
menu = [
    "1. Input Stocks & Data",
    "2. Fundamental Analysis",
    "3. Select Stocks for Technical/Sentiment",
    "4. Technical/Sentiment & Charts",
]

st.sidebar.title("App Navigation")
choice = st.sidebar.radio("Go to:", menu, index=st.session_state['step'] - 1)

# 6. Navigation control (keeps step in sync)
def set_step(n):
    st.session_state['step'] = n

# 7. Page logic
if choice == menu[0]:
    set_step(1)
    data_input.run()

elif choice == menu[1]:
    set_step(2)
    fundamental.run()

elif choice == menu[2]:
    set_step(3)
    # A page to select from filtered stocks (for technicals/sentiment)
    if st.session_state['fundamental_results']:
        st.write("Select stocks for technical and sentiment analysis:")
        selected = st.multiselect(
            "Choose stocks:",
            [row['symbol'] for row in st.session_state['fundamental_results']],
            default=[row['symbol'] for row in st.session_state['fundamental_results']]
        )
        st.session_state['selected_stocks'] = selected
        if st.button("Proceed to Technical/Sentiment Analysis"):
            set_step(4)
            st.rerun()
    else:
        st.warning("No fundamental results yet. Please run the fundamental analysis first.")

elif choice == menu[3]:
    set_step(4)
    if st.session_state['selected_stocks']:
        technical.run()
        sentiment.run()
    else:
        st.warning("Please select stocks on the previous page first.")

elif choice == menu[4]:
    set_step(5)
    st.info("Use the built-in Streamlit table/chart download buttons to export your results. (No separate export module is needed.)")

else:
    st.write("Invalid page. Please select from the sidebar.")

# 8. Helpful instructions (can expand with more guidance as app grows)
st.sidebar.markdown("---")
st.sidebar.info("""
1. Input your stock symbols and any manual data.
2. Run fundamental analysis to filter candidates.
3. Select stocks for further analysis.
4. View technicals, sentiment, and interactive charts.
""")
