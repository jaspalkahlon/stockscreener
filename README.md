# 🚀 Enhanced Indian Stock Screener

A comprehensive stock analysis platform for Indian equity markets with advanced analytics, machine learning predictions, and multi-source sentiment analysis.

## ✨ Features

### 🤖 Machine Learning Predictions
- **3 ML Models**: Random Forest, Gradient Boosting, Linear Regression
- **30+ Features**: Technical indicators, price patterns, volume analysis
- **Ensemble Predictions**: Combines models for better accuracy
- **Confidence Scoring**: Model agreement-based reliability metrics

### 💭 Advanced Sentiment Analysis
- **Multi-source News**: NewsAPI + Reddit integration
- **Dual Analysis Engines**: TextBlob + VADER sentiment
- **Market Sentiment**: Volatility regime, momentum indicators
- **100% Free Options**: Works without API keys using Reddit + TextBlob

### 📈 Enhanced Technical Analysis with Trading Recommendations
- **15+ Advanced Indicators**: RSI, MACD, Stochastic, Williams %R, CCI, ATR, Parabolic SAR, MFI
- **Pattern Recognition**: Double tops/bottoms, triangles, flags
- **Support/Resistance**: Automated level detection
- **Volume Analysis**: OBV trends, breakout detection
- **90-Day Price Projections**: Interactive slider for 1-90 day analysis periods
- **AI Trading Recommendations**: Buy/Sell/Hold signals with confidence levels
- **Target Price & Stop Loss**: Automated calculation based on technical factors
- **Risk-Reward Analysis**: Complete position sizing and risk management guidance

### 🔬 Advanced Analytics
- **Anomaly Detection**: Isolation Forest for unusual stock behavior
- **Stock Clustering**: K-means grouping by characteristics
- **Risk Metrics**: Sharpe, Sortino, VaR, Beta, Maximum Drawdown
- **Trend Analysis**: Multi-method strength and direction

## 🎯 8-Step Analysis Workflow

1. **📊 Input & Data** - Enter stock symbols or upload CSV
2. **🔍 Fundamental Analysis** - Smart scoring system with 6 criteria
3. **🎯 Stock Selection** - Choose stocks for advanced analysis
4. **📈 Technical Analysis & Recommendations** - Interactive charts with 90-day projections and AI trading signals
5. **🤖 ML Predictions** - AI-powered price forecasting (1-90 days)
6. **💭 Sentiment Analysis** - Multi-source news sentiment
7. **🔬 Advanced Analytics** - Clustering, risk analysis, patterns
8. **📋 Summary Report** - Comprehensive analysis export

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- pip or pip3

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd enhanced-stock-screener
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download NLTK data** (for TextBlob)
   ```bash
   python -c "import nltk; nltk.download('punkt'); nltk.download('brown')"
   ```

4. **Set up API keys** (optional)
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys
   ```

5. **Run the application**
   ```bash
   streamlit run enhanced_app.py
   ```

## 🔑 API Keys (Optional)

### Free Tier Options
- **NewsAPI**: 100 requests/day - [Sign up](https://newsapi.org/)
- **HuggingFace**: Rate limited but free - [Sign up](https://huggingface.co/)

### Environment Variables
Create a `.env` file:
```env
NEWSAPI_KEY=your_newsapi_key_here
HF_API_KEY=your_huggingface_token_here
```

**Note**: The app works fully without API keys using free alternatives!

## 📊 Sample Analysis Output

### ML Prediction
```
Current Price: ₹2,450.00
Predicted Price (5d): ₹2,523.50 (+3.00%)
Model Confidence: 78.5%

Individual Models:
- Random Forest: ₹2,515.20 (+2.66%)
- Gradient Boost: ₹2,531.80 (+3.34%)
- Linear: ₹2,523.50 (+3.00%)
```

### Risk Analysis
```
Annual Return: 15.2%
Annual Volatility: 28.5%
Sharpe Ratio: 0.53
Beta: 1.15
Max Drawdown: -18.7%
VaR (95%): -3.2%
```

### Trading Recommendation
```
Recommendation: 🟢 BUY (High Confidence)
Target Price: ₹2,650.00 (+8.2%)
Stop Loss: ₹2,280.00 (-6.9%)
Risk-Reward Ratio: 1:1.8
Time Horizon: 30 days

Component Scores:
• Technical: 72/100
• ML Prediction: 68/100  
• Momentum: 75/100
• Risk: 65/100
• Volume: 80/100

Overall Score: 71.2/100
```

### Sentiment Analysis
```
Overall Sentiment: Positive
Sentiment Score: 0.245
News Count: 12
Distribution: 60% Positive, 25% Neutral, 15% Negative
```

## 🛠️ Technical Stack

- **Frontend**: Streamlit
- **Data Source**: Yahoo Finance (yfinance)
- **ML/Analytics**: scikit-learn, pandas, numpy
- **Technical Analysis**: TA-Lib, custom indicators
- **Visualization**: Plotly, interactive charts
- **Sentiment**: TextBlob, VADER, NewsAPI, Reddit
- **Risk Analytics**: Statistical calculations

## 📁 Project Structure

```
├── enhanced_app.py              # Main Streamlit application
├── advanced_analytics.py        # ML analytics & risk metrics
├── enhanced_sentiment.py        # Multi-source sentiment analysis
├── ml_predictions.py           # Machine learning predictions
├── enhanced_technical.py       # Advanced technical analysis
├── data_input.py              # Original data input module
├── fundamental.py             # Original fundamental analysis
├── technical.py               # Original technical analysis
├── sentiment.py               # Original sentiment analysis
├── app.py                     # Original application
├── requirements.txt           # Python dependencies
├── test_enhanced_features.py  # Feature testing script
├── SETUP_ENHANCED.md         # Detailed setup guide
└── README.md                 # This file
```

## 🧪 Testing

Run the test suite to verify all features:
```bash
python test_enhanced_features.py
```

## 🆓 Free vs Premium Features

### Completely Free
- ✅ Machine Learning Predictions (1-90 days)
- ✅ Advanced Technical Analysis with Projections
- ✅ AI Trading Recommendations (Buy/Sell/Hold)
- ✅ Target Price & Stop Loss Calculations
- ✅ Risk Analytics & Clustering
- ✅ Reddit Sentiment Analysis
- ✅ TextBlob/VADER Sentiment
- ✅ Pattern Recognition
- ✅ Anomaly Detection

### Enhanced with Free APIs
- 🔑 NewsAPI (100 requests/day)
- 🔑 HuggingFace Models (rate limited)

## 📈 Supported Markets

- **Primary**: Indian Stock Exchanges (NSE/BSE)
- **Format**: Add ".NS" suffix for NSE stocks
- **Examples**: RELIANCE.NS, TCS.NS, INFY.NS

## ⚠️ Disclaimer

This tool is for educational and research purposes only. Not financial advice. Always consult with qualified financial advisors before making investment decisions.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Yahoo Finance for market data
- scikit-learn for ML algorithms
- Streamlit for the web framework
- NewsAPI for news data
- TextBlob & VADER for sentiment analysis

## 📞 Support

For issues or questions:
1. Check the [Setup Guide](SETUP_ENHANCED.md)
2. Run the test suite: `python test_enhanced_features.py`
3. Open an issue on GitHub

---

**Built with ❤️ for the Indian stock market community**