import random
import math
from datetime import datetime

"""
In the program, the decision was made to omit the inclusion of Heart Rate Variability (HRV). HRV is a method for measuring the time gap between heartbeats. When simulating realistic heart rates, it is crucial to account for HRV as it mirrors the natural fluctuations in heart rate.

However, incorporating HRV requires the use of algorithms that replicate real-life patterns of heart rate variation based on factors such as age, fitness, and stress. The rationale behind not including HRV in this program is that it could potentially increase the program's execution time.

The prolonged execution time is partially attributed to the random intervals of sleep introduced between each step in the program. These random pauses introduce unpredictable delays, leading to an overall increase in the program's runtime. To enhance the program's speed, one solution is to use fixed intervals for these pauses instead of random ones. This adjustment makes the program more predictable and results in faster execution.
"""

# Resting and stressed heart rate ranges for different age groups
age_groups = {
    'child': {'relaxed': (80, 100), 'stressed': (120, 160)},
    'adult': {'relaxed': (60, 80), 'stressed': (100, 150)},
    'elderly': {'relaxed': (70, 90), 'stressed': (110, 140)}
}

# Get age and age group for the passenger and driver
def get_age_group(age, is_driver=False):
    if (is_driver and (age < 18 or age > 100)) or (not is_driver and age < 18):
        raise ValueError("Invalid age for driver/passenger.")
    elif age < 65:
        return 'adult'
    elif age < 100:
        return 'elderly'
    else:
        raise ValueError("Invalid age for driver/passenger.")

# Function to simulate heart rate with a sine wave and time-of-day variations
def simulate_heart_rate(base_rate, amplitude, frequency, time, time_of_day_factor):
    return base_rate + amplitude * math.sin(2 * math.pi * frequency * time) * time_of_day_factor

# Function to introduce emotional context
def get_emotional_factor():
    return random.uniform(0.5, 1.5)

# Function to get time of day factor (adjustment based on circadian rhythm)
def get_time_of_day_factor(time):
    # Mimic natural variations in heart rate based on the time of day
    hour = datetime.fromtimestamp(time).hour
    if 6 <= hour < 12:  # Morning
        return 1.2
    elif 12 <= hour < 18:  # Afternoon
        return 1.0
    elif 18 <= hour < 24:  # Evening
        return 1.1
    else:  # Night
        return 0.9

# Prompt the user to enter the age of the passenger and validate it
while True:
    try:
        passenger_age = int(input("Enter the age of the passenger: "))
        passenger_age_group = get_age_group(passenger_age)
        break
    except ValueError as e:
        print(str(e))

# Prompt the user to enter the age of the driver and validate it
while True:
    try:
        driver_age = int(input("Enter the age of the driver: "))
        driver_age_group = get_age_group(driver_age, is_driver=True)
        break
    except ValueError as e:
        print(str(e))

passenger_heart_rate_data = []
driver_heart_rate_data = []

ride_duration = 6 * 60  # 6 minutes in seconds
time_interval = 1  # 1 second between heart rate measurements
frequency = 1/10  # Frequency of the heart rate simulation

for t in range(ride_duration):
    # Determine whether the passenger and driver start the trip calmly or not
    start_state = random.random() < 0.5

    # Introduce emotional context factors
    emotional_factor_passenger = get_emotional_factor()
    emotional_factor_driver = get_emotional_factor()

    # Get time of day factor
    time_of_day_factor = get_time_of_day_factor(t)

    # Simulate heart rate for the passenger
    passenger_hr_range = age_groups[passenger_age_group]['relaxed'] if start_state else age_groups[passenger_age_group]['stressed']
    passenger_heart_rate = simulate_heart_rate(
        emotional_factor_passenger * random.uniform(*passenger_hr_range),  # base_rate
        random.uniform(5, 15),  # amplitude
        frequency,
        t,
        time_of_day_factor
    )
    passenger_heart_rate_data.append(passenger_heart_rate)

    # Simulate heart rate for the driver
    driver_hr_range = age_groups[driver_age_group]['relaxed'] if start_state else age_groups[driver_age_group]['stressed']
    driver_heart_rate = simulate_heart_rate(
        emotional_factor_driver * random.uniform(*driver_hr_range),  # base_rate
        random.uniform(5, 15),  # amplitude
        frequency,
        t,
        time_of_day_factor
    )
    driver_heart_rate_data.append(driver_heart_rate)

# Save heart rate data to a file
with open('heart_rate_data.txt', 'w') as file:
    file.write("Passenger Heart Rate, Driver Heart Rate\n")
    for passenger_hr, driver_hr in zip(passenger_heart_rate_data, driver_heart_rate_data):
        file.write(f"{passenger_hr},{driver_hr}\n")

print("Heart rate data generated and saved to 'heart_rate_data.txt'.")
