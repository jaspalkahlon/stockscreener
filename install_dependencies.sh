#!/bin/bash

# install_dependencies.sh - Install all required dependencies for stock screener

echo "🚀 Installing Stock Screener Dependencies..."

# Update pip first
echo "📦 Updating pip..."
python3 -m pip install --upgrade pip

# Core dependencies
echo "📊 Installing core dependencies..."
pip3 install streamlit yfinance plotly pandas numpy requests

# Optional advanced dependencies
echo "🔬 Installing advanced analytics dependencies..."
pip3 install scipy scikit-learn beautifulsoup4 lxml

# NLP dependencies for sentiment analysis
echo "💭 Installing NLP dependencies..."
pip3 install nltk textblob vaderSentiment

# Additional useful packages
echo "⚡ Installing additional packages..."
pip3 install ta-lib || echo "⚠️ ta-lib installation failed (optional)"
pip3 install python-dateutil pytz

echo "✅ Installation complete!"
echo ""
echo "🧪 Testing installation..."
python3 -c "
import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
import numpy as np
print('✅ Core packages working!')

try:
    import scipy
    print('✅ SciPy available')
except ImportError:
    print('⚠️ SciPy not available (some advanced features disabled)')

try:
    import sklearn
    print('✅ Scikit-learn available')
except ImportError:
    print('⚠️ Scikit-learn not available (some ML features disabled)')

try:
    import nltk
    print('✅ NLTK available')
except ImportError:
    print('⚠️ NLTK not available (some sentiment features disabled)')
"

echo ""
echo "🎯 Ready to run apps:"
echo "streamlit run clean_app.py --server.port 8501 --server.address 0.0.0.0"
echo "streamlit run simple_app.py --server.port 8501 --server.address 0.0.0.0"
echo "streamlit run enhanced_app.py --server.port 8501 --server.address 0.0.0.0"