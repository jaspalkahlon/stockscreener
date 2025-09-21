# Technology Stack & Build System

## Core Technologies

### Frontend & Framework
- **Streamlit**: Web application framework for data science apps
- **Plotly**: Interactive charting and visualization library
- **Pandas**: Data manipulation and analysis

### Data Sources & APIs
- **Yahoo Finance (yfinance)**: Primary market data source
- **NewsAPI**: News sentiment analysis (optional, 100 requests/day free)
- **Reddit API**: Alternative news source for sentiment
- **HuggingFace**: ML model API (optional, rate limited)

### Machine Learning & Analytics
- **scikit-learn**: ML models (Random Forest, Gradient Boosting, Linear Regression)
- **NumPy/SciPy**: Numerical computing and statistical analysis
- **TextBlob/VADER**: Natural language processing for sentiment analysis
- **TA-Lib**: Technical analysis indicators (optional dependency)

### Environment & Configuration
- **python-dotenv**: Environment variable management
- **openpyxl**: Excel file handling for data export

## Common Commands

### Installation & Setup
```bash
# Install all dependencies
pip install -r requirements.txt

# Alternative installation script
./install_dependencies.sh

# Download NLTK data for TextBlob
python -c "import nltk; nltk.download('punkt'); nltk.download('brown')"
```

### Running Applications
```bash
# Main enhanced application
streamlit run enhanced_app.py

# Original basic application
streamlit run app.py

# Simple versions
streamlit run simple_app.py
streamlit run clean_app.py
```

### Testing & Validation
```bash
# Test enhanced features
python test_enhanced_features.py

# Test all applications
python test_apps.py

# Test environment setup
python test_env.py
```

### Service Management
```bash
# Use management script for production
./manage_stockscreener.sh start
./manage_stockscreener.sh status
./manage_stockscreener.sh logs
```

## Development Patterns

### Module Architecture
- Modular design with separate files for each analysis type
- Class-based analytics modules with caching decorators
- Session state management for multi-step workflows

### Error Handling
- Graceful degradation when API keys are missing
- Try-catch blocks for external API calls
- Fallback options for optional dependencies

### Performance Optimization
- `@st.cache_resource` for expensive operations
- Lazy loading of analytics instances
- Efficient data processing with pandas/numpy