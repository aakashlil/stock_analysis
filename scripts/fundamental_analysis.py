"""
Fundamental Analysis Module
Fetches and analyzes earnings, revenue, growth estimates, valuation metrics,
and future outlook data using yfinance.
"""

import yfinance as yf
import pandas as pd
from typing import Dict, Any, Optional


class FundamentalAnalyzer:
    """Fetch and analyze fundamental data for stocks"""

    def __init__(self, symbol: str):
        self.symbol = symbol
        self.ticker = yf.Ticker(symbol)
        self._info = None

    @property
    def info(self) -> dict:
        if self._info is None:
            self._info = self.ticker.info
        return self._info

    def get_key_metrics(self) -> Dict[str, Any]:
        """Get key financial metrics from yfinance info."""
        i = self.info
        return {
            'market_cap': i.get('marketCap'),
            'enterprise_value': i.get('enterpriseValue'),
            'forward_pe': i.get('forwardPE'),
            'trailing_pe': i.get('trailingPE'),
            'peg_ratio': i.get('pegRatio'),
            'price_to_sales': i.get('priceToSalesTrailing12Months'),
            'price_to_book': i.get('priceToBook'),
            'revenue_ttm': i.get('totalRevenue'),
            'net_income': i.get('netIncomeToCommon'),
            'profit_margin': i.get('profitMargins'),
            'operating_margin': i.get('operatingMargins'),
            'gross_margin': i.get('grossMargins'),
            'roe': i.get('returnOnEquity'),
            'debt_to_equity': i.get('debtToEquity'),
            'free_cash_flow': i.get('freeCashflow'),
            'revenue_growth': i.get('revenueGrowth'),
            'earnings_growth': i.get('earningsGrowth'),
            'current_price': i.get('currentPrice') or i.get('regularMarketPrice'),
            'target_mean': i.get('targetMeanPrice'),
            'target_low': i.get('targetLowPrice'),
            'target_high': i.get('targetHighPrice'),
            'recommendation': i.get('recommendationKey'),
            'shares_outstanding': i.get('sharesOutstanding'),
            'sector': i.get('sector'),
            'industry': i.get('industry'),
            'short_name': i.get('shortName'),
        }

    def get_quarterly_financials(self) -> Dict[str, Optional[pd.Series]]:
        """Get quarterly revenue and net income."""
        fin = self.ticker.quarterly_financials
        result: Dict[str, Optional[pd.Series]] = {
            'revenue': None,
            'net_income': None,
            'gross_profit': None,
        }
        if fin is not None and not fin.empty:
            if 'Total Revenue' in fin.index:
                result['revenue'] = fin.loc['Total Revenue']
            if 'Net Income' in fin.index:
                result['net_income'] = fin.loc['Net Income']
            if 'Gross Profit' in fin.index:
                result['gross_profit'] = fin.loc['Gross Profit']
        return result

    def get_earnings_estimates(self) -> Dict[str, Optional[pd.DataFrame]]:
        """Get forward earnings and revenue estimates."""
        return {
            'earnings_estimate': _safe_df(self.ticker.earnings_estimate),
            'revenue_estimate': _safe_df(self.ticker.revenue_estimate),
            'eps_trend': _safe_df(self.ticker.eps_trend),
        }

    def get_valuation_analysis(self) -> Dict[str, Any]:
        """Compute valuation ratios and upside/downside from analyst targets."""
        metrics = self.get_key_metrics()
        price = metrics['current_price']
        target = metrics['target_mean']

        upside = None
        if price and target:
            upside = ((target - price) / price) * 100

        estimates = self.get_earnings_estimates()
        forward_eps_current_year = None
        forward_eps_next_year = None
        ee = estimates['earnings_estimate']
        if ee is not None and not ee.empty and 'avg' in ee.columns:
            if '0y' in ee.index:
                forward_eps_current_year = ee.loc['0y', 'avg']
            if '+1y' in ee.index:
                forward_eps_next_year = ee.loc['+1y', 'avg']

        pe_on_next_year = None
        if price and forward_eps_next_year and forward_eps_next_year > 0:
            pe_on_next_year = price / forward_eps_next_year

        return {
            'current_price': price,
            'analyst_target': target,
            'analyst_low': metrics['target_low'],
            'analyst_high': metrics['target_high'],
            'upside_to_target': upside,
            'forward_pe': metrics['forward_pe'],
            'trailing_pe': metrics['trailing_pe'],
            'peg_ratio': metrics['peg_ratio'],
            'eps_current_year': forward_eps_current_year,
            'eps_next_year': forward_eps_next_year,
            'pe_on_next_year': pe_on_next_year,
            'recommendation': metrics['recommendation'],
        }

    def get_growth_analysis(self) -> Dict[str, Any]:
        """Analyze earnings and revenue growth trajectory."""
        estimates = self.get_earnings_estimates()
        ee = estimates['earnings_estimate']
        re = estimates['revenue_estimate']
        et = estimates['eps_trend']

        result: Dict[str, Any] = {
            'revenue_growth_ttm': self.info.get('revenueGrowth'),
            'earnings_growth_ttm': self.info.get('earningsGrowth'),
        }

        if ee is not None and not ee.empty:
            for period in ['0q', '+1q', '0y', '+1y']:
                if period in ee.index:
                    row = ee.loc[period]
                    result[f'eps_{period}'] = {
                        'avg': row.get('avg'),
                        'low': row.get('low'),
                        'high': row.get('high'),
                        'growth': row.get('growth'),
                        'num_analysts': row.get('numberOfAnalysts'),
                    }

        if re is not None and not re.empty:
            for period in ['0q', '+1q', '0y', '+1y']:
                if period in re.index:
                    row = re.loc[period]
                    result[f'rev_{period}'] = {
                        'avg': row.get('avg'),
                        'low': row.get('low'),
                        'high': row.get('high'),
                        'growth': row.get('growth'),
                        'num_analysts': row.get('numberOfAnalysts'),
                    }

        if et is not None and not et.empty and 'current' in et.columns:
            result['eps_revisions'] = {}
            for period in ['0y', '+1y']:
                if period in et.index:
                    row = et.loc[period]
                    result['eps_revisions'][period] = {
                        'current': row.get('current'),
                        '7d_ago': row.get('7daysAgo'),
                        '30d_ago': row.get('30daysAgo'),
                        '90d_ago': row.get('90daysAgo'),
                    }

        return result

    def generate_full_report(self) -> Dict[str, Any]:
        """Generate a complete fundamental analysis report."""
        return {
            'symbol': self.symbol,
            'metrics': self.get_key_metrics(),
            'quarterly': self.get_quarterly_financials(),
            'estimates': self.get_earnings_estimates(),
            'valuation': self.get_valuation_analysis(),
            'growth': self.get_growth_analysis(),
        }

    def print_report(self) -> Dict[str, Any]:
        """Print a formatted fundamental analysis report and return data."""
        report = self.generate_full_report()
        m = report['metrics']
        v = report['valuation']
        g = report['growth']

        print(f"\n{'='*60}")
        print(f"Fundamental Analysis for {self.symbol}")
        print(f"{'='*60}\n")

        print(f"Company: {m.get('short_name', 'N/A')}")
        print(f"Sector: {m.get('sector', 'N/A')} | Industry: {m.get('industry', 'N/A')}")

        print(f"\n--- Key Metrics ---")
        print(f"  Market Cap: {_fmt_dollars(m['market_cap'])}")
        print(f"  Revenue (TTM): {_fmt_dollars(m['revenue_ttm'])}")
        print(f"  Net Income (TTM): {_fmt_dollars(m['net_income'])}")
        print(f"  Profit Margin: {_fmt_pct(m['profit_margin'])}")
        print(f"  Operating Margin: {_fmt_pct(m['operating_margin'])}")
        print(f"  Gross Margin: {_fmt_pct(m['gross_margin'])}")
        print(f"  ROE: {_fmt_pct(m['roe'])}")
        print(f"  Debt/Equity: {_fmt_val(m['debt_to_equity'])}")
        print(f"  Free Cash Flow: {_fmt_dollars(m['free_cash_flow'])}")
        print(f"  Revenue Growth (YoY): {_fmt_pct(m['revenue_growth'])}")
        print(f"  Earnings Growth (YoY): {_fmt_pct(m['earnings_growth'])}")

        print(f"\n--- Valuation ---")
        print(f"  Current Price: ${_fmt_val(v['current_price'])}")
        print(f"  Forward PE: {_fmt_val(v['forward_pe'])}")
        print(f"  Trailing PE: {_fmt_val(v['trailing_pe'])}")
        print(f"  PEG Ratio: {_fmt_val(v['peg_ratio'])}")
        print(f"  Price/Sales: {_fmt_val(m['price_to_sales'])}")
        print(f"  Price/Book: {_fmt_val(m['price_to_book'])}")

        print(f"\n--- Analyst Estimates ---")
        print(f"  Recommendation: {v['recommendation']}")
        print(f"  Target Mean: ${_fmt_val(v['analyst_target'])}")
        print(f"  Target Low: ${_fmt_val(v['analyst_low'])}")
        print(f"  Target High: ${_fmt_val(v['analyst_high'])}")
        print(f"  Upside to Target: {_fmt_pct_val(v['upside_to_target'])}")

        print(f"\n--- Forward Earnings ---")
        print(f"  EPS (Current Year): {_fmt_val(v['eps_current_year'])}")
        print(f"  EPS (Next Year): {_fmt_val(v['eps_next_year'])}")
        print(f"  PE on Next Year EPS: {_fmt_val(v['pe_on_next_year'])}")

        # Earnings estimates table
        ee = report['estimates']['earnings_estimate']
        if ee is not None and not ee.empty:
            print(f"\n--- Earnings Estimates Detail ---")
            for period in ['0q', '+1q', '0y', '+1y']:
                if period in ee.index:
                    row = ee.loc[period]
                    label = {'0q': 'Current Q', '+1q': 'Next Q', '0y': 'Current Year', '+1y': 'Next Year'}
                    print(f"  {label.get(period, period)}: EPS ${row.get('avg', 'N/A'):.2f} "
                          f"(Low ${row.get('low', 'N/A'):.2f}, High ${row.get('high', 'N/A'):.2f}) "
                          f"Growth: {_fmt_pct(row.get('growth'))} | {int(row.get('numberOfAnalysts', 0))} analysts")

        # Revenue estimates table
        re_est = report['estimates']['revenue_estimate']
        if re_est is not None and not re_est.empty:
            print(f"\n--- Revenue Estimates Detail ---")
            for period in ['0q', '+1q', '0y', '+1y']:
                if period in re_est.index:
                    row = re_est.loc[period]
                    label = {'0q': 'Current Q', '+1q': 'Next Q', '0y': 'Current Year', '+1y': 'Next Year'}
                    print(f"  {label.get(period, period)}: Rev {_fmt_dollars(row.get('avg'))} "
                          f"Growth: {_fmt_pct(row.get('growth'))} | {int(row.get('numberOfAnalysts', 0))} analysts")

        # EPS revision trend
        revisions = g.get('eps_revisions', {})
        if revisions:
            print(f"\n--- EPS Revision Trend (Analyst Upgrades/Downgrades) ---")
            for period, rev in revisions.items():
                label = {'0y': 'Current Year', '+1y': 'Next Year'}.get(period, period)
                current = rev.get('current')
                ago_90 = rev.get('90d_ago')
                if current and ago_90 and ago_90 != 0:
                    change = ((current - ago_90) / abs(ago_90)) * 100
                    direction = "↑" if change > 0 else "↓"
                    print(f"  {label}: ${ago_90:.2f} → ${current:.2f} ({direction}{abs(change):.1f}% in 90 days)")

        # Quarterly financials
        q = report['quarterly']
        if q['revenue'] is not None:
            print(f"\n--- Quarterly Revenue (Last 5) ---")
            rev = q['revenue'].dropna().head(5)
            for date, val in rev.items():
                print(f"  {date.strftime('%Y-%m-%d')}: {_fmt_dollars(val)}")

        if q['net_income'] is not None:
            print(f"\n--- Quarterly Net Income (Last 5) ---")
            ni = q['net_income'].dropna().head(5)
            for date, val in ni.items():
                profit_loss = "Profit" if val > 0 else "Loss"
                print(f"  {date.strftime('%Y-%m-%d')}: {_fmt_dollars(val)} ({profit_loss})")

        print(f"\n{'='*60}\n")
        return report


def _safe_df(df) -> Optional[pd.DataFrame]:
    """Return DataFrame if not None/empty, else None."""
    if df is not None and not df.empty:
        return df
    return None


def _fmt_dollars(val) -> str:
    """Format a number as dollars with B/M suffix."""
    if val is None:
        return 'N/A'
    abs_val = abs(val)
    sign = '-' if val < 0 else ''
    if abs_val >= 1e12:
        return f'{sign}${abs_val / 1e12:.2f}T'
    if abs_val >= 1e9:
        return f'{sign}${abs_val / 1e9:.2f}B'
    if abs_val >= 1e6:
        return f'{sign}${abs_val / 1e6:.2f}M'
    return f'{sign}${abs_val:,.2f}'


def _fmt_pct(val) -> str:
    """Format a decimal as percentage."""
    if val is None:
        return 'N/A'
    return f'{val * 100:.1f}%'


def _fmt_pct_val(val) -> str:
    """Format a value that is already a percentage."""
    if val is None:
        return 'N/A'
    return f'{val:+.1f}%'


def _fmt_val(val) -> str:
    """Format a numeric value."""
    if val is None:
        return 'N/A'
    if isinstance(val, float):
        return f'{val:.2f}'
    return str(val)
