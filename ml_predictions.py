# ml_predictions.py
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error, mean_absolute_error
import yfinance as yf
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class MLPredictor:
    def __init__(self):
        self.models = {
            'random_forest': RandomForestRegressor(n_estimators=100, random_state=42),
            'gradient_boost': GradientBoostingRegressor(n_estimators=100, random_state=42),
            'linear': LinearRegression()
        }
        self.scaler = StandardScaler()
        self.feature_names = []
    
    def create_features(self, df, lookback_days=20):
        """Create comprehensive features for ML model"""
        features_df = df.copy()
        
        # Price-based features
        features_df['returns'] = df['Close'].pct_change()
        features_df['log_returns'] = np.log(df['Close'] / df['Close'].shift(1))
        
        # Moving averages
        for window in [5, 10, 20, 50]:
            features_df[f'sma_{window}'] = df['Close'].rolling(window).mean()
            features_df[f'price_vs_sma_{window}'] = df['Close'] / features_df[f'sma_{window}'] - 1
        
        # Volatility features
        features_df['volatility_5'] = features_df['returns'].rolling(5).std()
        features_df['volatility_20'] = features_df['returns'].rolling(20).std()
        
        # Momentum features
        for period in [5, 10, 20]:
            features_df[f'momentum_{period}'] = df['Close'] / df['Close'].shift(period) - 1
        
        # Volume features
        features_df['volume_sma'] = df['Volume'].rolling(20).mean()
        features_df['volume_ratio'] = df['Volume'] / features_df['volume_sma']
        
        # Technical indicators
        features_df['rsi'] = self.calculate_rsi(df['Close'])
        features_df['macd'], features_df['macd_signal'] = self.calculate_macd(df['Close'])
        features_df['bb_position'] = self.calculate_bollinger_position(df['Close'])
        
        # Price position features
        features_df['high_low_ratio'] = df['High'] / df['Low'] - 1
        features_df['close_position'] = (df['Close'] - df['Low']) / (df['High'] - df['Low'])
        
        # Lag features (previous day values)
        for lag in [1, 2, 3, 5]:
            features_df[f'close_lag_{lag}'] = df['Close'].shift(lag)
            features_df[f'volume_lag_{lag}'] = df['Volume'].shift(lag)
            features_df[f'returns_lag_{lag}'] = features_df['returns'].shift(lag)
        
        return features_df
    
    def calculate_rsi(self, prices, window=14):
        """Calculate RSI"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))
    
    def calculate_macd(self, prices, fast=12, slow=26, signal=9):
        """Calculate MACD"""
        ema_fast = prices.ewm(span=fast).mean()
        ema_slow = prices.ewm(span=slow).mean()
        macd = ema_fast - ema_slow
        macd_signal = macd.ewm(span=signal).mean()
        return macd, macd_signal
    
    def calculate_bollinger_position(self, prices, window=20, num_std=2):
        """Calculate position within Bollinger Bands"""
        sma = prices.rolling(window).mean()
        std = prices.rolling(window).std()
        upper_band = sma + (std * num_std)
        lower_band = sma - (std * num_std)
        return (prices - lower_band) / (upper_band - lower_band)
    
    def prepare_data(self, symbol, prediction_days=5, train_size=0.8):
        """Prepare data for training"""
        try:
            # Get historical data
            ticker = yf.Ticker(symbol + ".NS")
            df = ticker.history(period="2y")  # Get 2 years of data
            
            if df.empty or len(df) < 100:
                return None, None, None, None
            
            # Create features
            features_df = self.create_features(df)
            
            # Create target (future returns)
            features_df['target'] = features_df['Close'].shift(-prediction_days) / features_df['Close'] - 1
            
            # Remove rows with NaN values
            features_df = features_df.dropna()
            
            if len(features_df) < 50:
                return None, None, None, None
            
            # Select feature columns (exclude target and original OHLCV)
            feature_cols = [col for col in features_df.columns 
                          if col not in ['Open', 'High', 'Low', 'Close', 'Volume', 'target']]
            
            X = features_df[feature_cols]
            y = features_df['target']
            
            # Store feature names
            self.feature_names = feature_cols
            
            # Split data
            split_idx = int(len(X) * train_size)
            X_train, X_test = X[:split_idx], X[split_idx:]
            y_train, y_test = y[:split_idx], y[split_idx:]
            
            return X_train, X_test, y_train, y_test
            
        except Exception as e:
            print(f"Error preparing data for {symbol}: {e}")
            return None, None, None, None
    
    def train_models(self, symbol, prediction_days=5):
        """Train multiple models and return best performer"""
        X_train, X_test, y_train, y_test = self.prepare_data(symbol, prediction_days)
        
        if X_train is None:
            return None
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        results = {}
        
        for name, model in self.models.items():
            try:
                # Train model
                if name == 'linear':
                    model.fit(X_train_scaled, y_train)
                    y_pred = model.predict(X_test_scaled)
                else:
                    model.fit(X_train, y_train)
                    y_pred = model.predict(X_test)
                
                # Calculate metrics
                mse = mean_squared_error(y_test, y_pred)
                mae = mean_absolute_error(y_test, y_pred)
                
                # Cross-validation score
                if name == 'linear':
                    cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=5, scoring='neg_mean_squared_error')
                else:
                    cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='neg_mean_squared_error')
                
                results[name] = {
                    'model': model,
                    'mse': mse,
                    'mae': mae,
                    'cv_score': -cv_scores.mean(),
                    'predictions': y_pred,
                    'actual': y_test.values
                }
                
                # Feature importance (for tree-based models)
                if hasattr(model, 'feature_importances_'):
                    feature_importance = dict(zip(self.feature_names, model.feature_importances_))
                    results[name]['feature_importance'] = sorted(feature_importance.items(), 
                                                               key=lambda x: x[1], reverse=True)[:10]
                
            except Exception as e:
                print(f"Error training {name} model: {e}")
                continue
        
        return results
    
    def predict_future_price(self, symbol, days_ahead=5):
        """Predict future price movement"""
        try:
            # Get recent data
            ticker = yf.Ticker(symbol + ".NS")
            df = ticker.history(period="6mo")
            
            if df.empty:
                return None
            
            # Create features for the latest data point
            features_df = self.create_features(df)
            features_df = features_df.dropna()
            
            if features_df.empty:
                return None
            
            # Get latest features
            feature_cols = [col for col in features_df.columns 
                          if col not in ['Open', 'High', 'Low', 'Close', 'Volume']]
            
            latest_features = features_df[feature_cols].iloc[-1:].values
            
            # Train models on recent data
            model_results = self.train_models(symbol, days_ahead)
            
            if not model_results:
                return None
            
            # Get predictions from all models
            predictions = {}
            current_price = df['Close'].iloc[-1]
            
            for name, result in model_results.items():
                model = result['model']
                
                if name == 'linear':
                    # Scale features for linear model
                    latest_scaled = self.scaler.transform(latest_features)
                    pred_return = model.predict(latest_scaled)[0]
                else:
                    pred_return = model.predict(latest_features)[0]
                
                predicted_price = current_price * (1 + pred_return)
                
                predictions[name] = {
                    'predicted_return': pred_return,
                    'predicted_price': predicted_price,
                    'confidence': 1 / (1 + result['mse']),  # Simple confidence metric
                    'model_accuracy': result
                }
            
            # Ensemble prediction (weighted average based on performance)
            weights = {name: 1 / (1 + result['mse']) for name, result in model_results.items()}
            total_weight = sum(weights.values())
            
            ensemble_return = sum(pred['predicted_return'] * weights[name] / total_weight 
                                for name, pred in predictions.items())
            ensemble_price = current_price * (1 + ensemble_return)
            
            return {
                'current_price': current_price,
                'ensemble_prediction': {
                    'predicted_price': ensemble_price,
                    'predicted_return': ensemble_return,
                    'prediction_days': days_ahead
                },
                'individual_models': predictions,
                'model_performance': {name: {'mse': result['mse'], 'mae': result['mae']} 
                                    for name, result in model_results.items()}
            }
            
        except Exception as e:
            print(f"Error predicting future price for {symbol}: {e}")
            return None
    
    def get_prediction_confidence(self, symbol):
        """Calculate prediction confidence based on model agreement"""
        try:
            results = self.train_models(symbol)
            if not results:
                return 0
            
            # Calculate agreement between models
            predictions = [result['predictions'] for result in results.values()]
            
            if len(predictions) < 2:
                return 0.5
            
            # Calculate correlation between predictions
            correlations = []
            for i in range(len(predictions)):
                for j in range(i+1, len(predictions)):
                    corr = np.corrcoef(predictions[i], predictions[j])[0, 1]
                    if not np.isnan(corr):
                        correlations.append(abs(corr))
            
            return np.mean(correlations) if correlations else 0.5
            
        except Exception as e:
            print(f"Error calculating confidence for {symbol}: {e}")
            return 0