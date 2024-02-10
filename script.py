import subprocess
import sys

def install_packages(packages):
    for package in packages:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install_packages(['pandas', 'requests', 'yahoo_fin', 'textblob'])


import pandas as pd
import requests
from yahoo_fin import news
from textblob import TextBlob

class CompanyNewsFetcher:
    """
    Fetches ticker symbols and news for companies in a specified country using NASDAQ's API and yahoo_fin.
    """

    def __init__(self, country):
        """
        Initializes the fetcher for a specific country.
        """
        self.country = country
        self.company_tickers = self.fetch_company_tickers()
        self.company_news = {}
        print(f"🌍 [Initiated] News fetcher for companies in {self.country}.")

    def fetch_company_tickers(self):
        """
        Fetches company tickers from NASDAQ based on the country provided.
        """
        print("🔍 Fetching company tickers...")
        headers = {
            'authority': 'api.nasdaq.com',
            'accept': 'application/json, text/plain, */*',
            'user-agent': 'Mozilla/5.0',
            'origin': 'https://www.nasdaq.com',
        }
        params = {'tableonly': 'true', 'limit': '25', 'offset': '0', 'download': 'true'}
        response = requests.get('https://api.nasdaq.com/api/screener/stocks', headers=headers, params=params)
        data = response.json()['data']
        tickers = pd.DataFrame(data['rows'], columns=data['headers'])
        country_tickers = tickers[tickers['country'] == self.country]['symbol'].tolist()
        print(f"✅ Successfully fetched {len(country_tickers)} tickers for companies in {self.country}.")
        return country_tickers

    def fetch_news_for_company(self, ticker):
        """
        Fetches news for a specific company using its ticker.
        """
        print(f"📰 Fetching news for {ticker}...")
        news_list = news.get_yf_rss(ticker)
        self.company_news[ticker] = {
            'titles': [article.get('title') for article in news_list],
            'summaries': [article.get('summary') for article in news_list]
        }

    def gather_news(self):
        """
        Gathers news for all companies in the country.
        """
        print("🌐 Starting news collection for all listed companies...")
        for ticker in self.company_tickers:
            self.fetch_news_for_company(ticker)
        print("🎉 Finished collecting news for all companies.")

class SentimentAnalyzer(CompanyNewsFetcher):
    """
    Performs sentiment analysis on the news titles and summaries of companies, including sentiment categories and polarities.
    """

    def __init__(self, country):
        """
        Initializes the sentiment analyzer for a specific country.
        """
        super().__init__(country)
        self.analyzed_data = []

    def analyze_sentiment(self, text):
        """
        Analyzes the sentiment polarity and category of the given text.
        """
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        return polarity, 'Positive' if polarity > 0 else 'Negative' if polarity < 0 else 'Neutral'

    def perform_analysis(self):
        """
        Performs sentiment analysis on all fetched news, calculating sentiment polarities and categories.
        """
        print("🔬 Performing sentiment analysis on collected news...")
        for ticker, news in self.company_news.items():
            print(f"🧐 Analyzing {ticker} news sentiment...")
            news_df = pd.DataFrame(news)
            # Calculate sentiment polarities and categories for titles and summaries
            news_df['title_sentiment_polarity'], news_df['title_sentiment'] = zip(*news_df['titles'].apply(self.analyze_sentiment))
            news_df['summary_sentiment_polarity'], news_df['summary_sentiment'] = zip(*news_df['summaries'].apply(self.analyze_sentiment))
            news_df['company'] = ticker
            self.analyzed_data.append(news_df)
        print("✨ Analysis complete. Compiling results...")

    def save_results(self):
        """
        Saves the analyzed sentiment data, including categories and polarities, to a CSV file.
        """
        if self.analyzed_data:
            final_df = pd.concat(self.analyzed_data)
            final_df.to_csv('company_news_sentiment_analysis.csv', index=False)
            print("📁 Results saved to company_news_sentiment_analysis.csv")
        else:
            print("⚠️ No data to save.")

if __name__ == "__main__":
    analyzer = SentimentAnalyzer('Ireland')
    analyzer.gather_news()
    analyzer.perform_analysis()
    analyzer.save_results()
