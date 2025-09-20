# simple_technical.py - Simplified technical analysis without advanced dependencies
import pandas as pd
import numpy as np
import yfinance as yf

class SimpleTechnicalAnalysis:
    """Simplified technical analysis that works with basic dependencies only"""
    
    def __init__(self):
        pass
    
    def get_comprehensive_analysis(self, symbol, period="6mo"):
        """Get basic technical analysis that always works"""
        try:
            ticker = yf.Ticker(symbol + ".NS")
            df = ticker.history(period=period)
            
            if df.empty:
                return None
            
            analysis = {}
            
            # Basic indicators (always work)
            analysis['basic_indicators'] = self.calculate_basic_indicators(df)
            
            # Simple support/resistance
            analysis['support_resistance'] = self.find_simple_support_resistance(df)
            
            # Simple trend analysis
            analysis['trend_analysis'] = self.analyze_simple_trend(df)
            
            # Basic patterns
            analysis['patterns'] = self.detect_simple_patterns(df)
            
            return analysis
            
        except Exception as e:
            print(f"Error in technical analysis for {symbol}: {e}")
            return self.get_default_analysis()
    
    def calculate_basic_indicators(self, df):
        """Calculate basic indicators that always work"""
        try:
            # RSI
            delta = df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
            rs = gain / loss.replace(0, 0.0001)
            rsi = 100 - (100 / (1 + rs))
            
            # MACD
            ema_12 = df['Close'].ewm(span=12).mean()
            ema_26 = df['Close'].ewm(span=26).mean()
            macd = ema_12 - ema_26
            macd_signal = macd.ewm(span=9).mean()
            
            # Moving averages
            sma_20 = df['Close'].rolling(20).mean()
            sma_50 = df['Close'].rolling(50).mean()
            
            # Bollinger Bands
            bb_middle = df['Close'].rolling(20).mean()
            bb_std = df['Close'].rolling(20).std()
            bb_upper = bb_middle + (bb_std * 2)
            bb_lower = bb_middle - (bb_std * 2)
            bb_position = (df['Close'] - bb_lower) / (bb_upper - bb_lower)
            
            # Get latest values safely
            latest_rsi = rsi.iloc[-1] if not rsi.empty and pd.notna(rsi.iloc[-1]) else 50
            latest_macd = macd.iloc[-1] if not macd.empty and pd.notna(macd.iloc[-1]) else 0
            latest_bb_pos = bb_position.iloc[-1] if not bb_position.empty and pd.notna(bb_position.iloc[-1]) else 0.5
            
            return {
                'RSI': float(latest_rsi),
                'MACD': float(latest_macd),
                'MACD_Signal': float(macd_signal.iloc[-1]) if not macd_signal.empty else 0,
                'BB_Position': float(latest_bb_pos),
                'SMA_20': float(sma_20.iloc[-1]) if not sma_20.empty else df['Close'].iloc[-1],
                'SMA_50': float(sma_50.iloc[-1]) if not sma_50.empty else df['Close'].iloc[-1],
                'Current_Price': float(df['Close'].iloc[-1])
            }
            
        except Exception as e:
            print(f"Error calculating indicators: {e}")
            return {
                'RSI': 50.0,
                'MACD': 0.0,
                'MACD_Signal': 0.0,
                'BB_Position': 0.5,
                'SMA_20': float(df['Close'].iloc[-1]),
                'SMA_50': float(df['Close'].iloc[-1]),
                'Current_Price': float(df['Close'].iloc[-1])
            }
    
    def find_simple_support_resistance(self, df):
        """Find basic support and resistance levels"""
        try:
            current_price = df['Close'].iloc[-1]
            
            # Simple method: recent highs and lows
            recent_data = df.tail(50)  # Last 50 days
            
            # Find local maxima and minima
            highs = recent_data['High'].rolling(5, center=True).max()
            lows = recent_data['Low'].rolling(5, center=True).min()
            
            resistance_levels = []
            support_levels = []
            
            for i in range(2, len(recent_data) - 2):
                if recent_data['High'].iloc[i] == highs.iloc[i] and recent_data['High'].iloc[i] > current_price:
                    resistance_levels.append(recent_data['High'].iloc[i])
                
                if recent_data['Low'].iloc[i] == lows.iloc[i] and recent_data['Low'].iloc[i] < current_price:
                    support_levels.append(recent_data['Low'].iloc[i])
            
            # Get top 3 levels
            resistance_levels = sorted(set(resistance_levels))[-3:] if resistance_levels else []
            support_levels = sorted(set(support_levels), reverse=True)[:3] if support_levels else []
            
            return {
                'current_price': float(current_price),
                'resistance_levels': [float(r) for r in resistance_levels],
                'support_levels': [float(s) for s in support_levels]
            }
            
        except Exception as e:
            print(f"Error finding support/resistance: {e}")
            current_price = float(df['Close'].iloc[-1])
            return {
                'current_price': current_price,
                'resistance_levels': [current_price * 1.05],
                'support_levels': [current_price * 0.95]
            }
    
    def analyze_simple_trend(self, df):
        """Simple trend analysis"""
        try:
            # Price change over different periods
            current_price = df['Close'].iloc[-1]
            
            # Short term (5 days)
            short_change = (current_price - df['Close'].iloc[-6]) / df['Close'].iloc[-6] if len(df) > 5 else 0
            
            # Medium term (20 days)  
            medium_change = (current_price - df['Close'].iloc[-21]) / df['Close'].iloc[-21] if len(df) > 20 else 0
            
            # Moving average trend
            sma_20 = df['Close'].rolling(20).mean()
            sma_50 = df['Close'].rolling(50).mean()
            
            ma_trend = 'bullish' if sma_20.iloc[-1] > sma_50.iloc[-1] else 'bearish'
            
            # Overall direction
            if short_change > 0.02:
                direction = 'up'
            elif short_change < -0.02:
                direction = 'down'
            else:
                direction = 'sideways'
            
            # Strength based on consistency
            strength = min(abs(short_change) + abs(medium_change), 1.0)
            
            return {
                'direction': direction,
                'strength': float(strength),
                'short_term_change': float(short_change * 100),
                'medium_term_change': float(medium_change * 100),
                'ma_trend': ma_trend,
                'adx': 25.0  # Default value
            }
            
        except Exception as e:
            print(f"Error in trend analysis: {e}")
            return {
                'direction': 'sideways',
                'strength': 0.5,
                'short_term_change': 0.0,
                'medium_term_change': 0.0,
                'ma_trend': 'neutral',
                'adx': 25.0
            }
    
    def detect_simple_patterns(self, df):
        """Detect basic patterns"""
        try:
            # Simple pattern detection
            recent_highs = df['High'].tail(10)
            recent_lows = df['Low'].tail(10)
            
            # Check for consolidation (low volatility)
            price_range = (recent_highs.max() - recent_lows.min()) / df['Close'].iloc[-1]
            
            patterns = {
                'consolidation': {
                    'detected': price_range < 0.05,  # Less than 5% range
                    'confidence': 0.7 if price_range < 0.05 else 0.3
                },
                'breakout': {
                    'detected': df['Close'].iloc[-1] > recent_highs.iloc[-2],
                    'confidence': 0.6
                }
            }
            
            return patterns
            
        except Exception as e:
            print(f"Error detecting patterns: {e}")
            return {
                'consolidation': {'detected': False, 'confidence': 0},
                'breakout': {'detected': False, 'confidence': 0}
            }
    
    def get_default_analysis(self):
        """Return default analysis when everything fails"""
        return {
            'basic_indicators': {
                'RSI': 50.0,
                'MACD': 0.0,
                'MACD_Signal': 0.0,
                'BB_Position': 0.5,
                'SMA_20': 100.0,
                'SMA_50': 100.0,
                'Current_Price': 100.0
            },
            'support_resistance': {
                'current_price': 100.0,
                'resistance_levels': [105.0],
                'support_levels': [95.0]
            },
            'trend_analysis': {
                'direction': 'sideways',
                'strength': 0.5,
                'short_term_change': 0.0,
                'medium_term_change': 0.0,
                'ma_trend': 'neutral',
                'adx': 25.0
            },
            'patterns': {
                'consolidation': {'detected': False, 'confidence': 0},
                'breakout': {'detected': False, 'confidence': 0}
            }
        }