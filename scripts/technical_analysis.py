"""
Technical Analysis Module
Implements various technical indicators and chart pattern detection
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from scipy.signal import argrelextrema
from scipy import stats


class TechnicalIndicators:
    """Calculate common technical indicators"""
    
    @staticmethod
    def sma(data: pd.Series, window: int) -> pd.Series:
        """Simple Moving Average"""
        return data.rolling(window=window).mean()
    
    @staticmethod
    def ema(data: pd.Series, window: int) -> pd.Series:
        """Exponential Moving Average"""
        return data.ewm(span=window, adjust=False).mean()
    
    @staticmethod
    def rsi(data: pd.Series, window: int = 14) -> pd.Series:
        """Relative Strength Index"""
        delta = data.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    @staticmethod
    def macd(data: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> Dict[str, pd.Series]:
        """MACD (Moving Average Convergence Divergence)"""
        ema_fast = data.ewm(span=fast, adjust=False).mean()
        ema_slow = data.ewm(span=slow, adjust=False).mean()
        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm(span=signal, adjust=False).mean()
        histogram = macd_line - signal_line
        return {
            'macd': macd_line,
            'signal': signal_line,
            'histogram': histogram
        }
    
    @staticmethod
    def bollinger_bands(data: pd.Series, window: int = 20, num_std: int = 2) -> Dict[str, pd.Series]:
        """Bollinger Bands"""
        sma = data.rolling(window=window).mean()
        std = data.rolling(window=window).std()
        upper_band = sma + (std * num_std)
        lower_band = sma - (std * num_std)
        return {
            'middle': sma,
            'upper': upper_band,
            'lower': lower_band
        }
    
    @staticmethod
    def atr(high: pd.Series, low: pd.Series, close: pd.Series, window: int = 14) -> pd.Series:
        """Average True Range - measures trend strength and volatility"""
        tr1 = high - low
        tr2 = abs(high - close.shift())
        tr3 = abs(low - close.shift())
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        atr = tr.rolling(window=window).mean()
        return atr
    
    @staticmethod
    def stochastic_oscillator(high: pd.Series, low: pd.Series, close: pd.Series, 
                               k_window: int = 14, d_window: int = 3) -> Dict[str, pd.Series]:
        """
        Stochastic Oscillator - predicts potential market tops and bottoms
        Compares closing price to high-low range over a given period
        """
        low_min = low.rolling(window=k_window).min()
        high_max = high.rolling(window=k_window).max()
        
        # Calculate %K
        k_percent = 100 * ((close - low_min) / (high_max - low_min))
        
        # Calculate %D (smoothed %K)
        d_percent = k_percent.rolling(window=d_window).mean()
        
        return {
            'k': k_percent,
            'd': d_percent
        }
    
    @staticmethod
    def ichimoku_cloud(high: pd.Series, low: pd.Series, close: pd.Series,
                       tenkan_period: int = 9, kijun_period: int = 26, 
                       senkou_span_b_period: int = 52) -> Dict[str, pd.Series]:
        """
        Ichimoku Cloud - comprehensive leading indicator for support/resistance and trend direction
        """
        # Tenkan-sen (Conversion Line) - (9-period high + 9-period low) / 2
        tenkan_sen = (high.rolling(window=tenkan_period).max() + 
                     low.rolling(window=tenkan_period).min()) / 2
        
        # Kijun-sen (Base Line) - (26-period high + 26-period low) / 2
        kijun_sen = (high.rolling(window=kijun_period).max() + 
                   low.rolling(window=kijun_period).min()) / 2
        
        # Senkou Span A (Leading Span A) - (Tenkan-sen + Kijun-sen) / 2, shifted 26 periods ahead
        senkou_span_a = ((tenkan_sen + kijun_sen) / 2).shift(kijun_period)
        
        # Senkou Span B (Leading Span B) - (52-period high + 52-period low) / 2, shifted 26 periods ahead
        senkou_span_b = ((high.rolling(window=senkou_span_b_period).max() + 
                         low.rolling(window=senkou_span_b_period).min()) / 2).shift(kijun_period)
        
        # Chikou Span (Lagging Span) - Current close, shifted 26 periods behind
        chikou_span = close.shift(-kijun_period)
        
        return {
            'tenkan_sen': tenkan_sen,
            'kijun_sen': kijun_sen,
            'senkou_span_a': senkou_span_a,
            'senkou_span_b': senkou_span_b,
            'chikou_span': chikou_span
        }
    
    @staticmethod
    def macd_rsi(data: pd.Series, rsi_window: int = 14, 
                 macd_fast: int = 12, macd_slow: int = 26, macd_signal: int = 9) -> Dict[str, pd.Series]:
        """
        MACD RSI - combines MACD and RSI to identify overbought/oversold zones and divergences
        """
        # Calculate RSI
        delta = data.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=rsi_window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=rsi_window).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        # Calculate MACD
        ema_fast = data.ewm(span=macd_fast, adjust=False).mean()
        ema_slow = data.ewm(span=macd_slow, adjust=False).mean()
        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm(span=macd_signal, adjust=False).mean()
        histogram = macd_line - signal_line
        
        # Generate MACD RSI signals
        # Signal when MACD histogram is positive and RSI is not overbought (>70)
        # or when MACD histogram is negative and RSI is not oversold (<30)
        macd_rsi_signal = pd.Series(0, index=data.index)
        macd_rsi_signal[(histogram > 0) & (rsi < 70)] = 1  # Buy signal
        macd_rsi_signal[(histogram < 0) & (rsi > 30)] = -1  # Sell signal
        
        return {
            'rsi': rsi,
            'macd': macd_line,
            'signal': signal_line,
            'histogram': histogram,
            'macd_rsi_signal': macd_rsi_signal
        }
    
    @staticmethod
    def adx(high: pd.Series, low: pd.Series, close: pd.Series, window: int = 14) -> Dict[str, pd.Series]:
        """
        ADX (Average Directional Index) - measures trend strength
        Ideal for enhancing trend-following strategies
        """
        # Calculate True Range
        tr1 = high - low
        tr2 = abs(high - close.shift())
        tr3 = abs(low - close.shift())
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        
        # Calculate +DM and -DM
        plus_dm = high.diff()
        minus_dm = -low.diff()
        
        plus_dm[plus_dm < 0] = 0
        minus_dm[minus_dm < 0] = 0
        
        # Calculate smoothed TR, +DM, -DM
        atr = tr.rolling(window=window).mean()
        plus_di = 100 * (plus_dm.rolling(window=window).mean() / atr)
        minus_di = 100 * (minus_dm.rolling(window=window).mean() / atr)
        
        # Calculate DX
        dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di)
        
        # Calculate ADX
        adx = dx.rolling(window=window).mean()
        
        return {
            'adx': adx,
            'plus_di': plus_di,
            'minus_di': minus_di
        }


class ChartPatterns:
    """Detect chart patterns for technical analysis"""
    
    def __init__(self, data: pd.DataFrame):
        """
        Initialize with OHLCV data
        
        Args:
            data: DataFrame with Open, High, Low, Close columns
        """
        self.data = data
        self.close = data['Close']
        self.high = data['High']
        self.low = data['Low']
    
    def find_peaks_and_troughs(self, window: int = 5) -> Tuple[np.ndarray, np.ndarray]:
        """
        Find local peaks and troughs in price data
        
        Args:
            window: Window size for peak/trough detection
        
        Returns:
            Tuple of (peaks, troughs) indices
        """
        peaks = argrelextrema(self.close.values, np.greater, order=window)[0]
        troughs = argrelextrema(self.close.values, np.less, order=window)[0]
        return peaks, troughs
    
    def detect_head_and_shoulders(self, window: int = 5) -> Dict[str, any]:
        """
        Detect Head and Shoulders pattern (bearish reversal)
        
        Returns:
            Dictionary with pattern detection results
        """
        peaks, troughs = self.find_peaks_and_troughs(window)
        
        if len(peaks) < 3:
            return {'pattern': None, 'confidence': 0}
        
        # Look for 3 peaks where middle is highest
        recent_peaks = peaks[-3:]
        peak_values = self.close.iloc[recent_peaks].values
        
        # Check if middle peak is highest
        if peak_values[1] > peak_values[0] and peak_values[1] > peak_values[2]:
            # Check if outer peaks are roughly equal (within 5%)
            outer_diff = abs(peak_values[0] - peak_values[2]) / peak_values[0]
            if outer_diff < 0.05:
                confidence = 0.7 + (1 - outer_diff) * 0.3
                return {
                    'pattern': 'Head and Shoulders',
                    'type': 'bearish',
                    'confidence': confidence,
                    'peaks': recent_peaks,
                    'neckline': min(peak_values[0], peak_values[2])
                }
        
        return {'pattern': None, 'confidence': 0}
    
    def detect_double_top(self, window: int = 5, tolerance: float = 0.03) -> Dict[str, any]:
        """
        Detect Double Top pattern (bearish reversal)
        
        Args:
            window: Window size for peak detection
            tolerance: Tolerance for peak equality (3%)
        
        Returns:
            Dictionary with pattern detection results
        """
        peaks, _ = self.find_peaks_and_troughs(window)
        
        if len(peaks) < 2:
            return {'pattern': None, 'confidence': 0}
        
        # Check last two peaks
        recent_peaks = peaks[-2:]
        peak_values = self.close.iloc[recent_peaks].values
        
        # Check if peaks are roughly equal
        peak_diff = abs(peak_values[0] - peak_values[1]) / peak_values[0]
        
        if peak_diff < tolerance:
            confidence = 0.7 + (1 - peak_diff / tolerance) * 0.3
            return {
                'pattern': 'Double Top',
                'type': 'bearish',
                'confidence': confidence,
                'peaks': recent_peaks,
                'support_level': min(peak_values)
            }
        
        return {'pattern': None, 'confidence': 0}
    
    def detect_double_bottom(self, window: int = 5, tolerance: float = 0.03) -> Dict[str, any]:
        """
        Detect Double Bottom pattern (bullish reversal)
        
        Args:
            window: Window size for trough detection
            tolerance: Tolerance for trough equality (3%)
        
        Returns:
            Dictionary with pattern detection results
        """
        _, troughs = self.find_peaks_and_troughs(window)
        
        if len(troughs) < 2:
            return {'pattern': None, 'confidence': 0}
        
        # Check last two troughs
        recent_troughs = troughs[-2:]
        trough_values = self.close.iloc[recent_troughs].values
        
        # Check if troughs are roughly equal
        trough_diff = abs(trough_values[0] - trough_values[1]) / trough_values[0]
        
        if trough_diff < tolerance:
            confidence = 0.7 + (1 - trough_diff / tolerance) * 0.3
            return {
                'pattern': 'Double Bottom',
                'type': 'bullish',
                'confidence': confidence,
                'troughs': recent_troughs,
                'resistance_level': max(trough_values)
            }
        
        return {'pattern': None, 'confidence': 0}
    
    def detect_triangle_pattern(self, window: int = 10) -> Dict[str, any]:
        """
        Detect Triangle patterns (Ascending, Descending, Symmetrical)
        
        Returns:
            Dictionary with pattern detection results
        """
        if len(self.data) < window * 2:
            return {'pattern': None, 'confidence': 0}
        
        recent_data = self.data.tail(window * 2)
        highs = recent_data['High'].values
        lows = recent_data['Low'].values
        
        # Calculate trend lines
        x = np.arange(len(highs))
        
        # High trend line
        high_slope, high_intercept, _, _, _ = stats.linregress(x, highs)
        
        # Low trend line
        low_slope, low_intercept, _, _, _ = stats.linregress(x, lows)
        
        # Determine pattern type
        if abs(high_slope) < 0.01 and low_slope > 0.01:
            pattern = 'Ascending Triangle'
            pattern_type = 'bullish'
            confidence = 0.6
        elif high_slope < -0.01 and abs(low_slope) < 0.01:
            pattern = 'Descending Triangle'
            pattern_type = 'bearish'
            confidence = 0.6
        elif abs(high_slope - low_slope) < 0.01:
            pattern = 'Symmetrical Triangle'
            pattern_type = 'neutral'
            confidence = 0.5
        else:
            return {'pattern': None, 'confidence': 0}
        
        return {
            'pattern': pattern,
            'type': pattern_type,
            'confidence': confidence,
            'high_slope': high_slope,
            'low_slope': low_slope
        }
    
    def detect_cup_and_handle(self, window: int = 20) -> Dict[str, any]:
        """
        Detect Cup and Handle pattern (bullish continuation)
        
        Returns:
            Dictionary with pattern detection results
        """
        if len(self.data) < window:
            return {'pattern': None, 'confidence': 0}
        
        recent_data = self.data.tail(window)
        prices = recent_data['Close'].values
        
        # Find the lowest point (cup bottom)
        min_idx = np.argmin(prices)
        min_price = prices[min_idx]
        
        # Check for U-shape (cup)
        if min_idx < len(prices) * 0.3 or min_idx > len(prices) * 0.7:
            return {'pattern': None, 'confidence': 0}
        
        # Check for handle (slight dip after recovery)
        if min_idx + 5 < len(prices):
            after_cup = prices[min_idx + 5:]
            if len(after_cup) > 5:
                handle_dip = np.min(after_cup) - np.max(after_cup[:len(after_cup)//2])
                if handle_dip < 0 and abs(handle_dip) / np.max(after_cup[:len(after_cup)//2]) < 0.1:
                    return {
                        'pattern': 'Cup and Handle',
                        'type': 'bullish',
                        'confidence': 0.6,
                        'cup_bottom': min_price
                    }
        
        return {'pattern': None, 'confidence': 0}
    
    def detect_all_patterns(self) -> List[Dict[str, any]]:
        """
        Detect all chart patterns
        
        Returns:
            List of detected patterns with their details
        """
        patterns = []
        
        # Detect all patterns
        patterns.append(self.detect_head_and_shoulders())
        patterns.append(self.detect_double_top())
        patterns.append(self.detect_double_bottom())
        patterns.append(self.detect_triangle_pattern())
        patterns.append(self.detect_cup_and_handle())
        
        # Filter out None patterns
        patterns = [p for p in patterns if p['pattern'] is not None]
        
        return patterns


class TechnicalAnalyzer:
    """Main class for technical analysis"""
    
    def __init__(self, data: pd.DataFrame):
        """
        Initialize with OHLCV data
        
        Args:
            data: DataFrame with Open, High, Low, Close, Volume columns
        """
        self.data = data
        self.indicators = TechnicalIndicators()
        self.patterns = ChartPatterns(data)
    
    def calculate_all_indicators(self) -> Dict[str, any]:
        """
        Calculate all technical indicators
        
        Returns:
            Dictionary with all indicators
        """
        close = self.data['Close']
        high = self.data['High']
        low = self.data['Low']
        
        return {
            'sma_20': self.indicators.sma(close, 20),
            'sma_50': self.indicators.sma(close, 50),
            'sma_200': self.indicators.sma(close, 200),
            'ema_12': self.indicators.ema(close, 12),
            'ema_26': self.indicators.ema(close, 26),
            'rsi': self.indicators.rsi(close),
            'macd': self.indicators.macd(close),
            'bollinger_bands': self.indicators.bollinger_bands(close),
            'atr': self.indicators.atr(high, low, close),
            'stochastic': self.indicators.stochastic_oscillator(high, low, close),
            'ichimoku': self.indicators.ichimoku_cloud(high, low, close),
            'macd_rsi': self.indicators.macd_rsi(close),
            'adx': self.indicators.adx(high, low, close)
        }
    
    def detect_patterns(self) -> List[Dict[str, any]]:
        """
        Detect all chart patterns
        
        Returns:
            List of detected patterns
        """
        return self.patterns.detect_all_patterns()
    
    def generate_signals(self) -> Dict[str, str]:
        """
        Generate buy/sell signals based on indicators and patterns
        
        Returns:
            Dictionary with signals
        """
        indicators = self.calculate_all_indicators()
        patterns = self.detect_patterns()
        
        signals = {
            'overall': 'HOLD',
            'rsi': 'HOLD',
            'macd': 'HOLD',
            'patterns': 'HOLD'
        }
        
        # RSI signal
        current_rsi = indicators['rsi'].iloc[-1]
        if current_rsi > 70:
            signals['rsi'] = 'SELL'
        elif current_rsi < 30:
            signals['rsi'] = 'BUY'
        
        # MACD signal
        macd = indicators['macd']
        if macd['macd'].iloc[-1] > macd['signal'].iloc[-1]:
            signals['macd'] = 'BUY'
        else:
            signals['macd'] = 'SELL'
        
        # Pattern-based signal
        if patterns:
            bullish_patterns = [p for p in patterns if p['type'] == 'bullish']
            bearish_patterns = [p for p in patterns if p['type'] == 'bearish']
            
            if bullish_patterns and not bearish_patterns:
                signals['patterns'] = 'BUY'
            elif bearish_patterns and not bullish_patterns:
                signals['patterns'] = 'SELL'
        
        # Overall signal (simple majority)
        signal_votes = [signals['rsi'], signals['macd'], signals['patterns']]
        buy_votes = signal_votes.count('BUY')
        sell_votes = signal_votes.count('SELL')
        
        if buy_votes > sell_votes:
            signals['overall'] = 'BUY'
        elif sell_votes > buy_votes:
            signals['overall'] = 'SELL'
        
        return signals
    
    def calculate_entry_exit_levels(self, risk_reward_ratio: float = 2.0) -> Dict[str, float]:
        """
        Calculate entry, stop loss, and take profit levels based on technical analysis
        
        Args:
            risk_reward_ratio: Risk to reward ratio (default 2.0)
        
        Returns:
            Dictionary with entry, stop loss, and take profit levels
        """
        indicators = self.calculate_all_indicators()
        signals = self.generate_signals()
        
        current_price = self.data['Close'].iloc[-1]
        high = self.data['High'].iloc[-1]
        low = self.data['Low'].iloc[-1]
        atr = indicators['atr'].iloc[-1]
        
        # Calculate support and resistance levels
        recent_data = self.data.tail(20)
        support_level = recent_data['Low'].min()
        resistance_level = recent_data['High'].max()
        
        # Calculate entry level based on signal
        if signals['overall'] == 'BUY':
            # Entry: Current price or slightly above recent resistance for breakout
            entry_level = current_price
            if current_price > resistance_level * 0.98:
                entry_level = current_price
            else:
                entry_level = (current_price + resistance_level) / 2
            
            # Stop loss: Below support or based on ATR
            stop_loss = max(support_level, current_price - (2 * atr))
            
            # Take profit: Based on risk-reward ratio
            risk = entry_level - stop_loss
            take_profit = entry_level + (risk * risk_reward_ratio)
            
        elif signals['overall'] == 'SELL':
            # Entry: Current price or slightly below recent support for breakdown
            entry_level = current_price
            if current_price < support_level * 1.02:
                entry_level = current_price
            else:
                entry_level = (current_price + support_level) / 2
            
            # Stop loss: Above resistance or based on ATR
            stop_loss = min(resistance_level, current_price + (2 * atr))
            
            # Take profit: Based on risk-reward ratio
            risk = stop_loss - entry_level
            take_profit = entry_level - (risk * risk_reward_ratio)
            
        else:
            # HOLD signal - use current levels
            entry_level = current_price
            stop_loss = current_price - (2 * atr)
            take_profit = current_price + (2 * atr)
        
        # Calculate additional target levels
        if signals['overall'] == 'BUY':
            target1 = entry_level + (entry_level - stop_loss) * 1.5
            target2 = entry_level + (entry_level - stop_loss) * 2.0
            target3 = entry_level + (entry_level - stop_loss) * 3.0
        else:
            target1 = entry_level - (stop_loss - entry_level) * 1.5
            target2 = entry_level - (stop_loss - entry_level) * 2.0
            target3 = entry_level - (stop_loss - entry_level) * 3.0
        
        return {
            'entry': entry_level,
            'stop_loss': stop_loss,
            'take_profit': take_profit,
            'target1': target1,
            'target2': target2,
            'target3': target3,
            'support': support_level,
            'resistance': resistance_level,
            'risk': abs(entry_level - stop_loss),
            'reward': abs(take_profit - entry_level),
            'risk_reward_ratio': abs(take_profit - entry_level) / abs(entry_level - stop_loss) if abs(entry_level - stop_loss) > 0 else 0
        }
