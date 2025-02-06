import random
from datetime import datetime, timedelta
import threading


class LuckManager():
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


    def __init__(self, weather_data={}, stocks_data={}):
        if not hasattr(self, '_initialized'):
            self._initialized = True  # Prevent double initialization
            self.weather_data = weather_data
            self.stocks_data = stocks_data
            self.lucky_event_triggered = False
            self.unlucky_event_triggered = False
            self.lucky_range = ''
            self.unlucky_range = ''
            self.last_generated = None
            self.luck_events = {
                'stocks_lucky': '',
                'stocks_unlucky': '',
                'weather_lucky': '',
                'weather_unlucky': ''
            }
            self.boost_times = {
                'boost_start': '',
                'boost_end': '',
                'decrease_start': '',
                'decrease_end': ''
            }
    

    def set_weather_data(self, api_data):
        self.weather_data = api_data
        self.apply_lucky_event_weather()
        

    def set_stocks_data(self, api_data):
        self.stocks_data = api_data
        self.apply_lucky_event_stocks()


    def generate_time_ranges(self):
        current_time = datetime.now()

        if self.last_generated is None or current_time - self.last_generated >= timedelta(hours=24):
            while True:
                boost_start_hour = random.randint(0, 22)
                boost_start_minute = random.randint(0, 59)
                boost_duration = random.randint(1, 4)

                decrease_start_hour = random.randint(0, 22)
                decrease_start_minute = random.randint(0, 59)
                decrease_duration = random.randint(1, 4)

                boost_start = datetime.strptime(f"{boost_start_hour:02d}:{boost_start_minute:02d}", "%H:%M")
                boost_end = boost_start + timedelta(hours=boost_duration)

                decrease_start = datetime.strptime(f"{decrease_start_hour:02d}:{decrease_start_minute:02d}", "%H:%M")
                decrease_end = decrease_start + timedelta(hours=decrease_duration)

                # Ensure ranges do not overlap
                if boost_start >= decrease_end or boost_end <= decrease_start:
                    self.boost_times['boost_start'] = boost_start
                    self.boost_times['boost_end'] = boost_end
                    self.boost_times['decrease_start'] = decrease_start
                    self.boost_times['decrease_end'] = decrease_end
                    break

            self.last_generated = current_time
    

    def apply_lucky_event_weather(self):
        if self.weather_data != {} and self.weather_data != None:
            if random.random() < 0.9:  # 10% chance
                self.lucky_weather_triggered = True
                key = random.choice(list(self.weather_data.keys()))  
                self.weather_data[f"{key}_lucky"] = f"Lucky weather {key}!"
                self.luck_events['weather_lucky'] = f"Lucky weather {key}!"
            elif random.random() < 0.9: 
                self.unlucky_weather_triggered = True
                key = random.choice(list(self.weather_data.keys()))  
                self.weather_data[f"{key}_unlucky"] = f"Unlucky weather {key} :("
                self.luck_events['weather_unlucky'] = f"Unlucky weather {key} :("
            else:
                self.luck_events['weather_lucky'] = ''
                self.luck_events['weather_unlucky'] = ''


    def apply_lucky_event_stocks(self):
        if self.stocks_data != {} and self.stocks_data != None:
            if random.random() < 0.9:  
                self.lucky_stocks_triggered = True
                key = random.choice(list(self.stocks_data.keys()))  
                # self.stocks_data[f"{key}_lucky"] = f"Lucky {key} stock!"
                self.luck_events['stocks_lucky'] = f"Lucky {key} stock!"
            elif random.random() < 0.9: 
                self.unlucky_stocks_triggered = True
                key = random.choice(list(self.stocks_data.keys()))  
                # self.stocks_data[f"{key}_unlucky"] = f"Unlucky {key} stock :("
                self.luck_events['stocks_unlucky'] = f"Unlucky {key} stock :("
            else:
                self.luck_events['stocks_lucky'] = ''
                self.luck_events['stocks_unlucky'] = ''