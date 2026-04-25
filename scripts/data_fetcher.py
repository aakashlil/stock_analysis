"""
Data Fetcher Module
Supports multiple data sources: Alpha Vantage, Finnhub, Yahoo Finance, Google Finance
"""

import yfinance as yf
import requests
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config


class DataFetcher:
    """Base class for fetching stock data from various sources"""
    
    def __init__(self):
        self.alpha_vantage_key = config.ALPHA_VANTAGE_API_KEY
        self.finnhub_key = config.FINNHUB_API_KEY
    
    def fetch_yahoo_finance(self, symbol: str, period: str = "1y") -> pd.DataFrame:
        """
        Fetch data from Yahoo Finance using yfinance
        
        Args:
            symbol: Stock symbol (e.g., 'RELIANCE.NS' for NSE, 'AAPL' for US)
            period: Time period ('1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max')
        
        Returns:
            DataFrame with OHLCV data
        """
        try:
            stock = yf.Ticker(symbol)
            data = stock.history(period=period)
            return data
        except Exception as e:
            print(f"Error fetching from Yahoo Finance: {e}")
            return pd.DataFrame()
    
    def fetch_alpha_vantage(self, symbol: str, function: str = "TIME_SERIES_DAILY") -> pd.DataFrame:
        """
        Fetch data from Alpha Vantage API
        
        Args:
            symbol: Stock symbol
            function: API function (TIME_SERIES_DAILY, TIME_SERIES_INTRADAY, etc.)
        
        Returns:
            DataFrame with OHLCV data
        """
        if self.alpha_vantage_key == "YOUR_ALPHA_VANTAGE_KEY":
            print("Please set your Alpha Vantage API key in config.py")
            return pd.DataFrame()
        
        base_url = "https://www.alphavantage.co/query"
        params = {
            "function": function,
            "symbol": symbol,
            "apikey": self.alpha_vantage_key,
            "outputsize": "full"
        }
        
        try:
            response = requests.get(base_url, params=params)
            data = response.json()
            
            # Parse the response based on function type
            if function == "TIME_SERIES_DAILY":
                time_series = data.get("Time Series (Daily)", {})
            elif function == "TIME_SERIES_INTRADAY":
                time_series = data.get(f"Time Series ({config.DEFAULT_INTERVAL})", {})
            else:
                time_series = {}
            
            if not time_series:
                print(f"No data received from Alpha Vantage for {symbol}")
                return pd.DataFrame()
            
            # Convert to DataFrame
            df = pd.DataFrame.from_dict(time_series, orient='index')
            df.index = pd.to_datetime(df.index)
            df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
            df = df.astype(float)
            df = df.sort_index()
            
            return df
        except Exception as e:
            print(f"Error fetching from Alpha Vantage: {e}")
            return pd.DataFrame()
    
    def fetch_finnhub(self, symbol: str, resolution: str = "D", from_date: Optional[str] = None, to_date: Optional[str] = None) -> pd.DataFrame:
        """
        Fetch data from Finnhub API
        
        Args:
            symbol: Stock symbol
            resolution: Resolution (1, 5, 15, 30, 60, D, W, M)
            from_date: From date (YYYY-MM-DD)
            to_date: To date (YYYY-MM-DD)
        
        Returns:
            DataFrame with OHLCV data
        """
        if self.finnhub_key == "YOUR_FINNHUB_KEY":
            print("Please set your Finnhub API key in config.py")
            return pd.DataFrame()
        
        if not from_date:
            from_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
        if not to_date:
            to_date = datetime.now().strftime("%Y-%m-%d")
        
        base_url = "https://finnhub.io/api/v1/stock/candle"
        params = {
            "symbol": symbol,
            "resolution": resolution,
            "from": from_date,
            "to": to_date,
            "token": self.finnhub_key
        }
        
        try:
            response = requests.get(base_url, params=params)
            data = response.json()
            
            if data.get('s') == 'no_data':
                print(f"No data received from Finnhub for {symbol}")
                return pd.DataFrame()
            
            df = pd.DataFrame({
                'Open': data['o'],
                'High': data['h'],
                'Low': data['l'],
                'Close': data['c'],
                'Volume': data['v']
            })
            df.index = pd.to_datetime(data['t'], unit='s')
            df = df.sort_index()
            
            return df
        except Exception as e:
            print(f"Error fetching from Finnhub: {e}")
            return pd.DataFrame()
    
    def fetch_stock_data(self, symbol: str, source: str = "yahoo", **kwargs) -> pd.DataFrame:
        """
        Main method to fetch stock data from specified source
        
        Args:
            symbol: Stock symbol
            source: Data source ('yahoo', 'alpha_vantage', 'finnhub')
            **kwargs: Additional parameters for specific sources
        
        Returns:
            DataFrame with OHLCV data
        """
        if source == "yahoo":
            return self.fetch_yahoo_finance(symbol, **kwargs)
        elif source == "alpha_vantage":
            return self.fetch_alpha_vantage(symbol, **kwargs)
        elif source == "finnhub":
            return self.fetch_finnhub(symbol, **kwargs)
        else:
            print(f"Unknown source: {source}")
            return pd.DataFrame()


# Convenience function
def get_stock_data(symbol: str, source: str = "yahoo", **kwargs) -> pd.DataFrame:
    """Convenience function to fetch stock data"""
    fetcher = DataFetcher()
    return fetcher.fetch_stock_data(symbol, source, **kwargs)
