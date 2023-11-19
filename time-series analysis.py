import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import messagebox
import time

threshold = 140  # Set the threshold heart rate for anxiety

# Function to check for an anxious heart rate and prompt driver and passenger
def check_anxious_heart_rate(driver_data, passenger_data):
    driver_max = np.max(driver_data)
    passenger_max = np.max(passenger_data)
    for n in range(1):
        if driver_max > threshold:
            response_driver = messagebox.askyesno("Anxious Heart Rate", "Driver: Are you feeling okay?")
            if not response_driver:
                messagebox.showinfo("Emergency Response", "Emergency response has been notified for the driver.")
        
        if passenger_max > threshold:
            response_passenger = messagebox.askyesno("Anxious Heart Rate", "Passenger: Are you feeling okay?")
            if not response_passenger:
                messagebox.showinfo("Emergency Response", "Emergency response has been notified for the passenger.")

# Read heart rate data from file
def read_heart_rate_data():
    file_name = 'heart_rate_data.txt'
    with open(file_name, 'r') as file:
        next(file)  # Skip the first row (column headers)
        heart_rate_data = np.loadtxt(file, delimiter=',')
    return heart_rate_data

# Apply time-series analysis techniques to heart rate data
def analyze_heart_rate_data(time, driver_data, passenger_data):
    # Perform time-series analysis here
    # Apply moving averages, Fourier Transform(not effective since data is not stationary) try Spectral analysis,
    # Example: Apply spectral analysis using periodogram:
    
    #f_driver, Pxx_driver = periodogram(driver_data)
    #f_passenger, Pxx_passenger = periodogram(passenger_data)    
    
    # Example: Calculate moving averages
    window_size = 10
    driver_data_smooth = np.convolve(driver_data, np.ones(window_size) / window_size, mode='valid')
    passenger_data_smooth = np.convolve(passenger_data, np.ones(window_size) / window_size, mode='valid')
    
    return driver_data_smooth, passenger_data_smooth

# Plot heart rate data in a 2D graph
def plot_heart_rate_data(time, driver_data , passenger_data):
    fig, axs = plt.subplots(2, 2, figsize=(10, 6))
    
    # Plot for the driver's heart rate data
    axs[0, 0].plot(time, driver_data, label='Driver')
    axs[0, 0].set_ylabel('Heart Rate (BPM)')
    axs[0, 0].axhline(y=140, color='r', linestyle='--', label='anxious_threshold BPM')
    axs[0, 0].legend()

    # Plot for the passenger's heart rate data
    axs[0, 1].plot(time, passenger_data, label='Passenger')
    axs[0, 1].set_ylabel('Heart Rate (BPM)')
    axs[0, 1].axhline(y=140, color='r', linestyle='--', label='anxious_threshold BPM')
    axs[0, 1].legend()

    # Apply time-series analysis techniques
    driver_data_smooth, passenger_data_smooth = analyze_heart_rate_data(time, driver_data, passenger_data)

    # Plot the smoothed heart rate data after applying time-series analysis techniques
    window_size = 10  # Define the window size for moving averages
    axs[1, 0].plot(time[window_size - 1:], driver_data_smooth, label='Driver (Smoothed)')
    axs[1, 0].plot(time[window_size - 1:], passenger_data_smooth, label='Passenger (Smoothed)')
    axs[1, 0].set_xlabel('Time (seconds)')
    axs[1, 0].set_ylabel('Heart Rate (BPM)')
    axs[1, 0].axhline(y=140, color='r', linestyle='--', label='anxious_threshold BPM')
    axs[1, 0].legend()

    # Create a fourth graph with combined heart rate data
    axs[1, 1].plot(time, driver_data, label='Driver')
    axs[1, 1].plot(time, passenger_data, label='Passenger')
    axs[1, 1].set_xlabel('Time (seconds)')
    axs[1, 1].set_ylabel('Heart Rate (BPM)')
    axs[1, 1].axhline(y=140, color='r', linestyle='--', label='anxious_threshold BPM')
    axs[1, 1].legend()

    plt.tight_layout()
    plt.show()

# Main function
def main():
    # Read heart rate data from file
    heart_rate_data = read_heart_rate_data()

    # Extract driver and passenger data
    time_array = np.arange(0, len(heart_rate_data))
    driver_data = heart_rate_data[:, 0]
    passenger_data = heart_rate_data[:, 1]

    start_time = time.time()  # Get the current time in seconds
    driver_prompted = False
    passenger_prompted = False
    
    while time.time() - start_time < 60:  # Run for 60 seconds
        # Check for an anxious heart rate and prompt driver and passenger if not already prompted
        if not driver_prompted and np.max(driver_data) > 100:
            check_anxious_heart_rate(driver_data, passenger_data)
            driver_prompted = True
        
        if not passenger_prompted and np.max(passenger_data) > 100:
            check_anxious_heart_rate(driver_data, passenger_data)
            passenger_prompted = True

        # Plot heart rate data in a 2D graph
        plot_heart_rate_data(time_array, driver_data, passenger_data)

        time.sleep(1)  # Wait for 1 second before updating the plot

# Start the GUI application
root = tk.Tk()
root.withdraw()

# Execute the main function
main()