import requests
import threading
import pygame
from datetime import date


class StocksFetcher():
    def __init__(self, api_key):
        self.api_key = api_key
        self.stocks_data =  {'Apple': {'date': '2025-02-03', 'closing_price': 228.85, 'opening_price': 229.7, 'price_change': -0.8499999999999943, 'percent_change': -0.37}, 'Nvidia': {'date': '2025-02-03', 'closing_price': 117.705, 'opening_price': 114.77, 'price_change': 2.9350000000000023, 'percent_change': 2.55}, 'Microsoft': {'date': '2025-02-03', 'closing_price': 414.0, 'opening_price': 411.6, 'price_change': 2.3999999999999773, 'percent_change': 0.58}, 'Google': {'date': '2025-02-03', 'closing_price': 201.81, 'opening_price': 200.2, 'price_change': 1.6100000000000136, 'percent_change': 0.80}, 'Amazon': {'date': '2025-02-03', 'closing_price': 237.77, 'opening_price': 233.61, 'price_change': 4.159999999999997, 'percent_change': 1.78}}
        self.is_fetching = True

        self.companines = {
            'Apple': 'AAPL',
            'Nvidia': 'NVDA',
            'Microsoft': 'MSFT',
            'Google': 'GOOGL',
            'Amazon': 'AMZN'
        }
    

    def fetch_stocks_data_async(self):
        thread = threading.Thread(target=self.fetch_stocks_data, daemon=True)
        thread.start()


    def fetch_stocks_data(self):
        self.stocks_data = {}
        count = 0
        for company, symbol in self.companines.items():
            try:
                response = requests.get(
                    f"https://api.twelvedata.com/time_series",
                    params={
                        "symbol": symbol,
                        "interval": "1day",
                        "apikey": self.api_key,
                        "outputsize": 1
                    }
                )
                response.raise_for_status()
                data = self.extract_stocks_data(response.json(), company)
                if data:
                    self.stocks_data[company] = data
                count += 1
                print(count)
                print(self.stocks_data)
            except Exception as e:
                print(f"Error fetching stock data for {company}: {e}")
            finally:
                self.is_fetching = False
    

    def extract_stocks_data(self, raw_data, company):
        values = raw_data.get("values", [])
        if not values:
            print(f"No time series data for {company}")
            return None

        latest_data = values[0]  # Only one result when `outputsize=1`
        closing_price = float(latest_data["close"])
        opening_price = float(latest_data["open"])
        price_change = closing_price - opening_price
        percent_change = round((price_change / opening_price) * 100, 2)

        return {
            "date": latest_data["datetime"],
            "closing_price": closing_price,
            "opening_price": opening_price,
            "price_change": price_change,
            "percent_change": percent_change
        }

