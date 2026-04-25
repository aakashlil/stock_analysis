"""
News Scraper Module
Fetches latest news for stocks from various sources using RSS feeds
"""

import requests
import feedparser
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import re


class NewsScraper:
    """Fetch latest news for stocks from multiple sources using RSS feeds"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def fetch_yahoo_finance_rss(self, symbol: str, limit: int = 5) -> List[Dict[str, str]]:
        """
        Fetch news from Yahoo Finance RSS feed
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL', 'QCOM')
            limit: Number of news items to fetch
        
        Returns:
            List of news items with title, link, date, and summary
        """
        try:
            # Yahoo Finance RSS feed
            url = f"https://finance.yahoo.com/rss/headline?s={symbol}"
            feed = feedparser.parse(url)
            
            news_items = []
            for entry in feed.entries[:limit]:
                try:
                    # Parse date
                    date = ""
                    if hasattr(entry, 'published'):
                        date = entry.published
                    elif hasattr(entry, 'updated'):
                        date = entry.updated
                    
                    # Get summary
                    summary = ""
                    if hasattr(entry, 'summary'):
                        summary = entry.summary
                    elif hasattr(entry, 'description'):
                        summary = entry.description
                    
                    news_items.append({
                        'title': entry.title if hasattr(entry, 'title') else "No title",
                        'link': entry.link if hasattr(entry, 'link') else "",
                        'summary': summary,
                        'date': date,
                        'source': 'Yahoo Finance'
                    })
                except Exception as e:
                    continue
            
            return news_items
        
        except Exception as e:
            print(f"Error fetching Yahoo Finance RSS: {e}")
            return []
    
    def fetch_google_news_rss(self, symbol: str, limit: int = 5) -> List[Dict[str, str]]:
        """
        Fetch news from Google News RSS feed
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL', 'QCOM')
            limit: Number of news items to fetch
        
        Returns:
            List of news items with title, link, date, and summary
        """
        try:
            # Google News RSS feed for stock
            url = f"https://news.google.com/rss/search?q={symbol}+stock&hl=en-US&gl=US&ceid=US:en"
            feed = feedparser.parse(url)
            
            news_items = []
            for entry in feed.entries[:limit]:
                try:
                    # Parse date
                    date = ""
                    if hasattr(entry, 'published'):
                        date = entry.published
                    elif hasattr(entry, 'updated'):
                        date = entry.updated
                    
                    # Get summary
                    summary = ""
                    if hasattr(entry, 'summary'):
                        summary = entry.summary
                    elif hasattr(entry, 'description'):
                        summary = entry.description
                    
                    news_items.append({
                        'title': entry.title if hasattr(entry, 'title') else "No title",
                        'link': entry.link if hasattr(entry, 'link') else "",
                        'summary': summary,
                        'date': date,
                        'source': 'Google News'
                    })
                except Exception as e:
                    continue
            
            return news_items
        
        except Exception as e:
            print(f"Error fetching Google News RSS: {e}")
            return []
    
    def fetch_bloomberg_rss(self, symbol: str, limit: int = 5) -> List[Dict[str, str]]:
        """
        Fetch news from Bloomberg RSS feed
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL', 'QCOM')
            limit: Number of news items to fetch
        
        Returns:
            List of news items with title, link, date, and summary
        """
        try:
            # Bloomberg Technology RSS (general tech news)
            url = "https://feeds.bloomberg.com/technology/news.rss"
            feed = feedparser.parse(url)
            
            news_items = []
            # Filter for symbol mentions in title
            for entry in feed.entries:
                if len(news_items) >= limit:
                    break
                try:
                    title = entry.title if hasattr(entry, 'title') else ""
                    if symbol.upper() in title.upper():
                        # Parse date
                        date = ""
                        if hasattr(entry, 'published'):
                            date = entry.published
                        elif hasattr(entry, 'updated'):
                            date = entry.updated
                        
                        # Get summary
                        summary = ""
                        if hasattr(entry, 'summary'):
                            summary = entry.summary
                        elif hasattr(entry, 'description'):
                            summary = entry.description
                        
                        news_items.append({
                            'title': title,
                            'link': entry.link if hasattr(entry, 'link') else "",
                            'summary': summary,
                            'date': date,
                            'source': 'Bloomberg'
                        })
                except Exception as e:
                    continue
            
            return news_items
        
        except Exception as e:
            print(f"Error fetching Bloomberg RSS: {e}")
            return []
    
    def fetch_reuters_rss(self, symbol: str, limit: int = 5) -> List[Dict[str, str]]:
        """
        Fetch news from Reuters RSS feed
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL', 'QCOM')
            limit: Number of news items to fetch
        
        Returns:
            List of news items with title, link, date, and summary
        """
        try:
            # Reuters Business News RSS
            url = "https://www.reutersagency.com/feed/?taxonomy=best-sectors&post_type=best"
            feed = feedparser.parse(url)
            
            news_items = []
            # Filter for symbol mentions in title
            for entry in feed.entries:
                if len(news_items) >= limit:
                    break
                try:
                    title = entry.title if hasattr(entry, 'title') else ""
                    if symbol.upper() in title.upper():
                        # Parse date
                        date = ""
                        if hasattr(entry, 'published'):
                            date = entry.published
                        elif hasattr(entry, 'updated'):
                            date = entry.updated
                        
                        # Get summary
                        summary = ""
                        if hasattr(entry, 'summary'):
                            summary = entry.summary
                        elif hasattr(entry, 'description'):
                            summary = entry.description
                        
                        news_items.append({
                            'title': title,
                            'link': entry.link if hasattr(entry, 'link') else "",
                            'summary': summary,
                            'date': date,
                            'source': 'Reuters'
                        })
                except Exception as e:
                    continue
            
            return news_items
        
        except Exception as e:
            print(f"Error fetching Reuters RSS: {e}")
            return []
    
    def fetch_all_news(self, symbol: str, sources: List[str] = None, limit: int = 5) -> List[Dict[str, str]]:
        """
        Fetch news from multiple sources using RSS feeds
        
        Args:
            symbol: Stock symbol
            sources: List of sources to fetch from (default: yahoo, google)
            limit: Number of news items per source
        
        Returns:
            Combined list of news items from all sources
        """
        if sources is None:
            sources = ['yahoo', 'google']
        
        all_news = []
        
        if 'yahoo' in sources:
            all_news.extend(self.fetch_yahoo_finance_rss(symbol, limit))
        
        if 'google' in sources:
            all_news.extend(self.fetch_google_news_rss(symbol, limit))
        
        if 'bloomberg' in sources:
            all_news.extend(self.fetch_bloomberg_rss(symbol, limit))
        
        if 'reuters' in sources:
            all_news.extend(self.fetch_reuters_rss(symbol, limit))
        
        return all_news
    
    def detect_key_events(self, news_items: List[Dict[str, str]]) -> Dict[str, List[Dict[str, str]]]:
        """
        Detect key events from news items (earnings calls, product launches, announcements)
        
        Args:
            news_items: List of news items
        
        Returns:
            Dictionary with categorized events (including title and date)
        """
        events = {
            'earnings_calls': [],
            'product_launches': [],
            'company_announcements': [],
            'partnerships': [],
            'regulatory': []
        }
        
        # Define keywords for each event type
        earnings_keywords = [
            'earnings call', 'earnings report', 'quarterly results', 'q1 earnings', 
            'q2 earnings', 'q3 earnings', 'q4 earnings', 'fiscal', 'eps',
            'earnings per share', 'revenue guidance', 'earnings release',
            'conference call', 'quarterly earnings', 'fiscal quarter'
        ]
        
        product_launch_keywords = [
            'launch', 'release', 'unveil', 'introduce', 'announce', 'chip',
            'processor', 'gpu', 'cpu', 'semiconductor', 'product', 'new chip',
            'snapdragon', 'platform', 'technology', 'innovation', 'breakthrough',
            'next-generation', 'new product', 'product line', 'series'
        ]
        
        announcement_keywords = [
            'announce', 'announcement', 'declare', 'reveal', 'statement',
            'press release', 'strategic', 'acquisition', 'merger', 'deal',
            'investment', 'expansion', 'partnership', 'collaboration',
            'agreement', 'joint venture', 'strategic partnership'
        ]
        
        partnership_keywords = [
            'partnership', 'collaboration', 'joint venture', 'alliance',
            'agreement', 'deal', 'collaborate', 'partner', 'strategic alliance',
            'memorandum of understanding', 'mou'
        ]
        
        regulatory_keywords = [
            'regulation', 'regulatory', 'approval', 'fda', 'sec', 'compliance',
            'antitrust', 'lawsuit', 'legal', 'ruling', 'investigation',
            'compliance', 'regulatory approval', 'clearance'
        ]
        
        for item in news_items:
            text = (item['title'] + ' ' + item.get('summary', '')).lower()
            
            # Check for earnings calls
            if any(keyword in text for keyword in earnings_keywords):
                events['earnings_calls'].append({
                    'title': item['title'],
                    'date': item.get('date', 'N/A'),
                    'source': item.get('source', '')
                })
            
            # Check for product launches
            if any(keyword in text for keyword in product_launch_keywords):
                events['product_launches'].append({
                    'title': item['title'],
                    'date': item.get('date', 'N/A'),
                    'source': item.get('source', '')
                })
            
            # Check for company announcements
            if any(keyword in text for keyword in announcement_keywords):
                events['company_announcements'].append({
                    'title': item['title'],
                    'date': item.get('date', 'N/A'),
                    'source': item.get('source', '')
                })
            
            # Check for partnerships
            if any(keyword in text for keyword in partnership_keywords):
                events['partnerships'].append({
                    'title': item['title'],
                    'date': item.get('date', 'N/A'),
                    'source': item.get('source', '')
                })
            
            # Check for regulatory events
            if any(keyword in text for keyword in regulatory_keywords):
                events['regulatory'].append({
                    'title': item['title'],
                    'date': item.get('date', 'N/A'),
                    'source': item.get('source', '')
                })
        
        return events
    
    def fetch_article_content(self, url: str) -> str:
        """
        Fetch full article content from a URL
        
        Args:
            url: Article URL
        
        Returns:
            Article text content
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code != 200:
                return ""
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "footer", "header", "aside"]):
                script.decompose()
            
            # Try to find main content
            content_selectors = [
                'article',
                '[class*="article-body"]',
                '[class*="story-body"]',
                '[class*="post-content"]',
                '[class*="entry-content"]',
                'main',
                '[id*="article"]',
                '[id*="content"]'
            ]
            
            article_text = ""
            for selector in content_selectors:
                elements = soup.select(selector)
                if elements:
                    article_text = ' '.join([elem.get_text(strip=True) for elem in elements])
                    if len(article_text) > 200:  # Only use if we got substantial content
                        break
            
            # Fallback: get all paragraphs
            if not article_text or len(article_text) < 200:
                paragraphs = soup.find_all('p')
                article_text = ' '.join([p.get_text(strip=True) for p in paragraphs])
            
            # Clean up text
            article_text = re.sub(r'\s+', ' ', article_text).strip()
            
            return article_text
        
        except Exception as e:
            print(f"Error fetching article content: {e}")
            return ""
    
    def summarize_article(self, content: str, max_sentences: int = 3) -> str:
        """
        Summarize article content using extractive summarization
        
        Args:
            content: Article text content
            max_sentences: Maximum number of sentences in summary
        
        Returns:
            Article summary
        """
        if not content or len(content) < 100:
            return content
        
        # Split into sentences
        sentences = re.split(r'[.!?]+', content)
        sentences = [s.strip() for s in sentences if s.strip() and len(s) > 20]
        
        if len(sentences) <= max_sentences:
            return '. '.join(sentences)
        
        # Score sentences based on position and length
        scores = []
        for i, sentence in enumerate(sentences):
            score = 0
            
            # Position score (first and last sentences are important)
            if i == 0 or i == len(sentences) - 1:
                score += 2
            elif i < 3 or i > len(sentences) - 4:
                score += 1
            
            # Length score (medium length sentences are usually more informative)
            length = len(sentence.split())
            if 10 <= length <= 30:
                score += 2
            elif 5 <= length <= 40:
                score += 1
            
            # Keyword score (sentences with important words)
            important_words = ['earnings', 'revenue', 'profit', 'growth', 'launch', 
                            'announce', 'deal', 'partnership', 'acquisition', 
                            'stock', 'price', 'market', 'investment', 'chip',
                            'technology', 'ai', 'artificial intelligence']
            if any(word in sentence.lower() for word in important_words):
                score += 1
            
            scores.append((score, i, sentence))
        
        # Sort by score and get top sentences
        scores.sort(reverse=True, key=lambda x: x[0])
        top_sentences = sorted([s[1] for s in scores[:max_sentences]])
        
        summary = '. '.join([sentences[i] for i in top_sentences])
        return summary
    
    def analyze_full_articles(self, news_items: List[Dict[str, str]], max_articles: int = 3) -> List[Dict[str, str]]:
        """
        Fetch and analyze full articles from news items
        
        Args:
            news_items: List of news items
            max_articles: Maximum number of articles to analyze
        
        Returns:
            List of articles with full content and summaries
        """
        analyzed_articles = []
        
        for item in news_items[:max_articles]:
            if not item.get('link'):
                continue
            
            print(f"  Fetching full article: {item['title'][:50]}...")
            content = self.fetch_article_content(item['link'])
            
            if content:
                summary = self.summarize_article(content)
                analyzed_articles.append({
                    'title': item['title'],
                    'link': item['link'],
                    'date': item.get('date', 'N/A'),
                    'source': item.get('source', ''),
                    'full_content': content,
                    'summary': summary
                })
            else:
                analyzed_articles.append({
                    'title': item['title'],
                    'link': item['link'],
                    'date': item.get('date', 'N/A'),
                    'source': item.get('source', ''),
                    'full_content': item.get('summary', ''),
                    'summary': item.get('summary', '')
                })
        
        return analyzed_articles
    
    def extract_stock_symbols(self, text: str) -> List[str]:
        """
        Extract stock symbols from text using regex patterns
        
        Args:
            text: Text to search for stock symbols
        
        Returns:
            List of stock symbols found
        """
        # Common stock symbol patterns (1-5 uppercase letters)
        pattern = r'\b[A-Z]{1,5}\b'
        matches = re.findall(pattern, text)
        
        # Filter out common words that are not stock symbols
        common_words = {
            'THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN', 'HAD', 'HER', 'WAS',
            'ONE', 'OUR', 'OUT', 'HAS', 'HAVE', 'BEEN', 'THIS', 'THAT', 'WITH', 'THEY', 'FROM',
            'WHAT', 'WHEN', 'MORE', 'WILL', 'SOME', 'TIME', 'LIKE', 'JUST', 'VERY', 'COME',
            'COULD', 'WOULD', 'SHOULD', 'MAKE', 'TAKE', 'INTO', 'YEAR', 'YOUR', 'GOOD', 'SOME',
            'THEM', 'THEN', 'THAN', 'LOOK', 'ONLY', 'COME', 'COULD', 'AFTER', 'ALSO', 'OTHER',
            'HOW', 'THEIR', 'WORK', 'FIRST', 'WELL', 'WAY', 'WHERE', 'WHO', 'MAY', 'DOWN',
            'BECAUSE', 'EACH', 'JUST', 'HOW', 'MOST', 'PEOPLE', 'WANT', 'BEEN', 'GOOD', 'NEW',
            'TAKE', 'USED', 'GET', 'PLACE', 'MADE', 'LIVE', 'WHERE', 'BACK', 'LITTLE', 'ONLY',
            'ROUND', 'MAN', 'YEAR', 'CAME', 'SHOW', 'EVERY', 'GOOD', 'ME', 'GIVE', 'OUR',
            'UNDER', 'NAME', 'VERY', 'THROUGH', 'JUST', 'FORM', 'SENTENCE', 'GREAT', 'THINK',
            'SAY', 'HELP', 'LOW', 'DIFFERENT', 'BECAUSE', 'TURN', 'HERE', 'ASK', 'SHOULD',
            'MEAN', 'MOVE', 'TRY', 'KIND', 'HAND', 'PICTURE', 'AGAIN', 'CHANGE', 'OFF', 'PLAY',
            'SPELL', 'AIR', 'AWAY', 'ANIMAL', 'HOUSE', 'POINT', 'PAGE', 'LETTER', 'MOTHER',
            'ANSWER', 'FOUND', 'STUDY', 'STILL', 'LEARN', 'SHOULD', 'AMERICA', 'WORLD'
        }
        
        # Also filter out month abbreviations
        months = {'JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'}
        
        symbols = [match for match in matches if match not in common_words and match not in months]
        
        # Remove duplicates while preserving order
        seen = set()
        unique_symbols = []
        for symbol in symbols:
            if symbol not in seen:
                seen.add(symbol)
                unique_symbols.append(symbol)
        
        return unique_symbols
    
    def compare_mentioned_stocks(self, target_symbol: str, news_items: List[Dict[str, str]], 
                                  max_stocks: int = 5) -> Dict[str, any]:
        """
        Extract stocks mentioned in news and compare with target stock
        
        Args:
            target_symbol: Target stock symbol (e.g., 'QCOM')
            news_items: List of news items
            max_stocks: Maximum number of stocks to compare
        
        Returns:
            Dictionary with comparison data
        """
        # Extract symbols from all news titles and summaries
        all_text = ' '.join([item['title'] + ' ' + item.get('summary', '') for item in news_items])
        mentioned_symbols = self.extract_stock_symbols(all_text)
        
        # Remove target symbol from list
        mentioned_symbols = [s for s in mentioned_symbols if s != target_symbol.upper()]
        
        if not mentioned_symbols:
            return {
                'mentioned_stocks': [],
                'comparison': 'No other stocks mentioned in news articles.'
            }
        
        # Limit to max_stocks
        mentioned_symbols = mentioned_symbols[:max_stocks]
        
        # Try to fetch basic data for mentioned stocks
        from scripts.data_fetcher import DataFetcher
        fetcher = DataFetcher()
        
        comparison_data = []
        for symbol in mentioned_symbols:
            try:
                # Try to fetch recent data
                data = fetcher.fetch_stock_data(symbol, source="yahoo", period="1mo")
                if not data.empty:
                    current_price = data['Close'].iloc[-1]
                    price_change = ((data['Close'].iloc[-1] - data['Close'].iloc[0]) / data['Close'].iloc[0]) * 100
                    comparison_data.append({
                        'symbol': symbol,
                        'current_price': current_price,
                        'price_change_percent': price_change
                    })
            except:
                # If fetch fails, just include the symbol
                comparison_data.append({
                    'symbol': symbol,
                    'current_price': 'N/A',
                    'price_change_percent': 'N/A'
                })
        
        # Generate comparison summary
        if comparison_data:
            comparison_text = f"Found {len(comparison_data)} other stocks mentioned in news: "
            comparison_text += ', '.join([d['symbol'] for d in comparison_data])
            
            # Add performance comparison if available
            valid_data = [d for d in comparison_data if d['current_price'] != 'N/A']
            if valid_data:
                comparison_text += "\n\nPerformance Comparison (1 month):"
                for stock in valid_data:
                    change_str = f"+{stock['price_change_percent']:.2f}%" if stock['price_change_percent'] > 0 else f"{stock['price_change_percent']:.2f}%"
                    comparison_text += f"\n  {stock['symbol']}: ${stock['current_price']:.2f} ({change_str})"
        else:
            comparison_text = f"Found {len(mentioned_symbols)} mentioned stocks but could not fetch comparison data."
        
        return {
            'mentioned_stocks': comparison_data,
            'comparison': comparison_text
        }
    
    def analyze_stock_sentiment(self, symbol: str, limit: int = 3) -> Dict[str, any]:
        """
        Analyze sentiment for a specific stock based on its news
        
        Args:
            symbol: Stock symbol
            limit: Number of news items to analyze
        
        Returns:
            Dictionary with sentiment data
        """
        try:
            news_items = self.fetch_all_news(symbol, sources=['yahoo', 'google'], limit=limit)
            if not news_items:
                return {
                    'symbol': symbol,
                    'sentiment': 'neutral',
                    'positive_count': 0,
                    'negative_count': 0,
                    'neutral_count': 0,
                    'news_count': 0
                }
            
            # Analyze sentiment
            all_text = []
            for item in news_items:
                all_text.append(item['title'].lower())
                if item['summary']:
                    all_text.append(item['summary'].lower())
            
            combined_text = ' '.join(all_text)
            
            positive_keywords = [
                'surge', 'rally', 'gain', 'rise', 'soar', 'jump', 'boost', 'growth',
                'beat', 'exceed', 'strong', 'positive', 'bullish', 'upgrade', 'buy',
                'profit', 'earnings', 'revenue', 'expansion', 'innovation', 'breakthrough',
                'success', 'win', 'lead', 'outperform', 'optimistic', 'opportunity'
            ]
            
            negative_keywords = [
                'fall', 'drop', 'decline', 'plunge', 'crash', 'loss', 'miss', 'weak',
                'negative', 'bearish', 'downgrade', 'sell', 'concern', 'risk', 'warning',
                'cut', 'layoff', 'struggle', 'challenge', 'downside', 'pessimistic',
                'uncertainty', 'volatility', 'decline', 'recession', 'slowdown'
            ]
            
            positive_count = sum(1 for word in positive_keywords if word in combined_text)
            negative_count = sum(1 for word in negative_keywords if word in combined_text)
            
            if positive_count > negative_count * 1.5:
                sentiment = 'positive'
            elif negative_count > positive_count * 1.5:
                sentiment = 'negative'
            else:
                sentiment = 'neutral'
            
            return {
                'symbol': symbol,
                'sentiment': sentiment,
                'positive_count': positive_count,
                'negative_count': negative_count,
                'neutral_count': len(news_items) - positive_count - negative_count,
                'news_count': len(news_items)
            }
        except Exception as e:
            return {
                'symbol': symbol,
                'sentiment': 'neutral',
                'positive_count': 0,
                'negative_count': 0,
                'neutral_count': 0,
                'news_count': 0
            }
    
    def compare_sentiment_across_stocks(self, target_symbol: str, mentioned_symbols: List[str]) -> Dict[str, any]:
        """
        Compare sentiment across target stock and mentioned stocks
        
        Args:
            target_symbol: Target stock symbol
            mentioned_symbols: List of mentioned stock symbols
        
        Returns:
            Dictionary with sentiment comparison data
        """
        # Analyze target stock sentiment
        target_sentiment = self.analyze_stock_sentiment(target_symbol, limit=3)
        
        # Analyze mentioned stocks sentiment
        mentioned_sentiments = []
        for symbol in mentioned_symbols[:5]:  # Limit to 5 stocks
            sentiment_data = self.analyze_stock_sentiment(symbol, limit=2)
            mentioned_sentiments.append(sentiment_data)
        
        # Generate comparison summary
        comparison_text = f"Sentiment Comparison:\n"
        comparison_text += f"  {target_symbol}: {target_sentiment['sentiment'].upper()} "
        comparison_text += f"(+{target_sentiment['positive_count']}, -{target_sentiment['negative_count']})\n"
        
        for sentiment_data in mentioned_sentiments:
            comparison_text += f"  {sentiment_data['symbol']}: {sentiment_data['sentiment'].upper()} "
            comparison_text += f"(+{sentiment_data['positive_count']}, -{sentiment_data['negative_count']})\n"
        
        # Determine overall sentiment trend
        all_sentiments = [target_sentiment['sentiment']] + [s['sentiment'] for s in mentioned_sentiments]
        positive_count = all_sentiments.count('positive')
        negative_count = all_sentiments.count('negative')
        
        if positive_count > negative_count:
            trend = "Overall sector sentiment is BULLISH"
        elif negative_count > positive_count:
            trend = "Overall sector sentiment is BEARISH"
        else:
            trend = "Overall sector sentiment is MIXED/NEUTRAL"
        
        comparison_text += f"\n{trend}"
        
        return {
            'target_sentiment': target_sentiment,
            'mentioned_sentiments': mentioned_sentiments,
            'comparison': comparison_text,
            'trend': trend
        }
    
    def generate_news_summary(self, news_items: List[Dict[str, str]]) -> Dict[str, any]:
        """
        Generate a summary and conclusion from news items
        
        Args:
            news_items: List of news items
        
        Returns:
            Dictionary with summary, sentiment, and conclusion
        """
        if not news_items:
            return {
                'summary': 'No news available for analysis.',
                'sentiment': 'neutral',
                'conclusion': 'Unable to determine outlook due to lack of news data.',
                'key_themes': [],
                'positive_count': 0,
                'negative_count': 0,
                'neutral_count': 0,
                'key_events': {}
            }
        
        # Extract titles and summaries
        all_text = []
        for item in news_items:
            all_text.append(item['title'].lower())
            if item['summary']:
                all_text.append(item['summary'].lower())
        
        combined_text = ' '.join(all_text)
        
        # Define positive and negative keywords
        positive_keywords = [
            'surge', 'rally', 'gain', 'rise', 'soar', 'jump', 'boost', 'growth',
            'beat', 'exceed', 'strong', 'positive', 'bullish', 'upgrade', 'buy',
            'profit', 'earnings', 'revenue', 'expansion', 'innovation', 'breakthrough',
            'success', 'win', 'lead', 'outperform', 'optimistic', 'opportunity'
        ]
        
        negative_keywords = [
            'fall', 'drop', 'decline', 'plunge', 'crash', 'loss', 'miss', 'weak',
            'negative', 'bearish', 'downgrade', 'sell', 'concern', 'risk', 'warning',
            'cut', 'layoff', 'struggle', 'challenge', 'downside', 'pessimistic',
            'uncertainty', 'volatility', 'decline', 'recession', 'slowdown'
        ]
        
        # Count sentiment
        positive_count = sum(1 for word in positive_keywords if word in combined_text)
        negative_count = sum(1 for word in negative_keywords if word in combined_text)
        neutral_count = len(news_items) - positive_count - negative_count
        
        # Determine overall sentiment
        if positive_count > negative_count * 1.5:
            sentiment = 'positive'
        elif negative_count > positive_count * 1.5:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
        
        # Extract key themes
        themes = []
        theme_keywords = {
            'Earnings': ['earnings', 'eps', 'revenue', 'profit', 'quarterly'],
            'AI/Technology': ['ai', 'artificial intelligence', 'chip', 'semiconductor', 'technology', 'innovation'],
            'Market Movement': ['stock', 'price', 'rally', 'surge', 'drop', 'market'],
            'Analyst Views': ['analyst', 'rating', 'upgrade', 'downgrade', 'target'],
            'Regulatory': ['regulation', 'legal', 'lawsuit', 'compliance', 'antitrust'],
            'Competition': ['competitor', 'competition', 'rival', 'market share']
        }
        
        for theme, keywords in theme_keywords.items():
            if any(keyword in combined_text for keyword in keywords):
                themes.append(theme)
        
        # Detect key events
        key_events = self.detect_key_events(news_items)
        
        # Generate summary
        summary = f"Analyzed {len(news_items)} recent news articles. "
        if themes:
            summary += f"Key themes: {', '.join(themes)}. "
        summary += f"Sentiment analysis shows {sentiment} outlook "
        summary += f"({positive_count} positive, {negative_count} negative indicators)."
        
        # Generate conclusion
        if sentiment == 'positive':
            conclusion = f"Overall news sentiment is positive for the stock. Recent developments suggest favorable conditions. Consider monitoring for continued positive momentum."
        elif sentiment == 'negative':
            conclusion = f"Overall news sentiment is negative for the stock. Recent developments indicate potential challenges. Exercise caution and monitor for further developments."
        else:
            conclusion = f"Overall news sentiment is neutral/mixed. Recent developments show both positive and negative factors. Monitor for clearer directional signals before making decisions."
        
        return {
            'summary': summary,
            'sentiment': sentiment,
            'conclusion': conclusion,
            'key_themes': themes,
            'positive_count': positive_count,
            'negative_count': negative_count,
            'neutral_count': neutral_count,
            'key_events': key_events
        }
    
    def display_news(self, news_items: List[Dict[str, str]]):
        """
        Display news items in a formatted way
        
        Args:
            news_items: List of news items
        """
        if not news_items:
            print("No news items found.")
            return
        
        print(f"\n{'='*60}")
        print(f"Latest News Updates ({len(news_items)} items)")
        print(f"{'='*60}\n")
        
        for i, item in enumerate(news_items, 1):
            print(f"{i}. [{item['source']}] {item['title']}")
            if item['date']:
                print(f"   Date: {item['date']}")
            if item['summary']:
                # Clean HTML from summary if present
                summary = item['summary']
                if '<' in summary:
                    from bs4 import BeautifulSoup
                    summary = BeautifulSoup(summary, 'html.parser').get_text()
                print(f"   Summary: {summary[:200]}...")
            if item['link']:
                print(f"   Link: {item['link']}")
            print()


# Convenience function
def get_stock_news(symbol: str, sources: List[str] = None, limit: int = 3) -> List[Dict[str, str]]:
    """Convenience function to fetch stock news"""
    scraper = NewsScraper()
    return scraper.fetch_all_news(symbol, sources, limit)
