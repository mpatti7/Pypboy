import requests
import threading
import pygame


class StocksFetcher():
    def __init__(self, api_key):
        self.api_key = api_key
        self.stocks_data = None
        self.is_fetching = True
    

    def fetch_stocks_data_async(self):
        thread = threading.Thread(target=self.fetch_stocks_data, daemon=True)
        thread.start()


    def fetch_stocks_data(self):
        try:
            response = requests.get(
                f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=AAPL&apikey=YOUR_API_KEY",
                params={"apikey": self.api_key, "symbol": f"AAPL"}
            )
            response.raise_for_status()
            self.weather_data = response.json()

            icon_url = f"http:{self.weather_data['current']['condition']['icon']}"
            self.weather_icon = self.fetch_weather_icon(icon_url)
        except Exception as e:
            print(f"Error fetching weather data: {e}")
        finally:
            self.is_fetching = False
