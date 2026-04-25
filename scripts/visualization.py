"""
Visualization Module
Creates professional charts for stock analysis
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from datetime import datetime

# Set style
sns.set_style("darkgrid")
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 10


class StockVisualizer:
    """Create various stock charts and visualizations"""
    
    def __init__(self, data: pd.DataFrame):
        """
        Initialize with OHLCV data
        
        Args:
            data: DataFrame with Open, High, Low, Close, Volume columns
        """
        self.data = data
        self.close = data['Close']
        self.high = data['High']
        self.low = data['Low']
        self.open = data['Open']
        self.volume = data['Volume']
    
    def plot_price_chart(self, title: str = "Stock Price Chart", show_volume: bool = True, 
                         show_ma: bool = True, ma_periods: List[int] = [20, 50, 200]) -> plt.Figure:
        """
        Plot basic price chart with optional volume and moving averages
        
        Args:
            title: Chart title
            show_volume: Whether to show volume
            show_ma: Whether to show moving averages
            ma_periods: List of MA periods to show
        
        Returns:
            matplotlib Figure object
        """
        fig, axes = plt.subplots(2 if show_volume else 1, 1, 
                                 figsize=(14, 10 if show_volume else 8),
                                 gridspec_kw={'height_ratios': [3, 1] if show_volume else [1]})
        
        if show_volume:
            ax1, ax2 = axes
        else:
            ax1 = axes
        
        # Plot price
        ax1.plot(self.data.index, self.close, label='Close Price', linewidth=2, color='blue')
        
        # Add moving averages
        if show_ma:
            colors = ['orange', 'green', 'red']
            for i, period in enumerate(ma_periods):
                ma = self.close.rolling(window=period).mean()
                ax1.plot(self.data.index, ma, label=f'MA {period}', 
                        linewidth=1.5, color=colors[i % len(colors)], alpha=0.7)
        
        ax1.set_title(title, fontsize=14, fontweight='bold')
        ax1.set_ylabel('Price', fontsize=12)
        ax1.legend(loc='best')
        ax1.grid(True, alpha=0.3)
        
        # Format x-axis
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax1.xaxis.set_major_locator(mdates.AutoDateLocator())
        plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        # Plot volume
        if show_volume:
            colors = ['red' if self.close.iloc[i] >= self.open.iloc[i] else 'green' 
                     for i in range(len(self.data))]
            ax2.bar(self.data.index, self.volume, color=colors, alpha=0.6)
            ax2.set_title('Volume', fontsize=12)
            ax2.set_ylabel('Volume', fontsize=10)
            ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            ax2.xaxis.set_major_locator(mdates.AutoDateLocator())
            plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')
            ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def plot_candlestick(self, title: str = "Candlestick Chart", ma_periods: List[int] = [20, 50]) -> plt.Figure:
        """
        Plot candlestick chart with moving averages
        
        Args:
            title: Chart title
            ma_periods: List of MA periods to show
        
        Returns:
            matplotlib Figure object
        """
        fig, ax = plt.subplots(figsize=(14, 8))
        
        # Calculate up and down prices
        up = self.data[self.data.Close >= self.data.Open]
        down = self.data[self.data.Close < self.data.Open]
        
        # Calculate width of candles
        width = 0.6
        width2 = 0.1
        
        # Plot up candles
        ax.bar(up.index, up.Close - up.Open, width, bottom=up.Open, color='green', alpha=0.7)
        ax.bar(up.index, up.High - up.Close, width2, bottom=up.Close, color='green', alpha=0.7)
        ax.bar(up.index, up.Low - up.Open, width2, bottom=up.Open, color='green', alpha=0.7)
        
        # Plot down candles
        ax.bar(down.index, down.Close - down.Open, width, bottom=down.Open, color='red', alpha=0.7)
        ax.bar(down.index, down.High - down.Open, width2, bottom=down.Open, color='red', alpha=0.7)
        ax.bar(down.index, down.Low - down.Close, width2, bottom=down.Close, color='red', alpha=0.7)
        
        # Add moving averages
        colors = ['orange', 'blue']
        for i, period in enumerate(ma_periods):
            ma = self.close.rolling(window=period).mean()
            ax.plot(self.data.index, ma, label=f'MA {period}', 
                   linewidth=2, color=colors[i % len(colors)], alpha=0.8)
        
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_ylabel('Price', fontsize=12)
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3)
        
        # Format x-axis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        plt.tight_layout()
        return fig
    
    def plot_technical_indicators(self, indicators: Dict[str, any]) -> plt.Figure:
        """
        Plot technical indicators (RSI, MACD, Bollinger Bands)
        
        Args:
            indicators: Dictionary of technical indicators
        
        Returns:
            matplotlib Figure object
        """
        fig, axes = plt.subplots(3, 1, figsize=(14, 12))
        
        # Plot price with Bollinger Bands
        ax1 = axes[0]
        ax1.plot(self.data.index, self.close, label='Close Price', linewidth=2, color='blue')
        
        if 'bollinger_bands' in indicators:
            bb = indicators['bollinger_bands']
            ax1.plot(self.data.index, bb['upper'], label='Upper Band', 
                    linewidth=1, color='red', alpha=0.7)
            ax1.plot(self.data.index, bb['middle'], label='Middle Band', 
                    linewidth=1, color='orange', alpha=0.7)
            ax1.plot(self.data.index, bb['lower'], label='Lower Band', 
                    linewidth=1, color='green', alpha=0.7)
            ax1.fill_between(self.data.index, bb['upper'], bb['lower'], alpha=0.1)
        
        ax1.set_title('Price with Bollinger Bands', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Price', fontsize=10)
        ax1.legend(loc='best')
        ax1.grid(True, alpha=0.3)
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        # Plot RSI
        ax2 = axes[1]
        if 'rsi' in indicators:
            rsi = indicators['rsi']
            ax2.plot(self.data.index, rsi, label='RSI', linewidth=2, color='purple')
            ax2.axhline(70, color='red', linestyle='--', alpha=0.5, label='Overbought (70)')
            ax2.axhline(30, color='green', linestyle='--', alpha=0.5, label='Oversold (30)')
            ax2.fill_between(self.data.index, 70, 30, alpha=0.1)
        
        ax2.set_title('RSI Indicator', fontsize=12, fontweight='bold')
        ax2.set_ylabel('RSI', fontsize=10)
        ax2.set_ylim(0, 100)
        ax2.legend(loc='best')
        ax2.grid(True, alpha=0.3)
        ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        # Plot MACD
        ax3 = axes[2]
        if 'macd' in indicators:
            macd = indicators['macd']
            ax3.plot(self.data.index, macd['macd'], label='MACD', linewidth=2, color='blue')
            ax3.plot(self.data.index, macd['signal'], label='Signal', linewidth=2, color='orange')
            ax3.bar(self.data.index, macd['histogram'], label='Histogram', 
                   color=macd['histogram'].apply(lambda x: 'green' if x > 0 else 'red'), alpha=0.6)
            ax3.axhline(0, color='black', linestyle='-', alpha=0.3)
        
        ax3.set_title('MACD Indicator', fontsize=12, fontweight='bold')
        ax3.set_ylabel('MACD', fontsize=10)
        ax3.legend(loc='best')
        ax3.grid(True, alpha=0.3)
        ax3.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.setp(ax3.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        plt.tight_layout()
        return fig
    
    def plot_patterns(self, patterns: List[Dict[str, any]], title: str = "Chart Patterns") -> plt.Figure:
        """
        Plot detected chart patterns on price chart
        
        Args:
            patterns: List of detected patterns
            title: Chart title
        
        Returns:
            matplotlib Figure object
        """
        fig, ax = plt.subplots(figsize=(14, 8))
        
        # Plot price
        ax.plot(self.data.index, self.close, label='Close Price', linewidth=2, color='blue')
        
        # Annotate patterns
        for pattern in patterns:
            pattern_name = pattern['pattern']
            pattern_type = pattern['type']
            confidence = pattern['confidence']
            
            # Find annotation position
            if 'peaks' in pattern:
                peak_idx = pattern['peaks'][-1]
                peak_date = self.data.index[peak_idx]
                peak_price = self.close.iloc[peak_idx]
                ax.annotate(f'{pattern_name}\n({pattern_type})\nConf: {confidence:.2f}',
                           xy=(peak_date, peak_price),
                           xytext=(10, 10), textcoords='offset points',
                           bbox=dict(boxstyle='round,pad=0.5', 
                                   facecolor='red' if pattern_type == 'bearish' else 'green',
                                   alpha=0.3),
                           arrowprops=dict(arrowstyle='->', 
                                         connectionstyle='arc3,rad=0'),
                           fontsize=9)
            elif 'troughs' in pattern:
                trough_idx = pattern['troughs'][-1]
                trough_date = self.data.index[trough_idx]
                trough_price = self.close.iloc[trough_idx]
                ax.annotate(f'{pattern_name}\n({pattern_type})\nConf: {confidence:.2f}',
                           xy=(trough_date, trough_price),
                           xytext=(10, -30), textcoords='offset points',
                           bbox=dict(boxstyle='round,pad=0.5',
                                   facecolor='red' if pattern_type == 'bearish' else 'green',
                                   alpha=0.3),
                           arrowprops=dict(arrowstyle='->',
                                         connectionstyle='arc3,rad=0'),
                           fontsize=9)
        
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_ylabel('Price', fontsize=12)
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3)
        
        # Format x-axis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        plt.tight_layout()
        return fig
    
    def plot_support_resistance(self, window: int = 20, num_levels: int = 3) -> plt.Figure:
        """
        Plot support and resistance levels
        
        Args:
            window: Window for calculating levels
            num_levels: Number of support/resistance levels to show
        
        Returns:
            matplotlib Figure object
        """
        fig, ax = plt.subplots(figsize=(14, 8))
        
        # Plot price
        ax.plot(self.data.index, self.close, label='Close Price', linewidth=2, color='blue')
        
        # Calculate pivot points (recent high and low)
        recent_data = self.data.tail(window)
        recent_high = recent_data['High'].max()
        recent_low = recent_data['Low'].min()
        
        # Calculate support and resistance levels
        pivot = (recent_high + recent_low + self.close.iloc[-1]) / 3
        
        resistance_levels = []
        support_levels = []
        
        for i in range(1, num_levels + 1):
            r = pivot + i * (recent_high - recent_low) / num_levels
            s = pivot - i * (recent_high - recent_low) / num_levels
            resistance_levels.append(r)
            support_levels.append(s)
        
        # Plot resistance levels
        for i, level in enumerate(resistance_levels):
            ax.axhline(level, color='red', linestyle='--', alpha=0.5, 
                      label=f'Resistance {i+1}' if i == 0 else '')
            ax.text(self.data.index[-1], level, f'R{i+1}', 
                   verticalalignment='bottom', horizontalalignment='right',
                   fontsize=9, color='red')
        
        # Plot support levels
        for i, level in enumerate(support_levels):
            ax.axhline(level, color='green', linestyle='--', alpha=0.5,
                      label=f'Support {i+1}' if i == 0 else '')
            ax.text(self.data.index[-1], level, f'S{i+1}',
                   verticalalignment='top', horizontalalignment='right',
                   fontsize=9, color='green')
        
        ax.set_title('Support and Resistance Levels', fontsize=14, fontweight='bold')
        ax.set_ylabel('Price', fontsize=12)
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3)
        
        # Format x-axis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        plt.tight_layout()
        return fig
    
    def plot_correlation_heatmap(self, data_dict: Dict[str, pd.DataFrame], title: str = "Stock Correlation") -> plt.Figure:
        """
        Plot correlation heatmap for multiple stocks
        
        Args:
            data_dict: Dictionary of stock data (symbol: DataFrame)
            title: Chart title
        
        Returns:
            matplotlib Figure object
        """
        # Calculate returns
        returns_df = pd.DataFrame()
        for symbol, data in data_dict.items():
            returns_df[symbol] = data['Close'].pct_change().dropna()
        
        # Calculate correlation
        correlation = returns_df.corr()
        
        # Plot heatmap
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(correlation, annot=True, cmap='coolwarm', center=0,
                   square=True, linewidths=1, cbar_kws={"shrink": 0.8},
                   fmt='.2f', ax=ax)
        
        ax.set_title(title, fontsize=14, fontweight='bold')
        plt.tight_layout()
        
        return fig
    
    def save_chart(self, fig: plt.Figure, filename: str, dpi: int = 300):
        """
        Save chart to file
        
        Args:
            fig: matplotlib Figure object
            filename: Output filename
            dpi: Resolution in dots per inch
        """
        fig.savefig(filename, dpi=dpi, bbox_inches='tight')
        print(f"Chart saved to {filename}")
        plt.close(fig)
