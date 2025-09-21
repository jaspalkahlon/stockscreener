# Project Structure & Organization

## Application Hierarchy

### Main Applications (Entry Points)
- **enhanced_app.py**: Primary enhanced application with full feature set
- **app.py**: Original basic application with 4-step workflow
- **simple_app.py**: Simplified version for basic analysis
- **clean_app.py**: Minimal clean implementation

### Core Analysis Modules

#### Enhanced Modules (Advanced Features)
- **advanced_analytics.py**: ML analytics, risk metrics, clustering, anomaly detection
- **enhanced_sentiment.py**: Multi-source sentiment analysis (NewsAPI + Reddit)
- **ml_predictions.py**: Machine learning predictions with ensemble models
- **enhanced_technical.py**: Advanced technical indicators and pattern recognition

#### Original Modules (Basic Features)
- **data_input.py**: Stock symbol input and data loading
- **fundamental.py**: Basic fundamental analysis scoring
- **technical.py**: Basic technical analysis indicators
- **sentiment.py**: Simple sentiment analysis

### Configuration & Setup
- **requirements.txt**: Python dependencies
- **.env.example**: Environment variable template
- **.env**: Local environment configuration (not in git)

### Installation & Management Scripts
- **install_dependencies.sh**: Automated dependency installation
- **install_server.sh**: Server setup automation
- **manage_stockscreener.sh**: Service management (start/stop/status)
- **setup_*.sh**: Various setup scripts for different deployment scenarios

### Testing & Validation
- **test_enhanced_features.py**: Comprehensive feature testing
- **test_apps.py**: Application testing suite
- **test_env.py**: Environment validation

### Documentation
- **README.md**: Main project documentation
- **SETUP_ENHANCED.md**: Detailed setup instructions
- **SECURITY_SETUP_GUIDE.md**: Security configuration guide
- **SELF_HOST_GUIDE.md**: Self-hosting instructions

## Code Organization Patterns

### Module Structure
- Each analysis type has its own dedicated module
- Class-based design for complex analytics (StockAnalytics, MLPredictor, etc.)
- Function-based design for simpler modules
- Clear separation between data processing and UI logic

### Session State Management
- Consistent session state keys across applications
- Step-based workflow tracking
- Persistent data storage between navigation steps

### File Naming Conventions
- **enhanced_*.py**: Advanced feature modules
- **simple_*.py**: Simplified implementations
- **test_*.py**: Testing modules
- **setup_*.sh**: Setup and installation scripts
- **install_*.sh**: Installation automation
- **UPPERCASE.md**: Documentation files

### Import Patterns
- External libraries imported first
- Local modules imported after external dependencies
- Conditional imports for optional dependencies
- Environment variables loaded early in application lifecycle