import random
from datetime import datetime, timedelta
import threading


class LuckManager():
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


    def __init__(self, api_key=None, api_data={}):
        if not hasattr(self, '_initialized'):
            self._initialized = True  # Prevent double initialization
            self.api_key = api_key
            self.api_data = api_data
            self.lucky_event_triggered = False
            self.unlucky_event_triggered = False
            self.last_generated = None
            self.boost_times = {
                'boost_start': '',
                'boost_end': '',
                'decrease_start': '',
                'decrease_end': ''
            }
    

    def set_api_data(self, api_key, api_data):
        self.api_key = api_key
        self.api_data = api_data
        

    def generate_time_ranges(self):
        current_time = datetime.now()

        if self.last_generated is None or current_time - self.last_generated >= timedelta(hours=24):
            boost_start_hour = random.randint(0, 22)  # Random start hour for boost between 00:00 to 22:00
            boost_start_minute = random.randint(0, 59)
            boost_duration = random.randint(1, 4)  # Boost duration between 1 and 4 hours

            self.boost_times['boost_start'] = datetime.strptime(f"{boost_start_hour:02d}:{boost_start_minute:02d}", "%H:%M")
            self.boost_times['boost_end'] = self.boost_times['boost_start'] + timedelta(hours=boost_duration)

            decrease_start_hour = random.randint(0, 22)
            decrease_start_minute = random.randint(0, 59)
            decrease_duration = random.randint(1, 4)

            self.boost_times['decrease_start'] = datetime.strptime(f"{decrease_start_hour:02d}:{decrease_start_minute:02d}", "%H:%M")
            self.boost_times['decrease_end'] = self.boost_times['decrease_start'] + timedelta(hours=decrease_duration)

            self.last_generated = current_time

        # Ensure no overlap between boost and decrease
        while self.boost_times['boost_start'] < self.boost_times['decrease_end'] and self.boost_times['boost_end'] > self.boost_times['decrease_start']:
            self.generate_time_ranges()
    

    def apply_lucky_event(self):
        # Chance to apply a lucky event
        if random.random() < 0.1:  # 10% chance
            self.lucky_event_triggered = True
            key = random.choice(list(self.api_data.keys()))  # Randomly pick a key
            self.api_data[key] = f"{self.api_data[key]} - Lucky!"
        elif random.random() < 0.1:  # 10% chance
            self.unlucky_event_triggered = True
            key = random.choice(list(self.api_data.keys()))  # Randomly pick a key
            self.api_data[key] = f"{self.api_data[key]} - Unlucky!"

        return self.api_data, self.unlucky_event_triggered