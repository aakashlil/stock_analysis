# Stock Analysis Prompt Template

This file contains prompt templates for AI-assisted stock analysis using this project.

## Technical Indicators Reference

### RSI (Relative Strength Index)
- **Significance**: Leading indicator that measures the speed and magnitude of price changes
- **Range**: 0-100
- **Interpretation**:
  - Below 20: Oversold condition (potential buy signal)
  - Above 80: Overbought condition (potential sell signal)
  - 50: Neutral zone
- **Usage**: Identifies overbought/oversold conditions and potential reversals

### MACD (Moving Average Convergence Divergence)
- **Significance**: Momentum-based indicator for trend direction and strength
- **Components**: MACD line, Signal line, Histogram
- **Interpretation**:
  - MACD above Signal: Bullish momentum
  - MACD below Signal: Bearish momentum
  - Histogram expansion: Increasing momentum
  - Histogram contraction: Decreasing momentum
- **Usage**: Identifies trend direction, momentum shifts, and optimal entry/exit points

### Bollinger Bands
- **Significance**: Volatility-based indicator using moving average and standard deviation
- **Components**: Upper band, Middle band (SMA), Lower band
- **Interpretation**:
  - Price near upper band: Overbought
  - Price near lower band: Oversold
  - Band squeeze: Low volatility (potential breakout)
  - Band expansion: High volatility
- **Usage**: Analyzes price volatility and identifies overbought/oversold conditions

### Stochastic Oscillator
- **Significance**: Predicts potential market tops and bottoms by comparing closing price to high-low range
- **Components**: %K line, %D line
- **Range**: 0-100
- **Interpretation**:
  - Above 80: Overbought (potential reversal)
  - Below 20: Oversold (potential reversal)
  - %K crosses above %D: Buy signal
  - %K crosses below %D: Sell signal
- **Usage**: Identifies potential market tops and bottoms in advance

### Ichimoku Cloud
- **Significance**: Comprehensive leading indicator for support/resistance and trend direction
- **Components**: Tenkan-sen, Kijun-sen, Senkou Span A, Senkou Span B, Chikou Span
- **Interpretation**:
  - Price above cloud: Bullish trend
  - Price below cloud: Bearish trend
  - Cloud acts as dynamic support/resistance
  - Tenkan-sen above Kijun-sen: Short-term bullish
- **Usage**: Provides complete picture of trend, support/resistance, and momentum

### ATR (Average True Range)
- **Significance**: Measures trend strength and volatility
- **Range**: 0 to infinity
- **Interpretation**:
  - High ATR: High volatility
  - Low ATR: Low volatility
  - Rising ATR: Increasing volatility
  - Falling ATR: Decreasing volatility
- **Usage**: Ideal for trend-following strategies and position sizing

### ADX (Average Directional Index)
- **Significance**: Measures trend strength regardless of direction
- **Range**: 0-100
- **Components**: ADX line, +DI (Positive Directional Indicator), -DI (Negative Directional Indicator)
- **Interpretation**:
  - ADX below 20: Weak trend or ranging market
  - ADX above 25: Strong trend
  - ADX above 40: Very strong trend
  - +DI above -DI: Bullish trend
  - -DI above +DI: Bearish trend
- **Usage**: Ideal for enhancing trend-following strategies and determining trend strength

### MACD RSI
- **Significance**: Combines MACD momentum with RSI overbought/oversold detection
- **Components**: RSI, MACD line, Signal line, Histogram, Combined signal
- **Interpretation**:
  - Buy signal: MACD histogram positive AND RSI not overbought (<70)
  - Sell signal: MACD histogram negative AND RSI not oversold (>30)
  - Divergence: Price and indicator moving in opposite directions
- **Usage**: Identifies overbought/oversold zones, detects divergences, generates accurate entry/exit signals

### Moving Averages (SMA/EMA)
- **Significance**: Trend identification and support/resistance levels
- **Types**: Simple Moving Average (SMA), Exponential Moving Average (EMA)
- **Common Periods**: 20 (short-term), 50 (medium-term), 200 (long-term)
- **Interpretation**:
  - Price above MA: Bullish
  - Price below MA: Bearish
  - MA crossover: Trend change signal
  - EMA reacts faster than SMA
- **Usage**: Identifies trend direction and potential support/resistance levels

## Setup Instructions

Before using this project, set up the Python environment:

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

## Quick Start

```bash
# Activate virtual environment (if not already activated)
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Run analysis
python main.py <SYMBOL>
```

## Basic Stock Analysis Prompt

```
You are a professional stock market analyst. Analyze the following stock data and provide comprehensive insights:

Stock Symbol: {symbol}
Data Period: {period}
Current Price: {current_price}
Price Range: {low_price} - {high_price}

Technical Indicators:
- RSI (14): {rsi_value}
- SMA 20: {sma_20}
- SMA 50: {sma_50}
- SMA 200: {sma_200}
- MACD Signal: {macd_signal}
- Stochastic %K: {stochastic_k}
- Stochastic %D: {stochastic_d}
- ATR: {atr_value}
- ADX: {adx_value}
- +DI: {plus_di}
- -DI: {minus_di}
- MACD RSI Signal: {macd_rsi_signal}

Detected Chart Patterns:
{patterns_list}

Trading Signals:
- Overall: {overall_signal}
- RSI: {rsi_signal}
- MACD: {macd_signal}
- Patterns: {pattern_signal}

Entry & Exit Levels:
- Entry Price: {entry_price}
- Stop Loss: {stop_loss}
- Take Profit: {take_profit}
- Risk/Reward Ratio: {risk_reward_ratio}

Please provide:
1. Technical analysis summary
2. Key support and resistance levels
3. Trend analysis (short-term, medium-term, long-term)
4. Risk assessment
5. Potential entry/exit points
6. Overall recommendation (Buy/Sell/Hold) with confidence level
```

## Multi-Stock Comparison Prompt

```
Compare the following stocks based on their recent performance:

Stocks: {symbols_list}
Analysis Period: {period}

Performance Metrics:
{returns_summary}

Correlation Matrix:
{correlation_data}

Please provide:
1. Relative strength analysis
2. Best performer identification
3. Risk-adjusted returns comparison
4. Diversification recommendations
5. Portfolio allocation suggestions
```

## Pattern Analysis Prompt

```
Analyze the detected chart patterns for {symbol}:

Patterns Detected:
{patterns_with_details}

For each pattern, provide:
1. Pattern validity assessment
2. Expected price targets
3. Timeframe for pattern completion
4. Failure probability
5. Confirmation signals to watch for
6. Risk management recommendations
```

## Risk Assessment Prompt

```
Perform a comprehensive risk assessment for {symbol}:

Current Market Data:
{market_data}

Technical Indicators:
{indicators}

Volatility Metrics:
- ATR: {atr_value}
- Price Volatility: {volatility_value}

Please assess:
1. Market risk (systematic)
2. Stock-specific risk (unsystematic)
3. Liquidity risk
4. Volatility risk
5. Recommended position sizing
6. Stop-loss levels
7. Risk-reward ratio for current setup
```

## Trading Strategy Prompt

```
Develop a trading strategy for {symbol} based on the following analysis:

Technical Analysis:
{technical_summary}

Pattern Analysis:
{pattern_summary}

Market Conditions:
{market_conditions}

Strategy Requirements:
- Timeframe: {timeframe}
- Risk tolerance: {risk_tolerance}
- Capital available: {capital}

Provide:
1. Entry strategy (price, conditions, confirmation)
2. Exit strategy (take profit, stop loss)
3. Position sizing recommendation
4. Trade management rules
5. Contingency plans
6. Performance metrics to track
```

## Custom Analysis Prompts

### Fundamental Analysis Integration
```
Combine technical analysis with fundamental data for {symbol}:

Technical Data:
{technical_data}

Fundamental Data:
- P/E Ratio: {pe_ratio}
- EPS: {eps}
- Market Cap: {market_cap}
- Dividend Yield: {dividend_yield}
- Debt-to-Equity: {de_ratio}

Provide integrated analysis considering both technical and fundamental factors.
```

### Sector Analysis
```
Analyze {symbol} in the context of its sector:

Sector: {sector}
Sector Performance: {sector_performance}
Peer Comparison: {peer_data}

Assess:
1. Relative sector strength
2. Sector rotation opportunities
3. Peer group ranking
4. Sector-specific risks
```

### Comprehensive Stock Analysis with News
```
Perform comprehensive analysis for {symbol} including technical indicators, news analysis, peer comparison, and event detection:

STOCK DATA:
- Symbol: {symbol}
- Current Price: {current_price}
- Price Range: {low_price} - {high_price}
- Data Period: {period}

TECHNICAL INDICATORS:
- RSI (14): {rsi_value}
- SMA 20: {sma_20}
- SMA 50: {sma_50}
- SMA 200: {sma_200}
- Stochastic %K: {stochastic_k}
- Stochastic %D: {stochastic_d}
- ATR: {atr_value}
- ADX: {adx_value}
- +DI: {plus_di}
- -DI: {minus_di}
- MACD RSI Signal: {macd_rsi_signal}

CHART PATTERNS:
{patterns_list}

TRADING SIGNALS:
- Overall: {overall_signal}
- RSI: {rsi_signal}
- MACD: {macd_signal}
- Patterns: {pattern_signal}

ENTRY & EXIT LEVELS:
- Entry Price: {entry_price}
- Stop Loss: {stop_loss}
- Take Profit: {take_profit}
- Risk/Reward Ratio: {risk_reward_ratio}

NEWS ANALYSIS:
- Total Articles Analyzed: {news_count}
- Overall Sentiment: {news_sentiment}
- Key Themes: {key_themes}

KEY EVENTS DETECTED:
{key_events}

FULL ARTICLE ANALYSIS:
{article_summaries}

PEER STOCK COMPARISON:
{peer_comparison}

SENTIMENT COMPARISON:
{sentiment_comparison}

Please provide:
1. Technical analysis summary and trend direction
2. News sentiment analysis and key themes
3. Major events/launches detected and their impact
4. Peer comparison and relative performance
5. Cross-stock sentiment analysis
6. Risk assessment based on technical and news factors
7. Investment recommendation (Buy/Sell/Hold) with confidence level
8. Key catalysts to watch for
9. Price targets and timeframes
10. Overall conclusion integrating all factors
```

### News Analysis
```
Analyze the latest news for {symbol} and its potential impact:

Recent News Headlines:
{news_headlines}

News Sources:
{news_sources}

Publication Dates:
{news_dates}

Please provide:
1. Sentiment analysis (positive/negative/neutral)
2. Key themes and topics
3. Potential price impact
4. Timeline for expected effects
5. Risk factors mentioned
6. Opportunities highlighted
7. Overall news-driven outlook
8. Recommended actions based on news
```

### Volatility Analysis
```
Perform comprehensive volatility analysis for {symbol}:

Current Volatility Metrics:
- ATR: {atr_value}
- Historical Volatility: {hist_vol}
- Implied Volatility: {impl_vol}
- VIX Correlation: {vix_corr}

Volatility Regime:
{volatility_regime}

Please assess:
1. Current volatility level (low/medium/high)
2. Volatility trend (increasing/decreasing/stable)
3. Expected volatility range
4. Options pricing implications
5. Position sizing recommendations
6. Stop-loss placement strategies
7. Profit-taking opportunities
8. Risk management adjustments
```

### Earnings Analysis
```
Analyze earnings data for {symbol}:

Recent Earnings:
- EPS: {eps_actual} vs {eps_estimate}
- Revenue: {revenue_actual} vs {revenue_estimate}
- Guidance: {guidance}

Historical Earnings Performance:
{earnings_history}

Please provide:
1. Earnings surprise analysis
2. Revenue growth trends
3. Margin analysis
4. Guidance implications
5. Historical post-earnings price reaction
6. Expected future performance
7. Investment recommendation based on earnings
```

### Dividend Analysis
```
Analyze dividend information for {symbol}:

Current Dividend Metrics:
- Dividend Yield: {div_yield}
- Payout Ratio: {payout_ratio}
- Dividend Growth Rate: {div_growth}
- Ex-Dividend Date: {ex_div_date}

Dividend History:
{dividend_history}

Please assess:
1. Dividend sustainability
2. Yield attractiveness vs peers
3. Growth potential
4. Income vs total return trade-off
5. Reinvestment opportunities
6. Tax implications
7. Suitability for income investors
```

## Usage Instructions

1. Replace placeholders (e.g., {symbol}, {period}) with actual values
2. Use these prompts with AI assistants or LLMs for enhanced analysis
3. Combine with the project's data fetching and analysis modules
4. Customize prompts based on your specific analysis needs

## Integration with Project

These prompts can be automated by modifying the `main.py` script to:
- Extract data from analysis results
- Populate prompt templates
- Send to AI APIs (OpenAI, Anthropic, etc.)
- Store AI-generated insights in results directory

Example integration:
```python
def generate_ai_analysis(symbol: str, analysis_results: dict):
    prompt = load_prompt_template("basic_analysis")
    filled_prompt = prompt.format(
        symbol=symbol,
        current_price=analysis_results['data']['Close'].iloc[-1],
        rsi_value=analysis_results['indicators']['rsi'].iloc[-1],
        # ... more fields
    )
    return send_to_ai_api(filled_prompt)
```
