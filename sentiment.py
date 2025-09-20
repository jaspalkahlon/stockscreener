# sentiment.py

import os
from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import requests

api_key = os.getenv("HF_API_KEY")

def run():
    st.header("Step 5: Sentiment Analysis (News & Updates)")

    selected_stocks = st.session_state.get('selected_stocks', [])
    if not selected_stocks:
        st.warning("No stocks selected for sentiment analysis.")
        return

    st.write("For each stock, you can enter recent news, updates, or any custom text. We'll analyze the sentiment using HuggingFace's API.")

    sentiment_results = {}
    for stock in selected_stocks:
        user_input = st.text_area(f"Recent news/updates for {stock}:", height=80, key=f"news_{stock}")

        if user_input.strip():
            with st.spinner(f"Analyzing sentiment for {stock}..."):
                sentiment = get_sentiment(user_input)
                if sentiment is not None:
                    st.success(f"{stock} – **Sentiment:** {sentiment['label'].capitalize()} (Score: {sentiment['score']:.2f})")
                    st.caption(sentiment['explanation'])
                    sentiment_results[stock] = sentiment
                else:
                    st.error(f"Could not analyze sentiment for {stock}.")
        else:
            st.info(f"Enter news or updates for {stock} to analyze.")

    st.session_state['sentiment_results'] = sentiment_results

def get_sentiment(text):
    if not api_key:
        st.error("HuggingFace API key not found in environment variables.")
        return None

    url = "https://api-inference.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2-english"
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {"inputs": text}

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=20)
        # Debug: Show raw response
        st.write("DEBUG - HuggingFace response.text:", response.text)
        result = response.json()

        if isinstance(result, list) and len(result) > 0:
            result = result[0]
        elif isinstance(result, dict) and 'error' in result:
            st.write(f"DEBUG - HuggingFace error: {result['error']}")
            return None

        label = result[0]['label'] if isinstance(result, list) and len(result) > 0 else None
        score = result[0]['score'] if isinstance(result, list) and len(result) > 0 else None

        explanation = interpret_sentiment(label, score)

        return {"label": label.lower(), "score": score, "explanation": explanation}
    except Exception as e:
        st.write(f"Sentiment API error: {e}")
        return None

def interpret_sentiment(label, score):
    if label == "POSITIVE":
        if score > 0.8:
            return "Very positive news—could boost confidence in the stock."
        elif score > 0.6:
            return "Positive news—likely to be seen as good."
        else:
            return "Mildly positive news."
    elif label == "NEGATIVE":
        if score > 0.8:
            return "Very negative news—could signal caution or selling."
        elif score > 0.6:
            return "Negative news—could weigh on sentiment."
        else:
            return "Mildly negative news."
    return "Neutral or mixed news."
