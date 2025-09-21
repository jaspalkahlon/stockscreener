# trading_recommendations.py
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import yfinance as yf
from enhanced_technical import EnhancedTechnicalAnalysis
from ml_predictions import MLPredictor
from advanced_analytics import StockAnalytics

class TradingRecommendationEngine:
    def __init__(self):
        self.technical_analyzer = EnhancedTechnicalAnalysis()
        self.ml_predictor = MLPredictor()
        self.stock_analytics = StockAnalytics()
        
        # Scoring weights for different factors
        self.weights = {
            'technical': 0.35,
            'ml_prediction': 0.25,
            'momentum': 0.20,
            'risk': 0.10,
            'volume': 0.10
        }
    
    def generate_recommendation(self, symbol, time_horizon_days=30):
        """Generate comprehensive buy/sell recommendation"""
        try:
            # Get comprehensive analysis
            analysis_data = self._get_comprehensive_data(symbol, time_horizon_days)
            
            if not analysis_data:
                return None
            
            # Calculate individual scores
            scores = self._calculate_scores(analysis_data, time_horizon_days)
            
            # Generate final recommendation
            recommendation = self._generate_final_recommendation(scores, analysis_data, time_horizon_days)
            
            return recommendation
            
        except Exception as e:
            print(f"Error generating recommendation for {symbol}: {e}")
            return None
    
    def _get_comprehensive_data(self, symbol, time_horizon_days):
        """Gather all necessary data for analysis"""
        try:
            # Get stock data
            ticker = yf.Ticker(symbol + ".NS")
            df = ticker.history(period="1y")
            
            if df.empty:
                return None
            
            # Technical analysis
            technical_analysis = self.technical_analyzer.get_comprehensive_analysis(symbol)
            
            # ML predictions for different horizons
            ml_predictions = {}
            for days in [7, 14, 30, 60, 90]:
                if days <= time_horizon_days:
                    pred = self.ml_predictor.predict_future_price(symbol, days)
                    if pred:
                        ml_predictions[days] = pred
            
            # Price projections
            fig, projections = self.technical_analyzer.create_projection_chart(symbol, time_horizon_days)
            
            # Current market data
            current_price = df['Close'].iloc[-1]
            current_volume = df['Volume'].iloc[-1]
            avg_volume = df['Volume'].rolling(20).mean().iloc[-1]
            
            # Risk metrics
            returns = df['Close'].pct_change().dropna()
            volatility = returns.std() * np.sqrt(252)  # Annualized
            sharpe_ratio = (returns.mean() * 252) / volatility if volatility > 0 else 0
            
            return {
                'df': df,
                'technical_analysis': technical_analysis,
                'ml_predictions': ml_predictions,
                'projections': projections,
                'current_price': current_price,
                'current_volume': current_volume,
                'avg_volume': avg_volume,
                'volatility': volatility,
                'sharpe_ratio': sharpe_ratio,
                'returns': returns
            }
            
        except Exception as e:
            print(f"Error gathering data: {e}")
            return None
    
    def _calculate_scores(self, data, time_horizon_days):
        """Calculate individual component scores"""
        scores = {}
        
        # Technical Score (0-100)
        scores['technical'] = self._calculate_technical_score(data['technical_analysis'])
        
        # ML Prediction Score (0-100)
        scores['ml_prediction'] = self._calculate_ml_score(data['ml_predictions'], data['current_price'], time_horizon_days)
        
        # Momentum Score (0-100)
        scores['momentum'] = self._calculate_momentum_score(data['df'], data['technical_analysis'])
        
        # Risk Score (0-100, higher is better risk-adjusted return)
        scores['risk'] = self._calculate_risk_score(data['volatility'], data['sharpe_ratio'], data['returns'])
        
        # Volume Score (0-100)
        scores['volume'] = self._calculate_volume_score(data['current_volume'], data['avg_volume'], data['technical_analysis'])
        
        return scores
    
    def _calculate_technical_score(self, technical_analysis):
        """Calculate technical analysis score"""
        if not technical_analysis:
            return 50  # Neutral
        
        score = 50  # Start neutral
        
        # RSI analysis
        basic = technical_analysis.get('basic_indicators', {})
        rsi = basic.get('RSI', 50)
        
        if rsi < 30:
            score += 20  # Oversold - bullish
        elif rsi > 70:
            score -= 20  # Overbought - bearish
        elif 40 <= rsi <= 60:
            score += 5   # Neutral zone - slightly positive
        
        # MACD analysis
        macd = basic.get('MACD', 0)
        macd_signal = basic.get('MACD_Signal', 0)
        
        if macd > macd_signal:
            score += 15  # Bullish crossover
        else:
            score -= 10  # Bearish crossover
        
        # Trend analysis
        trend = technical_analysis.get('trend_analysis', {})
        direction = trend.get('direction', 'neutral')
        strength = trend.get('strength', 0.5)
        
        if direction == 'up':
            score += int(strength * 20)
        elif direction == 'down':
            score -= int(strength * 20)
        
        # Support/Resistance analysis
        sr = technical_analysis.get('support_resistance', {})
        current_price = sr.get('current_price', 0)
        resistance_levels = sr.get('resistance_levels', [])
        support_levels = sr.get('support_levels', [])
        
        if resistance_levels and current_price > 0:
            nearest_resistance = resistance_levels[0]
            resistance_distance = (nearest_resistance - current_price) / current_price
            if resistance_distance > 0.05:  # More than 5% upside to resistance
                score += 10
            elif resistance_distance < 0.02:  # Close to resistance
                score -= 5
        
        if support_levels and current_price > 0:
            nearest_support = support_levels[0]
            support_distance = (current_price - nearest_support) / current_price
            if support_distance < 0.02:  # Close to support
                score += 5  # Potential bounce
        
        return max(0, min(100, score))
    
    def _calculate_ml_score(self, ml_predictions, current_price, time_horizon_days):
        """Calculate ML prediction score"""
        if not ml_predictions or current_price <= 0:
            return 50  # Neutral
        
        # Find the closest prediction to our time horizon
        best_prediction = None
        for days in sorted(ml_predictions.keys()):
            if days <= time_horizon_days:
                best_prediction = ml_predictions[days]
        
        if not best_prediction:
            return 50
        
        # Calculate expected return
        predicted_price = best_prediction.get('predicted_price', current_price)
        expected_return = (predicted_price - current_price) / current_price
        
        # Convert to score (0-100)
        # -20% return = 0, 0% return = 50, +20% return = 100
        score = 50 + (expected_return * 250)
        
        # Adjust for confidence
        confidence = best_prediction.get('confidence', 0.5)
        score = 50 + (score - 50) * confidence
        
        return max(0, min(100, score))
    
    def _calculate_momentum_score(self, df, technical_analysis):
        """Calculate momentum score"""
        score = 50  # Start neutral
        
        # Price momentum (recent performance)
        recent_returns = df['Close'].pct_change().tail(20)
        momentum_20d = recent_returns.mean()
        
        # Convert to score
        score += momentum_20d * 1000  # Scale up
        
        # Volume momentum
        volume_analysis = technical_analysis.get('volume_analysis', {})
        vol_trend = volume_analysis.get('volume_trend', 'neutral')
        
        if vol_trend == 'increasing':
            score += 10
        elif vol_trend == 'decreasing':
            score -= 5
        
        # Moving average momentum
        basic = technical_analysis.get('basic_indicators', {})
        price_vs_sma20 = basic.get('Price_vs_SMA20', 0)
        price_vs_sma50 = basic.get('Price_vs_SMA50', 0)
        
        if price_vs_sma20 > 0 and price_vs_sma50 > 0:
            score += 15  # Above both MAs
        elif price_vs_sma20 > 0:
            score += 5   # Above short-term MA
        elif price_vs_sma20 < 0 and price_vs_sma50 < 0:
            score -= 15  # Below both MAs
        
        return max(0, min(100, score))
    
    def _calculate_risk_score(self, volatility, sharpe_ratio, returns):
        """Calculate risk-adjusted score"""
        score = 50  # Start neutral
        
        # Volatility analysis (lower volatility is better for most strategies)
        if volatility < 0.2:  # Low volatility
            score += 10
        elif volatility > 0.5:  # High volatility
            score -= 15
        
        # Sharpe ratio analysis
        if sharpe_ratio > 1.0:
            score += 20
        elif sharpe_ratio > 0.5:
            score += 10
        elif sharpe_ratio < 0:
            score -= 20
        
        # Drawdown analysis
        cumulative_returns = (1 + returns).cumprod()
        rolling_max = cumulative_returns.expanding().max()
        drawdown = (cumulative_returns - rolling_max) / rolling_max
        max_drawdown = drawdown.min()
        
        if max_drawdown > -0.1:  # Less than 10% max drawdown
            score += 10
        elif max_drawdown < -0.3:  # More than 30% max drawdown
            score -= 15
        
        return max(0, min(100, score))
    
    def _calculate_volume_score(self, current_volume, avg_volume, technical_analysis):
        """Calculate volume-based score"""
        score = 50  # Start neutral
        
        # Volume ratio analysis
        if avg_volume > 0:
            volume_ratio = current_volume / avg_volume
            
            if volume_ratio > 2.0:  # High volume
                score += 15
            elif volume_ratio > 1.5:
                score += 10
            elif volume_ratio < 0.5:  # Low volume
                score -= 10
        
        # Volume trend analysis
        volume_analysis = technical_analysis.get('volume_analysis', {})
        
        if volume_analysis.get('volume_breakout', False):
            score += 20  # Volume breakout is very bullish
        
        obv_trend = volume_analysis.get('obv_trend', 'neutral')
        if obv_trend == 'bullish':
            score += 10
        elif obv_trend == 'bearish':
            score -= 10
        
        return max(0, min(100, score))
    
    def _generate_final_recommendation(self, scores, data, time_horizon_days):
        """Generate final recommendation based on all scores"""
        # Calculate weighted score
        weighted_score = 0
        for component, score in scores.items():
            weighted_score += score * self.weights.get(component, 0)
        
        # Determine recommendation
        if weighted_score >= 75:
            action = "STRONG BUY"
            confidence = "High"
        elif weighted_score >= 60:
            action = "BUY"
            confidence = "Medium-High"
        elif weighted_score >= 55:
            action = "WEAK BUY"
            confidence = "Medium"
        elif weighted_score >= 45:
            action = "HOLD"
            confidence = "Medium"
        elif weighted_score >= 40:
            action = "WEAK SELL"
            confidence = "Medium"
        elif weighted_score >= 25:
            action = "SELL"
            confidence = "Medium-High"
        else:
            action = "STRONG SELL"
            confidence = "High"
        
        # Calculate target price and stop loss
        current_price = data['current_price']
        volatility = data['volatility']
        
        # Target price based on projections and ML predictions
        target_price = self._calculate_target_price(data, time_horizon_days, weighted_score)
        
        # Stop loss based on volatility and support levels
        stop_loss = self._calculate_stop_loss(data, weighted_score)
        
        # Risk-reward ratio
        if action in ["STRONG BUY", "BUY", "WEAK BUY"]:
            risk_reward = (target_price - current_price) / (current_price - stop_loss) if current_price > stop_loss else 0
        else:
            risk_reward = 0
        
        # Generate reasoning
        reasoning = self._generate_reasoning(scores, data, action)
        
        return {
            'action': action,
            'confidence': confidence,
            'overall_score': weighted_score,
            'component_scores': scores,
            'current_price': current_price,
            'target_price': target_price,
            'stop_loss': stop_loss,
            'risk_reward_ratio': risk_reward,
            'time_horizon_days': time_horizon_days,
            'expected_return': ((target_price - current_price) / current_price * 100) if current_price > 0 else 0,
            'reasoning': reasoning,
            'weights_used': self.weights
        }
    
    def _calculate_target_price(self, data, time_horizon_days, weighted_score):
        """Calculate target price based on various factors"""
        current_price = data['current_price']
        
        # Start with current price
        target_price = current_price
        
        # Use ML predictions if available
        ml_predictions = data['ml_predictions']
        if ml_predictions:
            # Find closest prediction
            best_days = min(ml_predictions.keys(), key=lambda x: abs(x - time_horizon_days))
            if best_days in ml_predictions:
                ml_target = ml_predictions[best_days].get('predicted_price', current_price)
                target_price = (target_price + ml_target) / 2  # Average with current
        
        # Use projections
        projections = data.get('projections', {})
        if projections and 'ensemble' in projections:
            ensemble_proj = projections['ensemble']
            if 'prices' in ensemble_proj and len(ensemble_proj['prices']) > 0:
                # Get price at our time horizon (or closest)
                days_available = len(ensemble_proj['prices'])
                target_index = min(time_horizon_days - 1, days_available - 1)
                proj_target = ensemble_proj['prices'][target_index]
                target_price = (target_price + proj_target) / 2
        
        # Adjust based on overall score
        score_adjustment = (weighted_score - 50) / 100  # -0.5 to +0.5
        target_price *= (1 + score_adjustment * 0.2)  # Max 10% adjustment
        
        # Use resistance levels as ceiling for buy recommendations
        technical_analysis = data.get('technical_analysis', {})
        if technical_analysis:
            sr = technical_analysis.get('support_resistance', {})
            resistance_levels = sr.get('resistance_levels', [])
            if resistance_levels and weighted_score > 50:
                nearest_resistance = resistance_levels[0]
                target_price = min(target_price, nearest_resistance * 0.95)  # 5% below resistance
        
        return target_price
    
    def _calculate_stop_loss(self, data, weighted_score):
        """Calculate stop loss based on support levels and volatility"""
        current_price = data['current_price']
        volatility = data['volatility']
        
        # Base stop loss on volatility (2 standard deviations)
        daily_vol = volatility / np.sqrt(252)
        vol_stop = current_price * (1 - 2 * daily_vol)
        
        # Use support levels
        technical_analysis = data.get('technical_analysis', {})
        support_stop = current_price * 0.9  # Default 10% stop
        
        if technical_analysis:
            sr = technical_analysis.get('support_resistance', {})
            support_levels = sr.get('support_levels', [])
            if support_levels:
                nearest_support = support_levels[0]
                support_stop = nearest_support * 0.98  # 2% below support
        
        # Use the higher of the two (less aggressive)
        stop_loss = max(vol_stop, support_stop)
        
        # Adjust based on recommendation strength
        if weighted_score > 70:  # Strong buy - can afford tighter stop
            stop_loss = max(stop_loss, current_price * 0.92)  # Max 8% stop
        elif weighted_score < 30:  # Strong sell - wider stop for short positions
            stop_loss = min(stop_loss, current_price * 1.15)  # 15% stop for shorts
        
        return stop_loss
    
    def _generate_reasoning(self, scores, data, action):
        """Generate human-readable reasoning for the recommendation"""
        reasoning = []
        
        # Technical analysis reasoning
        tech_score = scores.get('technical', 50)
        if tech_score > 65:
            reasoning.append("Strong technical indicators support upward movement")
        elif tech_score < 35:
            reasoning.append("Technical indicators suggest downward pressure")
        
        # ML prediction reasoning
        ml_score = scores.get('ml_prediction', 50)
        if ml_score > 60:
            reasoning.append("Machine learning models predict positive price movement")
        elif ml_score < 40:
            reasoning.append("ML models indicate potential price decline")
        
        # Momentum reasoning
        momentum_score = scores.get('momentum', 50)
        if momentum_score > 60:
            reasoning.append("Strong positive momentum in price and volume")
        elif momentum_score < 40:
            reasoning.append("Negative momentum suggests caution")
        
        # Risk reasoning
        risk_score = scores.get('risk', 50)
        if risk_score > 60:
            reasoning.append("Favorable risk-adjusted returns profile")
        elif risk_score < 40:
            reasoning.append("Higher risk profile requires careful position sizing")
        
        # Volume reasoning
        volume_score = scores.get('volume', 50)
        if volume_score > 60:
            reasoning.append("Strong volume support confirms price movement")
        elif volume_score < 40:
            reasoning.append("Weak volume may limit price movement")
        
        # Specific technical factors
        technical_analysis = data.get('technical_analysis', {})
        if technical_analysis:
            basic = technical_analysis.get('basic_indicators', {})
            rsi = basic.get('RSI', 50)
            
            if rsi > 70:
                reasoning.append("RSI indicates overbought conditions - consider profit taking")
            elif rsi < 30:
                reasoning.append("RSI shows oversold conditions - potential buying opportunity")
        
        if not reasoning:
            reasoning.append("Mixed signals suggest a neutral stance")
        
        return reasoning