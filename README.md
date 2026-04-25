# Stock Analysis Project

A comprehensive Python-based stock analysis tool that fetches market data from multiple sources, performs technical analysis with chart pattern detection, and generates professional visualizations.

## Features

- **Multiple Data Sources**: Support for Yahoo Finance, Alpha Vantage, Finnhub APIs
- **Technical Indicators**: RSI, MACD, Bollinger Bands, Moving Averages (SMA/EMA), ATR, Stochastic Oscillator, Ichimoku Cloud, ADX, MACD RSI
- **Chart Pattern Detection**: Head and Shoulders, Double Top/Bottom, Triangles, Cup and Handle
- **Professional Visualizations**: Price charts, candlestick charts, technical indicator plots, pattern annotations
- **Stock Comparison**: Correlation analysis and multi-stock comparison
- **Trading Signals**: Automated buy/sell signal generation based on indicators and patterns
- **Entry/Exit Levels**: Calculated entry, stop loss, and take profit levels with risk-reward ratios
- **News Analysis**: Fetches latest news, performs sentiment analysis, detects key events (earnings, product launches), and compares with peer stocks

## Project Structure

```
stock_analysis/
├── config.py              # API keys and configuration settings
├── main.py                # Main analysis script
├── requirements.txt       # Python dependencies
├── scripts/
│   ├── data_fetcher.py    # Data fetching from multiple APIs
│   ├── technical_analysis.py  # Technical indicators and pattern detection
│   └── visualization.py   # Charting and visualization
├── data/                  # Raw data storage
├── notebooks/             # Jupyter notebooks for analysis
└── results/               # Generated charts and analysis results
```

## Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Install Dependencies

```bash
pip install -r requirements.txt
```

Required packages:
- pandas
- numpy
- matplotlib
- seaborn
- yfinance
- jupyter
- requests
- scipy

## Configuration

Before using the project, configure your API keys in `config.py`:

```python
# Alpha Vantage API Key
ALPHA_VANTAGE_API_KEY = "YOUR_ALPHA_VANTAGE_KEY"

# Finnhub API Key
FINNHUB_API_KEY = "YOUR_FINNHUB_KEY"

# Upstox API Credentials
UPSTOX_API_KEY = "YOUR_UPSTOX_API_KEY"
UPSTOX_API_SECRET = "YOUR_UPSTOX_API_SECRET"
UPSTOX_REDIRECT_URI = "YOUR_UPSTOX_REDIRECT_URI"
```

**Note**: Yahoo Finance works without API keys for basic usage.

## Usage

### Analyze a Single Stock

```bash
python main.py RELIANCE.NS yahoo 1y
```

Or run the main script with built-in examples:

```bash
python main.py
```

### Programmatic Usage

```python
from scripts.data_fetcher import DataFetcher
from scripts.technical_analysis import TechnicalAnalyzer
from scripts.visualization import StockVisualizer

# Fetch data
fetcher = DataFetcher()
data = fetcher.fetch_stock_data("RELIANCE.NS", source="yahoo", period="1y")

# Perform technical analysis
analyzer = TechnicalAnalyzer(data)
indicators = analyzer.calculate_all_indicators()
patterns = analyzer.detect_patterns()
signals = analyzer.generate_signals()
entry_exit = analyzer.calculate_entry_exit_levels()

# Create visualizations
visualizer = StockVisualizer(data)
fig = visualizer.plot_price_chart(title="RELIANCE.NS Analysis")
visualizer.save_chart(fig, "results/reliance_chart.png")
```

### Compare Multiple Stocks

```python
from main import compare_stocks

symbols = ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS"]
compare_stocks(symbols, source="yahoo", period="1y", save_charts=True)
```

## Technical Indicators

The project includes the following technical indicators:

- **RSI (Relative Strength Index)**: Measures overbought/oversold conditions
- **MACD (Moving Average Convergence Divergence)**: Momentum-based trend indicator
- **Bollinger Bands**: Volatility-based indicator
- **Stochastic Oscillator**: Predicts market tops/bottoms
- **Ichimoku Cloud**: Comprehensive indicator for support/resistance and trend direction
- **ADX (Average Directional Index)**: Measures trend strength
- **ATR (Average True Range)**: Measures volatility
- **MACD RSI**: Combined indicator for entry/exit signals
- **Moving Averages (SMA/EMA)**: Trend identification

## Output

Analysis results are saved to the `results/` directory:
- `{symbol}_price_chart.png` - Price chart with moving averages
- `{symbol}_candlestick.png` - Candlestick chart
- `{symbol}_indicators.png` - Technical indicators (RSI, MACD, Bollinger Bands)
- `{symbol}_patterns.png` - Chart pattern annotations
- `{symbol}_support_resistance.png` - Support and resistance levels
- `{symbol}_data.csv` - Raw OHLCV data
- `correlation_heatmap.png` - Multi-stock correlation matrix
- `returns_summary.csv` - Returns comparison for multiple stocks

## Examples

### Indian Stocks (NSE)
```python
# Reliance Industries
analyze_stock("RELIANCE.NS")

# Tata Consultancy Services
analyze_stock("TCS.NS")

# Infosys
analyze_stock("INFY.NS")

# HDFC Bank
analyze_stock("HDFCBANK.NS")
```

### US Stocks
```python
# Apple
analyze_stock("AAPL")

# Microsoft
analyze_stock("MSFT")

# Google
analyze_stock("GOOGL")

# Tesla
analyze_stock("TSLA")
```

## Notes

- For Indian stocks, use `.NS` suffix for NSE and `.BO` for BSE
- Yahoo Finance is recommended for free usage without API keys
- Alpha Vantage and Finnhub require API keys for full functionality
- Pattern detection requires sufficient historical data (minimum 20-30 data points)
- All charts are saved at 300 DPI for high-quality output

## License

This project is for educational and research purposes.

## Disclaimer

This tool is for educational purposes only. Stock market analysis involves risk. Always do your own research and consult with financial advisors before making investment decisions.