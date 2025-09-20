# enhanced_technical.py
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

# Handle optional dependencies gracefully
try:
    from scipy import stats
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False
    print("Warning: scipy not available. Some advanced features will be disabled.")

try:
    from sklearn.linear_model import LinearRegression
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    print("Warning: sklearn not available. Some ML features will be disabled.")

class EnhancedTechnicalAnalysis:
    def __init__(self):
        self.support_resistance_levels = {}
    
    def get_comprehensive_analysis(self, symbol, period="6mo"):
        """Get comprehensive technical analysis"""
        try:
            ticker = yf.Ticker(symbol + ".NS")
            df = ticker.history(period=period)
            
            if df.empty:
                return None
            
            analysis = {}
            
            # Basic indicators
            analysis['basic_indicators'] = self.calculate_basic_indicators(df)
            
            # Advanced indicators
            analysis['advanced_indicators'] = self.calculate_advanced_indicators(df)
            
            # Support and resistance
            analysis['support_resistance'] = self.find_support_resistance(df)
            
            # Trend analysis
            analysis['trend_analysis'] = self.analyze_trend(df)
            
            # Pattern recognition
            analysis['patterns'] = self.detect_patterns(df)
            
            # Volume analysis
            analysis['volume_analysis'] = self.analyze_volume(df)
            
            # Volatility analysis
            analysis['volatility_analysis'] = self.analyze_volatility(df)
            
            return analysis
            
        except Exception as e:
            print(f"Error in comprehensive analysis for {symbol}: {e}")
            return None
    
    def calculate_basic_indicators(self, df):
        """Calculate basic technical indicators with error handling"""
        try:
            indicators = {}
            
            # Moving averages
            for period in [5, 10, 20, 50, 200]:
                if len(df) >= period:
                    df[f'SMA_{period}'] = df['Close'].rolling(period).mean()
                    df[f'EMA_{period}'] = df['Close'].ewm(span=period).mean()
            
            # RSI
            delta = df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
            
            # Avoid division by zero
            rs = gain / loss.replace(0, 0.0001)
            df['RSI'] = 100 - (100 / (1 + rs))
            
            # MACD
            ema_12 = df['Close'].ewm(span=12).mean()
            ema_26 = df['Close'].ewm(span=26).mean()
            df['MACD'] = ema_12 - ema_26
            df['MACD_Signal'] = df['MACD'].ewm(span=9).mean()
            df['MACD_Histogram'] = df['MACD'] - df['MACD_Signal']
            
            # Bollinger Bands
            df['BB_Middle'] = df['Close'].rolling(20).mean()
            bb_std = df['Close'].rolling(20).std()
            df['BB_Upper'] = df['BB_Middle'] + (bb_std * 2)
            df['BB_Lower'] = df['BB_Middle'] - (bb_std * 2)
            
            # Avoid division by zero for BB calculations
            bb_range = df['BB_Upper'] - df['BB_Lower']
            df['BB_Width'] = bb_range / df['BB_Middle'].replace(0, 1)
            df['BB_Position'] = (df['Close'] - df['BB_Lower']) / bb_range.replace(0, 1)
            
            # Current values with safe access
            latest = df.iloc[-1]
            
            def safe_get(key, default=0):
                try:
                    value = latest[key]
                    return value if pd.notna(value) else default
                except (KeyError, IndexError):
                    return default
            
            indicators = {
                'RSI': safe_get('RSI', 50),
                'MACD': safe_get('MACD', 0),
                'MACD_Signal': safe_get('MACD_Signal', 0),
                'BB_Position': safe_get('BB_Position', 0.5),
                'BB_Width': safe_get('BB_Width', 0.1),
                'Price_vs_SMA20': safe_get('Close', 0) / safe_get('SMA_20', safe_get('Close', 1)) - 1 if safe_get('SMA_20', 0) > 0 else 0,
                'Price_vs_SMA50': safe_get('Close', 0) / safe_get('SMA_50', safe_get('Close', 1)) - 1 if safe_get('SMA_50', 0) > 0 else 0,
            }
            
            return indicators
            
        except Exception as e:
            print(f"Error calculating basic indicators: {e}")
            # Return default values
            return {
                'RSI': 50,
                'MACD': 0,
                'MACD_Signal': 0,
                'BB_Position': 0.5,
                'BB_Width': 0.1,
                'Price_vs_SMA20': 0,
                'Price_vs_SMA50': 0,
            }
    
    def calculate_advanced_indicators(self, df):
        """Calculate advanced technical indicators"""
        indicators = {}
        
        # Stochastic Oscillator
        low_14 = df['Low'].rolling(14).min()
        high_14 = df['High'].rolling(14).max()
        df['Stoch_K'] = 100 * ((df['Close'] - low_14) / (high_14 - low_14))
        df['Stoch_D'] = df['Stoch_K'].rolling(3).mean()
        
        # Williams %R
        df['Williams_R'] = -100 * ((high_14 - df['Close']) / (high_14 - low_14))
        
        # Commodity Channel Index (CCI)
        tp = (df['High'] + df['Low'] + df['Close']) / 3
        sma_tp = tp.rolling(20).mean()
        mad = tp.rolling(20).apply(lambda x: np.mean(np.abs(x - x.mean())))
        df['CCI'] = (tp - sma_tp) / (0.015 * mad)
        
        # Average True Range (ATR)
        high_low = df['High'] - df['Low']
        high_close = np.abs(df['High'] - df['Close'].shift())
        low_close = np.abs(df['Low'] - df['Close'].shift())
        true_range = np.maximum(high_low, np.maximum(high_close, low_close))
        df['ATR'] = true_range.rolling(14).mean()
        
        # Parabolic SAR (simplified)
        df['PSAR'] = self.calculate_parabolic_sar(df)
        
        # Money Flow Index
        df['MFI'] = self.calculate_mfi(df)
        
        latest = df.iloc[-1]
        indicators = {
            'Stochastic_K': latest['Stoch_K'],
            'Stochastic_D': latest['Stoch_D'],
            'Williams_R': latest['Williams_R'],
            'CCI': latest['CCI'],
            'ATR': latest['ATR'],
            'PSAR': latest['PSAR'],
            'MFI': latest['MFI']
        }
        
        return indicators
    
    def calculate_parabolic_sar(self, df, af_start=0.02, af_increment=0.02, af_max=0.2):
        """Calculate Parabolic SAR"""
        psar = df['Close'].copy()
        trend = [1]  # 1 for uptrend, -1 for downtrend
        af = af_start
        ep = df['High'].iloc[0]  # Extreme point
        
        for i in range(1, len(df)):
            if trend[-1] == 1:  # Uptrend
                psar.iloc[i] = psar.iloc[i-1] + af * (ep - psar.iloc[i-1])
                
                if df['High'].iloc[i] > ep:
                    ep = df['High'].iloc[i]
                    af = min(af + af_increment, af_max)
                
                if df['Low'].iloc[i] < psar.iloc[i]:
                    trend.append(-1)
                    psar.iloc[i] = ep
                    af = af_start
                    ep = df['Low'].iloc[i]
                else:
                    trend.append(1)
            else:  # Downtrend
                psar.iloc[i] = psar.iloc[i-1] + af * (ep - psar.iloc[i-1])
                
                if df['Low'].iloc[i] < ep:
                    ep = df['Low'].iloc[i]
                    af = min(af + af_increment, af_max)
                
                if df['High'].iloc[i] > psar.iloc[i]:
                    trend.append(1)
                    psar.iloc[i] = ep
                    af = af_start
                    ep = df['High'].iloc[i]
                else:
                    trend.append(-1)
        
        return psar
    
    def calculate_mfi(self, df, period=14):
        """Calculate Money Flow Index"""
        typical_price = (df['High'] + df['Low'] + df['Close']) / 3
        money_flow = typical_price * df['Volume']
        
        positive_flow = []
        negative_flow = []
        
        for i in range(1, len(typical_price)):
            if typical_price.iloc[i] > typical_price.iloc[i-1]:
                positive_flow.append(money_flow.iloc[i])
                negative_flow.append(0)
            elif typical_price.iloc[i] < typical_price.iloc[i-1]:
                positive_flow.append(0)
                negative_flow.append(money_flow.iloc[i])
            else:
                positive_flow.append(0)
                negative_flow.append(0)
        
        positive_flow = pd.Series([0] + positive_flow, index=df.index)
        negative_flow = pd.Series([0] + negative_flow, index=df.index)
        
        positive_mf = positive_flow.rolling(period).sum()
        negative_mf = negative_flow.rolling(period).sum()
        
        mfi = 100 - (100 / (1 + (positive_mf / negative_mf)))
        return mfi
    
    def find_support_resistance(self, df, window=20):
        """Find support and resistance levels"""
        highs = df['High'].rolling(window, center=True).max()
        lows = df['Low'].rolling(window, center=True).min()
        
        # Find peaks and troughs
        resistance_levels = []
        support_levels = []
        
        for i in range(window, len(df) - window):
            if df['High'].iloc[i] == highs.iloc[i]:
                resistance_levels.append(df['High'].iloc[i])
            if df['Low'].iloc[i] == lows.iloc[i]:
                support_levels.append(df['Low'].iloc[i])
        
        # Get most significant levels (by frequency)
        current_price = df['Close'].iloc[-1]
        
        # Filter and sort levels
        resistance_levels = [r for r in resistance_levels if r > current_price]
        support_levels = [s for s in support_levels if s < current_price]
        
        return {
            'resistance_levels': sorted(set(resistance_levels))[-3:],  # Top 3 resistance
            'support_levels': sorted(set(support_levels), reverse=True)[:3],  # Top 3 support
            'current_price': current_price
        }
    
    def analyze_trend(self, df):
        """Analyze price trend using multiple methods"""
        try:
            # Moving average trend
            sma_20 = df['Close'].rolling(20).mean()
            sma_50 = df['Close'].rolling(50).mean()
            
            # Simple trend calculation
            recent_prices = df['Close'].tail(20)
            price_change = (recent_prices.iloc[-1] - recent_prices.iloc[0]) / recent_prices.iloc[0]
            trend_direction = 'up' if price_change > 0 else 'down'
            trend_strength = abs(price_change)
            
            # Linear regression trend (if scipy available)
            if SCIPY_AVAILABLE:
                x = np.arange(len(df))
                y = df['Close'].values
                slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
                trend_strength = abs(r_value)
                trend_direction = 'up' if slope > 0 else 'down'
                r_squared = r_value ** 2
            else:
                slope = price_change
                r_squared = 0.5  # Default value
            
            # ADX for trend strength
            try:
                adx = self.calculate_adx(df)
                adx_value = adx.iloc[-1] if not adx.empty else 25
            except:
                adx_value = 25  # Default ADX value
            
            return {
                'direction': trend_direction,
                'strength': min(trend_strength, 1.0),  # Cap at 1.0
                'slope': slope,
                'r_squared': r_squared,
                'adx': adx_value,
                'ma_trend': 'bullish' if sma_20.iloc[-1] > sma_50.iloc[-1] else 'bearish'
            }
        except Exception as e:
            print(f"Error in trend analysis: {e}")
            return {
                'direction': 'neutral',
                'strength': 0.5,
                'slope': 0,
                'r_squared': 0.5,
                'adx': 25,
                'ma_trend': 'neutral'
            }
    
    def calculate_adx(self, df, period=14):
        """Calculate Average Directional Index"""
        high_diff = df['High'].diff()
        low_diff = df['Low'].diff()
        
        plus_dm = np.where((high_diff > low_diff) & (high_diff > 0), high_diff, 0)
        minus_dm = np.where((low_diff > high_diff) & (low_diff > 0), low_diff, 0)
        
        tr1 = df['High'] - df['Low']
        tr2 = abs(df['High'] - df['Close'].shift())
        tr3 = abs(df['Low'] - df['Close'].shift())
        tr = np.maximum(tr1, np.maximum(tr2, tr3))
        
        atr = pd.Series(tr).rolling(period).mean()
        plus_di = 100 * (pd.Series(plus_dm).rolling(period).mean() / atr)
        minus_di = 100 * (pd.Series(minus_dm).rolling(period).mean() / atr)
        
        dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di)
        adx = dx.rolling(period).mean()
        
        return adx
    
    def detect_patterns(self, df):
        """Detect common chart patterns"""
        patterns = {}
        
        # Double top/bottom detection
        patterns['double_top'] = self.detect_double_top(df)
        patterns['double_bottom'] = self.detect_double_bottom(df)
        
        # Head and shoulders
        patterns['head_shoulders'] = self.detect_head_shoulders(df)
        
        # Triangle patterns
        patterns['triangle'] = self.detect_triangle(df)
        
        # Flag/pennant
        patterns['flag'] = self.detect_flag(df)
        
        return patterns
    
    def detect_double_top(self, df, window=20):
        """Detect double top pattern"""
        highs = df['High'].rolling(window, center=True).max()
        peaks = []
        
        for i in range(window, len(df) - window):
            if df['High'].iloc[i] == highs.iloc[i]:
                peaks.append((i, df['High'].iloc[i]))
        
        if len(peaks) >= 2:
            # Check if last two peaks are similar in height
            last_two = peaks[-2:]
            height_diff = abs(last_two[0][1] - last_two[1][1]) / last_two[0][1]
            
            if height_diff < 0.02:  # Within 2%
                return {'detected': True, 'confidence': 1 - height_diff}
        
        return {'detected': False, 'confidence': 0}
    
    def detect_double_bottom(self, df, window=20):
        """Detect double bottom pattern"""
        lows = df['Low'].rolling(window, center=True).min()
        troughs = []
        
        for i in range(window, len(df) - window):
            if df['Low'].iloc[i] == lows.iloc[i]:
                troughs.append((i, df['Low'].iloc[i]))
        
        if len(troughs) >= 2:
            last_two = troughs[-2:]
            height_diff = abs(last_two[0][1] - last_two[1][1]) / last_two[0][1]
            
            if height_diff < 0.02:
                return {'detected': True, 'confidence': 1 - height_diff}
        
        return {'detected': False, 'confidence': 0}
    
    def detect_head_shoulders(self, df):
        """Detect head and shoulders pattern"""
        # Simplified detection - look for three peaks with middle one highest
        return {'detected': False, 'confidence': 0}  # Placeholder
    
    def detect_triangle(self, df):
        """Detect triangle patterns"""
        try:
            # Simplified - check if highs are declining and lows are rising
            recent_highs = df['High'].tail(20)
            recent_lows = df['Low'].tail(20)
            
            if SCIPY_AVAILABLE:
                high_slope = stats.linregress(range(len(recent_highs)), recent_highs)[0]
                low_slope = stats.linregress(range(len(recent_lows)), recent_lows)[0]
            else:
                # Simple slope calculation
                high_slope = (recent_highs.iloc[-1] - recent_highs.iloc[0]) / len(recent_highs)
                low_slope = (recent_lows.iloc[-1] - recent_lows.iloc[0]) / len(recent_lows)
            
            if high_slope < 0 and low_slope > 0:
                return {'detected': True, 'type': 'symmetrical', 'confidence': 0.7}
            
            return {'detected': False, 'confidence': 0}
        except Exception as e:
            print(f"Error detecting triangle: {e}")
            return {'detected': False, 'confidence': 0}
    
    def detect_flag(self, df):
        """Detect flag/pennant patterns"""
        # Simplified - look for consolidation after strong move
        recent_returns = df['Close'].pct_change().tail(20)
        volatility = recent_returns.std()
        
        if volatility < 0.02:  # Low volatility consolidation
            return {'detected': True, 'confidence': 0.6}
        
        return {'detected': False, 'confidence': 0}
    
    def analyze_volume(self, df):
        """Analyze volume patterns"""
        volume_sma = df['Volume'].rolling(20).mean()
        current_volume = df['Volume'].iloc[-1]
        avg_volume = volume_sma.iloc[-1]
        
        # Volume trend
        volume_trend = df['Volume'].rolling(10).mean().diff().iloc[-1]
        
        # On Balance Volume
        obv = (df['Volume'] * np.where(df['Close'].diff() > 0, 1, -1)).cumsum()
        
        return {
            'current_vs_average': current_volume / avg_volume,
            'volume_trend': 'increasing' if volume_trend > 0 else 'decreasing',
            'obv_trend': 'bullish' if obv.diff().tail(5).mean() > 0 else 'bearish',
            'volume_breakout': current_volume > avg_volume * 1.5
        }
    
    def analyze_volatility(self, df):
        """Analyze volatility patterns"""
        returns = df['Close'].pct_change()
        
        # Historical volatility
        vol_20 = returns.rolling(20).std() * np.sqrt(252)
        vol_50 = returns.rolling(50).std() * np.sqrt(252)
        
        # Volatility percentile
        current_vol = vol_20.iloc[-1]
        vol_percentile = (vol_20 < current_vol).sum() / len(vol_20.dropna())
        
        return {
            'current_volatility': current_vol,
            'volatility_percentile': vol_percentile,
            'volatility_regime': 'high' if vol_percentile > 0.8 else 'low' if vol_percentile < 0.2 else 'normal',
            'vol_20_vs_50': vol_20.iloc[-1] / vol_50.iloc[-1] - 1
        }