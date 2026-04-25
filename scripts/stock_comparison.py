"""
Stock Comparison Module
Compares two or more stocks on fundamentals, growth, valuation,
and generates a head-to-head analysis with upside scenarios.
"""

from typing import List, Dict, Any, Optional
from scripts.fundamental_analysis import FundamentalAnalyzer, _fmt_dollars, _fmt_pct, _fmt_val


class StockComparator:
    """Compare multiple stocks on fundamental metrics."""

    def __init__(self, symbols: List[str]):
        self.symbols = symbols
        self.analyzers = {s: FundamentalAnalyzer(s) for s in symbols}
        self._reports: Dict[str, Dict] = {}

    def _get_report(self, symbol: str) -> Dict[str, Any]:
        if symbol not in self._reports:
            self._reports[symbol] = self.analyzers[symbol].generate_full_report()
        return self._reports[symbol]

    def compare_metrics(self) -> Dict[str, Dict[str, Any]]:
        """Return key metrics for each symbol for side-by-side comparison."""
        result = {}
        for s in self.symbols:
            report = self._get_report(s)
            m = report['metrics']
            v = report['valuation']
            g = report['growth']

            eps_revisions_current = None
            eps_revisions_next = None
            revisions = g.get('eps_revisions', {})
            for period, rev in revisions.items():
                current = rev.get('current')
                ago_90 = rev.get('90d_ago')
                if current and ago_90 and ago_90 != 0:
                    change = ((current - ago_90) / abs(ago_90)) * 100
                    if period == '0y':
                        eps_revisions_current = change
                    elif period == '+1y':
                        eps_revisions_next = change

            result[s] = {
                'price': v['current_price'],
                'market_cap': m['market_cap'],
                'revenue_ttm': m['revenue_ttm'],
                'net_income': m['net_income'],
                'profit_margin': m['profit_margin'],
                'operating_margin': m['operating_margin'],
                'gross_margin': m['gross_margin'],
                'roe': m['roe'],
                'debt_to_equity': m['debt_to_equity'],
                'free_cash_flow': m['free_cash_flow'],
                'revenue_growth': m['revenue_growth'],
                'earnings_growth': m['earnings_growth'],
                'forward_pe': v['forward_pe'],
                'trailing_pe': v['trailing_pe'],
                'peg_ratio': v['peg_ratio'],
                'price_to_sales': m['price_to_sales'],
                'eps_current_year': v['eps_current_year'],
                'eps_next_year': v['eps_next_year'],
                'pe_on_next_year': v['pe_on_next_year'],
                'analyst_target': v['analyst_target'],
                'analyst_low': v['analyst_low'],
                'analyst_high': v['analyst_high'],
                'upside_to_target': v['upside_to_target'],
                'recommendation': v['recommendation'],
                'eps_revision_current_year': eps_revisions_current,
                'eps_revision_next_year': eps_revisions_next,
            }
        return result

    def compute_upside_scenarios(self, symbol: str) -> List[Dict[str, Any]]:
        """Compute price target scenarios based on PE multiples and EPS estimates."""
        report = self._get_report(symbol)
        v = report['valuation']
        price = v['current_price']
        eps_next = v['eps_next_year']
        eps_high = None

        ee = report['estimates']['earnings_estimate']
        if ee is not None and not ee.empty and '+1y' in ee.index:
            eps_high = ee.loc['+1y'].get('high')

        scenarios = []
        if eps_next and price and eps_next > 0:
            fwd_pe = v['forward_pe'] or 20
            # Use sensible PE ranges based on the stock's current valuation
            bear_pe = max(8, fwd_pe * 0.6)
            base_pe = max(10, fwd_pe)
            bull_pe = max(15, fwd_pe * 1.5)

            # Use low EPS estimate for bear case if available
            eps_low = None
            if ee is not None and not ee.empty and '+1y' in ee.index:
                eps_low = ee.loc['+1y'].get('low')

            for label, eps, pe in [
                ('Bear', eps_low or eps_next * 0.7, bear_pe),
                ('Base', eps_next, base_pe),
                ('Bull', eps_next, bull_pe),
                ('Hyper-bull', eps_high or eps_next * 1.3, bull_pe),
            ]:
                target = eps * pe
                upside = ((target - price) / price) * 100
                scenarios.append({
                    'label': label,
                    'eps': eps,
                    'pe': pe,
                    'target_price': target,
                    'upside': upside,
                })
        return scenarios

    def print_comparison(self) -> Dict[str, Dict[str, Any]]:
        """Print a formatted comparison table and return data."""
        metrics = self.compare_metrics()

        print(f"\n{'='*70}")
        print(f"FUNDAMENTAL COMPARISON: {' vs '.join(self.symbols)}")
        print(f"{'='*70}\n")

        rows = [
            ('Price', 'price', lambda v: f'${_fmt_val(v)}'),
            ('Market Cap', 'market_cap', _fmt_dollars),
            ('Revenue (TTM)', 'revenue_ttm', _fmt_dollars),
            ('Net Income (TTM)', 'net_income', _fmt_dollars),
            ('Profit Margin', 'profit_margin', _fmt_pct),
            ('Operating Margin', 'operating_margin', _fmt_pct),
            ('Gross Margin', 'gross_margin', _fmt_pct),
            ('ROE', 'roe', _fmt_pct),
            ('Free Cash Flow', 'free_cash_flow', _fmt_dollars),
            ('Debt/Equity', 'debt_to_equity', lambda v: _fmt_val(v)),
            ('Revenue Growth', 'revenue_growth', _fmt_pct),
            ('Earnings Growth', 'earnings_growth', _fmt_pct),
            ('Forward PE', 'forward_pe', lambda v: _fmt_val(v)),
            ('Trailing PE', 'trailing_pe', lambda v: _fmt_val(v)),
            ('PEG Ratio', 'peg_ratio', lambda v: _fmt_val(v)),
            ('EPS (Current Year)', 'eps_current_year', lambda v: f'${_fmt_val(v)}'),
            ('EPS (Next Year)', 'eps_next_year', lambda v: f'${_fmt_val(v)}'),
            ('PE on Next Year EPS', 'pe_on_next_year', lambda v: _fmt_val(v)),
            ('Analyst Target', 'analyst_target', lambda v: f'${_fmt_val(v)}'),
            ('Upside to Target', 'upside_to_target', lambda v: f'{v:+.1f}%' if v else 'N/A'),
            ('Recommendation', 'recommendation', lambda v: str(v).upper() if v else 'N/A'),
            ('EPS Revision (CY, 90d)', 'eps_revision_current_year', lambda v: f'{v:+.1f}%' if v else 'N/A'),
            ('EPS Revision (NY, 90d)', 'eps_revision_next_year', lambda v: f'{v:+.1f}%' if v else 'N/A'),
        ]

        # Calculate column widths
        label_width = max(len(r[0]) for r in rows) + 2
        col_width = 18

        # Header
        header = f"{'Metric':<{label_width}}"
        for s in self.symbols:
            header += f"{s:>{col_width}}"
        print(header)
        print('-' * (label_width + col_width * len(self.symbols)))

        for label, key, fmt in rows:
            line = f"{label:<{label_width}}"
            for s in self.symbols:
                val = metrics[s].get(key)
                line += f"{fmt(val):>{col_width}}"
            print(line)

        # Upside scenarios
        for s in self.symbols:
            scenarios = self.compute_upside_scenarios(s)
            if scenarios:
                print(f"\n--- {s} Upside Scenarios (Next Year EPS × PE) ---")
                for sc in scenarios:
                    print(f"  {sc['label']:12s}: EPS ${sc['eps']:.2f} × {sc['pe']:.1f}x PE = "
                          f"${sc['target_price']:.0f} ({sc['upside']:+.0f}%)")

        print(f"\n{'='*70}\n")
        return metrics

    def determine_winner(self) -> Dict[str, Any]:
        """Determine which stock has better fundamentals for growth."""
        metrics = self.compare_metrics()
        scores = {s: 0 for s in self.symbols}

        comparisons = []

        def compare(key, label, higher_is_better=True):
            vals = {s: metrics[s].get(key) for s in self.symbols}
            valid = {s: v for s, v in vals.items() if v is not None}
            if len(valid) < 2:
                return
            if higher_is_better:
                winner = max(valid, key=valid.get)
            else:
                winner = min(valid, key=valid.get)
            scores[winner] += 1
            comparisons.append({
                'metric': label,
                'winner': winner,
                'values': vals,
            })

        compare('revenue_growth', 'Revenue Growth', True)
        compare('earnings_growth', 'Earnings Growth', True)
        compare('profit_margin', 'Profit Margin', True)
        compare('operating_margin', 'Operating Margin', True)
        compare('gross_margin', 'Gross Margin', True)
        compare('roe', 'ROE', True)
        compare('free_cash_flow', 'Free Cash Flow', True)
        compare('forward_pe', 'Forward PE (lower=cheaper)', False)
        compare('peg_ratio', 'PEG Ratio (lower=cheaper)', False)
        compare('debt_to_equity', 'Debt/Equity (lower=better)', False)
        compare('upside_to_target', 'Upside to Analyst Target', True)
        compare('eps_revision_current_year', 'EPS Revisions (CY)', True)
        compare('eps_revision_next_year', 'EPS Revisions (NY)', True)

        overall_winner = max(scores, key=scores.get)

        print(f"\n{'='*70}")
        print(f"SCORECARD: {' vs '.join(self.symbols)}")
        print(f"{'='*70}\n")

        for c in comparisons:
            vals_str = " | ".join(f"{s}: {c['values'].get(s, 'N/A')}" for s in self.symbols)
            print(f"  {c['metric']}: Winner = {c['winner']} ({vals_str})")

        print(f"\n  Final Score: ", end="")
        print(" | ".join(f"{s}: {scores[s]}" for s in self.symbols))
        print(f"  Overall Winner on Fundamentals: {overall_winner}")
        print(f"\n{'='*70}\n")

        return {
            'scores': scores,
            'comparisons': comparisons,
            'winner': overall_winner,
        }
