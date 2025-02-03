from datetime import datetime


class SpecialCalculator():
    def __init__(self):
        pass


    @classmethod
    def calculate_strength(cls, cpu_usage, frequency, memory_usage, num_cores, core_usages):
        strength_value = 5  # Base value

        # CPU Usage factor
        if cpu_usage >= 80:
            strength_value -= 3
        elif 50 <= cpu_usage < 80:
            strength_value -= 1

        # CPU Frequency factor
        if frequency >= 3000:
            strength_value += 3
        elif 2000 <= frequency < 3000:
            strength_value += 1

        # Memory Usage factor
        if memory_usage >= 80:
            strength_value -= 2

        # Number of cores factor
        strength_value += max(0, num_cores - 4)  # 4 cores is baseline

        # Individual Core Usage factor
        for core_usage in core_usages:
            if core_usage >= 80:
                strength_value -= 1
        
        return max(1, min(strength_value, 10))


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
    

    @classmethod
    def calculate_endurance(cls, uptime_hours, cpu_temp):
        endurance_value = 5  # Neutral base

        # Uptime Modifiers
        if uptime_hours >= 1:
            endurance_value += min(uptime_hours // 6, 3)  # Max +3
        else:
            endurance_value -= 1

        # Temperature Modifiers
        if cpu_temp < 50:
            endurance_value += 1
        elif cpu_temp > 70:
            endurance_value -= 1
        if cpu_temp > 80:
            endurance_value -= 2

        # Clamp Endurance value between 1 and 10
        endurance_value = max(1, min(endurance_value, 10))

        return endurance_value


    @classmethod
    def calculate_charisma(cls, devices, device_count, gateway_status):
        charisma_value = 5
        charisma_value += min(device_count // 2, 5)
        high_latency_count = sum(1 for latency in devices.values() if latency > 100)

        if high_latency_count > 2:
            charisma_value -= 1
            
        if gateway_status:
            charisma_value += 1

        return max(1, min(charisma_value, 10))

















