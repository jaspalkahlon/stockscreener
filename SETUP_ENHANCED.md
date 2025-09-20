# Enhanced Stock Screener Setup Guide

## 🚀 New Features Added

### 1. Machine Learning Predictions
- **Random Forest, Gradient Boosting, Linear Regression** models
- **Feature Engineering**: 30+ technical and fundamental features
- **Ensemble Predictions**: Combines multiple models for better accuracy
- **Confidence Scoring**: Model agreement-based confidence metrics

### 2. Advanced Sentiment Analysis
- **Multi-source News**: NewsAPI, Reddit integration
- **Dual Analysis**: TextBlob + VADER sentiment engines
- **Market Sentiment**: Volatility regime, momentum, breadth indicators
- **Free Options**: Works without API keys using Reddit and TextBlob

### 3. Enhanced Technical Analysis
- **Advanced Indicators**: Stochastic, Williams %R, CCI, ATR, Parabolic SAR, MFI
- **Pattern Recognition**: Double tops/bottoms, triangles, flags
- **Support/Resistance**: Automated level detection
- **Volume Analysis**: OBV, volume breakouts, trend analysis

### 4. Advanced Analytics
- **Anomaly Detection**: Isolation Forest for unusual stock behavior
- **Stock Clustering**: K-means clustering by characteristics
- **Risk Metrics**: Sharpe, Sortino, VaR, Maximum Drawdown, Beta
- **Trend Analysis**: Multi-method trend strength and direction

## 📦 Installation

### 1. Install Required Packages
```bash
pip install -r requirements.txt
```

### 2. Optional API Keys (for enhanced features)

#### NewsAPI (Free tier: 100 requests/day)
1. Sign up at https://newsapi.org/
2. Get your free API key
3. Add to `.env` file:
```
NEWSAPI_KEY=your_newsapi_key_here
```

#### HuggingFace (for advanced sentiment - optional)
1. Sign up at https://huggingface.co/
2. Get your API token
3. Add to `.env` file:
```
HF_API_KEY=your_huggingface_token_here
```

### 3. Run Enhanced Application
```bash
# Run the enhanced version
streamlit run enhanced_app.py

# Or run the original version
streamlit run app.py
```

## 🎯 Usage Guide

### Step-by-Step Workflow

1. **📊 Input & Data**: Enter stock symbols or upload CSV
2. **🔍 Fundamental Analysis**: Screen stocks using scoring model
3. **🎯 Stock Selection**: Choose stocks for advanced analysis
4. **📈 Technical Analysis**: View enhanced charts and indicators
5. **🤖 ML Predictions**: Get AI-powered price predictions
6. **💭 Sentiment Analysis**: Analyze news and market sentiment
7. **🔬 Advanced Analytics**: Clustering, risk analysis, patterns
8. **📋 Summary Report**: Generate comprehensive report

### Key Features Explained

#### Machine Learning Predictions
- Uses 30+ features including price, volume, technical indicators
- Trains 3 different models and combines predictions
- Provides confidence scores based on model agreement
- Supports 1-30 day prediction horizons

#### Sentiment Analysis (Free Options)
- **Reddit Integration**: Scrapes r/IndiaInvestments (no API key needed)
- **TextBlob**: Free sentiment analysis library
- **VADER**: Social media optimized sentiment analysis
- **Market Indicators**: Volatility regime, momentum signals

#### Advanced Technical Analysis
- **Pattern Recognition**: Automated detection of chart patterns
- **Support/Resistance**: Dynamic level calculation
- **Volume Analysis**: OBV trends, breakout detection
- **Multi-timeframe**: 90-day and 180-day analysis

#### Risk Analytics
- **Comprehensive Metrics**: 8 different risk measures
- **Benchmark Comparison**: Against Nifty 50 index
- **Volatility Analysis**: Regime detection and percentiles
- **Drawdown Analysis**: Maximum loss periods

## 🔧 Configuration Options

### Model Parameters (in ml_predictions.py)
```python
# Adjust these for different prediction characteristics
prediction_days = 5  # 1-30 days
train_size = 0.8     # 80% for training
lookback_days = 20   # Feature calculation window
```

### Risk Analysis Settings (in advanced_analytics.py)
```python
contamination = 0.1  # Anomaly detection sensitivity
n_clusters = 5       # Number of stock clusters
window = 20          # Support/resistance detection window
```

### Sentiment Analysis (in enhanced_sentiment.py)
```python
days_back = 7        # News lookback period
confidence_threshold = 0.1  # Sentiment classification threshold
```

## 🆓 Free vs Paid Features

### Completely Free Features
- ✅ Machine Learning Predictions (scikit-learn)
- ✅ Advanced Technical Analysis (TA-Lib, custom indicators)
- ✅ Risk Analytics (statistical calculations)
- ✅ Stock Clustering (K-means)
- ✅ Anomaly Detection (Isolation Forest)
- ✅ Reddit Sentiment (no API key needed)
- ✅ TextBlob/VADER Sentiment Analysis
- ✅ Pattern Recognition (custom algorithms)

### Enhanced with Free API Keys
- 🔑 NewsAPI Sentiment (100 requests/day free)
- 🔑 HuggingFace Models (rate limited but free)

### Potential Paid Upgrades (not implemented)
- 💰 Real-time data feeds
- 💰 Premium news sources
- 💰 Options flow data
- 💰 Institutional sentiment data

## 🚨 Troubleshooting

### Common Issues

1. **Import Errors**
```bash
# Install missing packages
pip install scikit-learn textblob vaderSentiment
```

2. **VADER Installation**
```bash
# If VADER fails to install
pip install vaderSentiment
# Or use conda
conda install -c conda-forge vadersentiment
```

3. **Memory Issues with Large Datasets**
- Reduce the number of stocks analyzed simultaneously
- Decrease the historical data period in yfinance calls
- Use smaller prediction horizons

4. **API Rate Limits**
- Reddit: Built-in delays, should work fine
- NewsAPI: 100 requests/day limit on free tier
- Yahoo Finance: Built-in rate limiting

### Performance Optimization

1. **Caching**: Uses Streamlit's `@st.cache_resource` for model instances
2. **Batch Processing**: Processes multiple stocks efficiently
3. **Error Handling**: Graceful degradation when APIs fail
4. **Memory Management**: Cleans up large DataFrames

## 📊 Sample Analysis Output

### ML Prediction Example
```
Current Price: ₹2,450.00
Predicted Price (5d): ₹2,523.50 (+3.00%)
Model Confidence: 78.5%

Individual Models:
- Random Forest: ₹2,515.20 (+2.66%)
- Gradient Boost: ₹2,531.80 (+3.34%)
- Linear: ₹2,523.50 (+3.00%)
```

### Risk Analysis Example
```
Annual Return: 15.2%
Annual Volatility: 28.5%
Sharpe Ratio: 0.53
Beta: 1.15
Max Drawdown: -18.7%
VaR (95%): -3.2%
```

### Sentiment Analysis Example
```
Overall Sentiment: Positive
Sentiment Score: 0.245
News Count: 12
Distribution: 60% Positive, 25% Neutral, 15% Negative
```

## 🔮 Future Enhancements

### Planned Free Features
- Options flow analysis using free data
- Sector rotation indicators
- Earnings calendar integration
- Social media sentiment (Twitter API v2 free tier)
- Economic calendar correlation

### Advanced Features (Potential)
- Real-time WebSocket data feeds
- Deep learning models (LSTM, Transformer)
- Alternative data integration
- Portfolio optimization
- Backtesting framework

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the code comments in each module
3. Test with a small number of stocks first
4. Ensure all dependencies are properly installed

The enhanced version maintains backward compatibility with the original app while adding powerful new analytics capabilities using only free and open-source tools.