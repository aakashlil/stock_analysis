"""
Main Stock Analysis Script
Orchestrates data fetching, technical analysis, and visualization
"""

import sys
import os
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

# Import project modules
from scripts.data_fetcher import DataFetcher
from scripts.technical_analysis import TechnicalAnalyzer
from scripts.visualization import StockVisualizer
from scripts.news_scraper import NewsScraper


def analyze_stock(symbol: str, source: str = "yahoo", period: str = "1y", 
                  save_charts: bool = True, output_dir: str = "results"):
    """
    Perform complete stock analysis
    
    Args:
        symbol: Stock symbol (e.g., 'RELIANCE.NS', 'AAPL')
        source: Data source ('yahoo', 'alpha_vantage', 'finnhub')
        period: Time period for data
        save_charts: Whether to save charts to files
        output_dir: Directory to save results
    """
    print(f"\n{'='*60}")
    print(f"Stock Analysis for {symbol}")
    print(f"{'='*60}\n")
    
    # Create output directory if it doesn't exist
    if save_charts and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Step 1: Fetch Data
    print("Step 1: Fetching stock data...")
    fetcher = DataFetcher()
    data = fetcher.fetch_stock_data(symbol, source=source, period=period)
    
    if data.empty:
        print(f"Error: Could not fetch data for {symbol}")
        return None
    
    print(f"✓ Fetched {len(data)} data points")
    print(f"  Date range: {data.index[0].date()} to {data.index[-1].date()}")
    print(f"  Current price: {data['Close'].iloc[-1]:.2f}")
    print(f"  Price range: {data['Low'].min():.2f} - {data['High'].max():.2f}\n")
    
    # Step 2: Technical Analysis
    print("Step 2: Performing technical analysis...")
    analyzer = TechnicalAnalyzer(data)
    
    # Calculate indicators
    indicators = analyzer.calculate_all_indicators()
    print("✓ Calculated technical indicators:")
    print(f"  - RSI (14): {indicators['rsi'].iloc[-1]:.2f}")
    print(f"  - SMA 20: {indicators['sma_20'].iloc[-1]:.2f}")
    print(f"  - SMA 50: {indicators['sma_50'].iloc[-1]:.2f}")
    print(f"  - SMA 200: {indicators['sma_200'].iloc[-1]:.2f}")
    print(f"  - Stochastic %K: {indicators['stochastic']['k'].iloc[-1]:.2f}")
    print(f"  - Stochastic %D: {indicators['stochastic']['d'].iloc[-1]:.2f}")
    print(f"  - ATR: {indicators['atr'].iloc[-1]:.2f}")
    print(f"  - ADX: {indicators['adx']['adx'].iloc[-1]:.2f}")
    print(f"  - +DI: {indicators['adx']['plus_di'].iloc[-1]:.2f}")
    print(f"  - -DI: {indicators['adx']['minus_di'].iloc[-1]:.2f}")
    print(f"  - MACD RSI Signal: {indicators['macd_rsi']['macd_rsi_signal'].iloc[-1]}")
    
    # Detect patterns
    patterns = analyzer.detect_patterns()
    print(f"\n✓ Detected {len(patterns)} chart patterns:")
    for pattern in patterns:
        print(f"  - {pattern['pattern']} ({pattern['type']}) - Confidence: {pattern['confidence']:.2f}")
    
    # Generate signals
    signals = analyzer.generate_signals()
    print(f"\n✓ Trading Signals:")
    print(f"  - Overall: {signals['overall']}")
    print(f"  - RSI: {signals['rsi']}")
    print(f"  - MACD: {signals['macd']}")
    print(f"  - Patterns: {signals['patterns']}\n")
    
    # Calculate entry/exit levels
    entry_exit = analyzer.calculate_entry_exit_levels()
    print(f"✓ Entry & Exit Levels:")
    print(f"  - Entry Price: ${entry_exit['entry']:.2f}")
    print(f"  - Stop Loss: ${entry_exit['stop_loss']:.2f}")
    print(f"  - Take Profit: ${entry_exit['take_profit']:.2f}")
    print(f"  - Target 1: ${entry_exit['target1']:.2f}")
    print(f"  - Target 2: ${entry_exit['target2']:.2f}")
    print(f"  - Target 3: ${entry_exit['target3']:.2f}")
    print(f"  - Support Level: ${entry_exit['support']:.2f}")
    print(f"  - Resistance Level: ${entry_exit['resistance']:.2f}")
    print(f"  - Risk: ${entry_exit['risk']:.2f}")
    print(f"  - Reward: ${entry_exit['reward']:.2f}")
    print(f"  - Risk/Reward Ratio: {entry_exit['risk_reward_ratio']:.2f}\n")
    
    # Step 3: Fetch Latest News
    print("Step 3: Fetching latest news...")
    news_scraper = NewsScraper()
    news_items = news_scraper.fetch_all_news(symbol, sources=['yahoo', 'google'], limit=5)
    
    if news_items:
        print(f"✓ Found {len(news_items)} news items")
        news_scraper.display_news(news_items)
        
        # Fetch and analyze full articles
        print(f"\n{'='*60}")
        print("Fetching and Analyzing Full Articles")
        print(f"{'='*60}\n")
        analyzed_articles = news_scraper.analyze_full_articles(news_items, max_articles=3)
        
        if analyzed_articles:
            print(f"✓ Analyzed {len(analyzed_articles)} articles\n")
            for i, article in enumerate(analyzed_articles, 1):
                print(f"{i}. {article['title']}")
                print(f"   Source: {article['source']}")
                print(f"   Date: {article['date']}")
                print(f"   Summary: {article['summary']}")
                print()
        
        # Generate and display news summary
        print(f"{'='*60}")
        print("News Analysis Summary")
        print(f"{'='*60}\n")
        news_summary = news_scraper.generate_news_summary(news_items)
        print(f"Summary: {news_summary['summary']}")
        print(f"Sentiment: {news_summary['sentiment'].upper()}")
        print(f"Key Themes: {', '.join(news_summary['key_themes']) if news_summary['key_themes'] else 'None identified'}")
        
        # Display key events
        key_events = news_summary['key_events']
        events_found = False
        for event_type, event_list in key_events.items():
            if event_list:
                events_found = True
                print(f"\n{event_type.replace('_', ' ').title()}:")
                for event in event_list[:3]:  # Show up to 3 events per category
                    if isinstance(event, dict):
                        print(f"  • {event['title']}")
                        print(f"    Date: {event['date']}")
                        print(f"    Source: {event['source']}")
                    else:
                        print(f"  • {event}")
        
        if not events_found:
            print("\nNo specific key events detected in recent news.")
        
        print(f"\nConclusion: {news_summary['conclusion']}\n")
        
        # Compare with other mentioned stocks
        print(f"{'='*60}")
        print("Stock Comparison with Mentioned Peers")
        print(f"{'='*60}\n")
        stock_comparison = news_scraper.compare_mentioned_stocks(symbol, news_items, max_stocks=5)
        print(stock_comparison['comparison'])
        print()
        
        # Compare sentiment across stocks
        print(f"{'='*60}")
        print("Sentiment Comparison Across Stocks")
        print(f"{'='*60}\n")
        mentioned_symbols = [s['symbol'] for s in stock_comparison['mentioned_stocks'] if s['symbol'] != 'N/A']
        if mentioned_symbols:
            sentiment_comparison = news_scraper.compare_sentiment_across_stocks(symbol, mentioned_symbols)
            print(sentiment_comparison['comparison'])
            print()
        else:
            print("No valid stock symbols found for sentiment comparison.\n")
    else:
        print("✓ No news items found or unable to fetch news\n")
    
    # Step 4: Visualization
    print("Step 4: Creating visualizations...")
    visualizer = StockVisualizer(data)
    
    # Create price chart
    fig1 = visualizer.plot_price_chart(title=f"{symbol} Price Chart")
    if save_charts:
        visualizer.save_chart(fig1, f"{output_dir}/{symbol}_price_chart.png")
    else:
        plt.show()
    
    # Create candlestick chart
    fig2 = visualizer.plot_candlestick(title=f"{symbol} Candlestick Chart")
    if save_charts:
        visualizer.save_chart(fig2, f"{output_dir}/{symbol}_candlestick.png")
    else:
        plt.show()
    
    # Create technical indicators chart
    fig3 = visualizer.plot_technical_indicators(indicators)
    if save_charts:
        visualizer.save_chart(fig3, f"{output_dir}/{symbol}_indicators.png")
    else:
        plt.show()
    
    # Create pattern chart if patterns detected
    if patterns:
        fig4 = visualizer.plot_patterns(patterns, title=f"{symbol} Chart Patterns")
        if save_charts:
            visualizer.save_chart(fig4, f"{output_dir}/{symbol}_patterns.png")
        else:
            plt.show()
    
    # Create support/resistance chart
    fig5 = visualizer.plot_support_resistance()
    if save_charts:
        visualizer.save_chart(fig5, f"{output_dir}/{symbol}_support_resistance.png")
    else:
        plt.show()
    
    print("✓ Visualizations created\n")
    
    # Step 4: Save data
    if save_charts:
        data.to_csv(f"{output_dir}/{symbol}_data.csv")
        print(f"✓ Data saved to {output_dir}/{symbol}_data.csv\n")
    
    # Return analysis results
    return {
        'data': data,
        'indicators': indicators,
        'patterns': patterns,
        'signals': signals
    }


def compare_stocks(symbols: list, source: str = "yahoo", period: str = "1y",
                   save_charts: bool = True, output_dir: str = "results"):
    """
    Compare multiple stocks
    
    Args:
        symbols: List of stock symbols
        source: Data source
        period: Time period
        save_charts: Whether to save charts
        output_dir: Output directory
    """
    print(f"\n{'='*60}")
    print(f"Comparing {len(symbols)} stocks")
    print(f"{'='*60}\n")
    
    # Create output directory if it doesn't exist
    if save_charts and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Fetch data for all stocks
    fetcher = DataFetcher()
    data_dict = {}
    
    print("Fetching data for all stocks...")
    for symbol in symbols:
        print(f"  Fetching {symbol}...")
        data = fetcher.fetch_stock_data(symbol, source=source, period=period)
        if not data.empty:
            data_dict[symbol] = data
            print(f"    ✓ Fetched {len(data)} data points")
        else:
            print(f"    ✗ Failed to fetch data")
    
    if not data_dict:
        print("Error: Could not fetch data for any stock")
        return None
    
    print(f"\n✓ Successfully fetched data for {len(data_dict)} stocks\n")
    
    # Create correlation heatmap
    print("Creating correlation heatmap...")
    visualizer = StockVisualizer(list(data_dict.values())[0])
    fig = visualizer.plot_correlation_heatmap(data_dict, title="Stock Correlation Matrix")
    
    if save_charts:
        visualizer.save_chart(fig, f"{output_dir}/correlation_heatmap.png")
    else:
        plt.show()
    
    print("✓ Correlation heatmap created\n")
    
    # Calculate and display returns
    print("Returns Summary:")
    returns_summary = pd.DataFrame()
    for symbol, data in data_dict.items():
        returns = data['Close'].pct_change().dropna()
        total_return = (data['Close'].iloc[-1] / data['Close'].iloc[0] - 1) * 100
        volatility = returns.std() * 100
        
        returns_summary[symbol] = [
            total_return,
            volatility,
            data['Close'].iloc[-1]
        ]
    
    returns_summary.index = ['Total Return (%)', 'Volatility (%)', 'Current Price']
    print(returns_summary.round(2))
    
    if save_charts:
        returns_summary.to_csv(f"{output_dir}/returns_summary.csv")
        print(f"\n✓ Returns summary saved to {output_dir}/returns_summary.csv\n")
    
    return data_dict


def main():
    """Main function with example usage"""
    print("\n" + "="*60)
    print("Stock Analysis Tool")
    print("="*60)
    
    # Example 1: Analyze a single stock
    print("\nExample 1: Analyzing RELIANCE.NS (Reliance Industries)")
    analyze_stock("RELIANCE.NS", source="yahoo", period="1y", save_charts=True)
    
    # Example 2: Compare multiple stocks
    print("\n" + "="*60)
    print("\nExample 2: Comparing multiple Indian stocks")
    symbols = ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS"]
    compare_stocks(symbols, source="yahoo", period="1y", save_charts=True)
    
    print("\n" + "="*60)
    print("Analysis complete!")
    print("="*60 + "\n")


if __name__ == "__main__":
    # Check if command line arguments are provided
    if len(sys.argv) > 1:
        symbol = sys.argv[1]
        source = sys.argv[2] if len(sys.argv) > 2 else "yahoo"
        period = sys.argv[3] if len(sys.argv) > 3 else "1y"
        
        analyze_stock(symbol, source=source, period=period, save_charts=True)
    else:
        # Run examples
        main()
