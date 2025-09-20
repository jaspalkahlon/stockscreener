# advanced_analytics.py
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import yfinance as yf
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class StockAnalytics:
    def __init__(self):
        self.scaler = StandardScaler()
        
    def get_enhanced_features(self, symbol, period="1y"):
        """Extract comprehensive features for a stock"""
        try:
            ticker = yf.Ticker(symbol + ".NS")
            df = ticker.history(period=period)
            
            if df.empty:
                return None
                
            # Price-based features
            df['returns'] = df['Close'].pct_change()
            df['log_returns'] = np.log(df['Close'] / df['Close'].shift(1))
            df['volatility_5d'] = df['returns'].rolling(5).std()
            df['volatility_20d'] = df['returns'].rolling(20).std()
            
            # Momentum features
            df['momentum_5d'] = df['Close'] / df['Close'].shift(5) - 1
            df['momentum_20d'] = df['Close'] / df['Close'].shift(20) - 1
            df['rsi'] = self.calculate_rsi(df['Close'])
            
            # Volume features
            df['volume_sma'] = df['Volume'].rolling(20).mean()
            df['volume_ratio'] = df['Volume'] / df['volume_sma']
            
            # Price position features
            df['price_position'] = (df['Close'] - df['Low'].rolling(20).min()) / (df['High'].rolling(20).max() - df['Low'].rolling(20).min())
            
            # Trend features
            df['sma_20'] = df['Close'].rolling(20).mean()
            df['sma_50'] = df['Close'].rolling(50).mean()
            df['price_vs_sma20'] = df['Close'] / df['sma_20'] - 1
            df['price_vs_sma50'] = df['Close'] / df['sma_50'] - 1
            
            return df.dropna()
            
        except Exception as e:
            print(f"Error processing {symbol}: {e}")
            return None
    
    def calculate_rsi(self, prices, window=14):
        """Calculate RSI indicator"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))
    
    def detect_anomalies(self, symbols, contamination=0.1):
        """Detect unusual stock behavior using Isolation Forest"""
        features_list = []
        valid_symbols = []
        
        for symbol in symbols:
            df = self.get_enhanced_features(symbol)
            if df is not None and len(df) > 50:
                # Get latest features
                latest_features = [
                    df['volatility_20d'].iloc[-1],
                    df['momentum_20d'].iloc[-1],
                    df['volume_ratio'].iloc[-1],
                    df['price_position'].iloc[-1],
                    df['rsi'].iloc[-1],
                    df['price_vs_sma20'].iloc[-1]
                ]
                
                if not any(pd.isna(latest_features)):
                    features_list.append(latest_features)
                    valid_symbols.append(symbol)
        
        if len(features_list) < 2:
            return {}
            
        # Fit Isolation Forest
        features_array = np.array(features_list)
        iso_forest = IsolationForest(contamination=contamination, random_state=42)
        anomaly_scores = iso_forest.fit_predict(features_array)
        
        results = {}
        for i, symbol in enumerate(valid_symbols):
            results[symbol] = {
                'is_anomaly': anomaly_scores[i] == -1,
                'anomaly_score': iso_forest.score_samples([features_array[i]])[0]
            }
        
        return results
    
    def cluster_stocks(self, symbols, n_clusters=5):
        """Cluster stocks based on their characteristics"""
        features_list = []
        valid_symbols = []
        
        for symbol in symbols:
            df = self.get_enhanced_features(symbol)
            if df is not None and len(df) > 50:
                # Calculate aggregate features
                features = [
                    df['returns'].mean(),  # Average return
                    df['volatility_20d'].mean(),  # Average volatility
                    df['momentum_20d'].mean(),  # Average momentum
                    df['volume_ratio'].mean(),  # Average volume ratio
                    df['rsi'].mean(),  # Average RSI
                    df['price_vs_sma20'].mean()  # Average price vs SMA
                ]
                
                if not any(pd.isna(features)):
                    features_list.append(features)
                    valid_symbols.append(symbol)
        
        if len(features_list) < n_clusters:
            return {}
            
        # Standardize features and cluster
        features_scaled = self.scaler.fit_transform(features_list)
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        clusters = kmeans.fit_predict(features_scaled)
        
        # Group stocks by cluster
        cluster_results = {}
        for i, symbol in enumerate(valid_symbols):
            cluster_id = clusters[i]
            if cluster_id not in cluster_results:
                cluster_results[cluster_id] = []
            cluster_results[cluster_id].append(symbol)
        
        return cluster_results
    
    def calculate_risk_metrics(self, symbol, benchmark_symbol="^NSEI"):
        """Calculate comprehensive risk metrics"""
        try:
            # Get stock and benchmark data
            stock_data = self.get_enhanced_features(symbol)
            benchmark_data = yf.download(benchmark_symbol, period="1y")['Close']
            
            if stock_data is None or benchmark_data.empty:
                return None
            
            # Align dates
            common_dates = stock_data.index.intersection(benchmark_data.index)
            stock_returns = stock_data.loc[common_dates, 'returns']
            benchmark_returns = benchmark_data.loc[common_dates].pct_change()
            
            # Calculate metrics
            metrics = {}
            
            # Basic metrics
            metrics['annual_return'] = stock_returns.mean() * 252
            metrics['annual_volatility'] = stock_returns.std() * np.sqrt(252)
            metrics['sharpe_ratio'] = metrics['annual_return'] / metrics['annual_volatility'] if metrics['annual_volatility'] > 0 else 0
            
            # Downside metrics
            negative_returns = stock_returns[stock_returns < 0]
            metrics['downside_deviation'] = negative_returns.std() * np.sqrt(252) if len(negative_returns) > 0 else 0
            metrics['sortino_ratio'] = metrics['annual_return'] / metrics['downside_deviation'] if metrics['downside_deviation'] > 0 else 0
            
            # Maximum drawdown
            cumulative = (1 + stock_returns).cumprod()
            rolling_max = cumulative.expanding().max()
            drawdown = (cumulative - rolling_max) / rolling_max
            metrics['max_drawdown'] = drawdown.min()
            
            # Beta calculation
            covariance = np.cov(stock_returns.dropna(), benchmark_returns.dropna())[0][1]
            benchmark_variance = np.var(benchmark_returns.dropna())
            metrics['beta'] = covariance / benchmark_variance if benchmark_variance > 0 else 0
            
            # Value at Risk (95% confidence)
            metrics['var_95'] = np.percentile(stock_returns.dropna(), 5)
            
            return metrics
            
        except Exception as e:
            print(f"Error calculating risk metrics for {symbol}: {e}")
            return None