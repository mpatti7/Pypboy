from datetime import datetime
from components.luck_manager import LuckManager


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
    

    @classmethod
    def calculate_intelligence(self, stocks_data):
        base_intelligence = 5
        total_impact = 0

        # Define weight factors for each company (sum to 1 for balanced influence)
        weight_factors = {
            "Apple": 0.25,
            "Nvidia": 0.25,
            "Microsoft": 0.2,
            "Google": 0.15,
            "Amazon": 0.15
        }

        # for stock_data in stocks_data:
        for company, data in stocks_data.items():
            percent_change = data["percent_change"]
            weight = weight_factors.get(company, 0)

            # Intelligence change weighted by percent change and company weight
            total_impact += percent_change * weight / 100

        # Adjust intelligence value, ensuring it's within bounds [1, 10]
        intelligence = max(1, min(base_intelligence + total_impact, 10))

        return int(intelligence)
    

    @classmethod
    def calculate_agility(cls, read_speed, write_speed, disk_queue_length, upload_speed, download_speed):
        base_agility = 5
        # Normalize and cap contributions
        io_speed_score = min((read_speed + write_speed) // 100, 2)  # Cap at 2 points
        queue_score = max(min(1 - (disk_queue_length / 10), 1), 0)  # Normalize to max 1 point
        network_speed_score = min((download_speed + upload_speed) // 100, 2)  # Cap at 2 points

        # Calculate final agility score
        agility_score = base_agility + io_speed_score + queue_score + network_speed_score
        agility_score = max(min(agility_score, 10), 1)  # Ensure between 1 and 10

        return int(agility_score)


    @classmethod
    def calculate_luck(cls):
        luck_value = 5
        luck_manager = LuckManager()

        if luck_manager.luck_events['weather_lucky'] != '':
            luck_value += 1
        if luck_manager.luck_events['weather_unlucky'] != '':
            luck_value -= 1

        if luck_manager.luck_events['stocks_lucky'] != '':
            luck_value += 1
        if luck_manager.luck_events['stocks_unlucky'] != '':
            luck_value -= 1
        
        current_time = datetime.now().strftime("%H:%M:%S")
        current_time = datetime.now().strptime(current_time, "%H:%M:%S")

        # print('BOOST')
        # print(luck_manager.boost_times['boost_start'])
        # print(current_time)
        # print(luck_manager.boost_times['boost_end'])

        # print('DECREASE')
        # print(luck_manager.boost_times['decrease_start'])
        # print(current_time)
        # print(luck_manager.boost_times['decrease_end'])

        if luck_manager.boost_times['boost_start'] <= current_time and current_time<= luck_manager.boost_times['boost_end']:
            # print('LUCK BOOST RANGE')
            luck_manager.lucky_range = f'Luck BOOST! {str(luck_manager.boost_times["boost_start"].time())} to {luck_manager.boost_times["boost_end"].time()}'
            luck_value += 1  
        else:
            luck_manager.lucky_range = ''

        if luck_manager.boost_times['decrease_start'] <= current_time and current_time <= luck_manager.boost_times['decrease_end']:
            # print('LUCK DECREASE RANGE')
            luck_manager.unlucky_range = f'Luck DECREASE! {str(luck_manager.boost_times["decrease_start"].time())} to {luck_manager.boost_times["decrease_end"].time()}'
            luck_value -= 1 
        else:
            luck_manager.unlucky_range = ''


        return luck_value














