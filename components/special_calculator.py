from datetime import datetime


class SpecialCalculator():
    def __init__(self):
        pass


    @classmethod
    def calculate_strength(cls, weather_fetcher):
        pass


    @classmethod
    def calculate_perception(cls, weather_fetcher):
        perception_value = 5  # Start with a neutral baseline
        
        # Extract weather information
        current_data = weather_fetcher.weather_data.get("current", {})
        temp_f = current_data.get("temp_f", 0.0)
        wind_mph = current_data.get("wind_mph", 0.0)
        cloud_cover = current_data.get("cloud", 0)
        localtime_epoch = weather_fetcher.weather_data.get("location", {}).get("localtime_epoch")

        # Calculate time of day impact
        if localtime_epoch:
            current_hour = datetime.fromtimestamp(localtime_epoch).hour
            if 6 <= current_hour < 18:  # Daytime
                perception_value += 1
            else:  # Nighttime
                perception_value -= 1

        # Weather-based perception modifiers
        if temp_f < 35:  # Cold weather
            perception_value -= 1
        elif temp_f >= 50 and temp_f <= 85:
            perception_value += 1
        elif temp_f > 85:
            perception_value -= 1

        if wind_mph > 20:  # High wind conditions
            perception_value -= 1

        if cloud_cover > 70:  # Reduced visibility due to heavy clouds
            perception_value -= 1
        
        # Keep perception value in the range [1, 10]
        perception_value = max(1, min(perception_value, 10))

        return perception_value, [temp_f, wind_mph, cloud_cover, current_hour]