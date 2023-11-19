import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import messagebox
import time
import threading

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

# Plot heart rate data in a 2D graph
def plot_heart_rate_data(time, driver_data, passenger_data, fig, axs):
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

    # Create a third graph to show data where both bpms are higher
    both_high = np.where((driver_data > threshold) & (passenger_data > threshold))
    axs[1, 0].plot(time[both_high], driver_data[both_high], 'ro', label='High BPM (Driver)')
    axs[1, 0].plot(time[both_high], passenger_data[both_high], 'go', label='High BPM (Passenger)')
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
    plt.draw()


    class HeartRateMonitorApp:
        def __init__(self, root):
            self.root = root
            self.root.title("Heart Rate Monitor")
            self.root.protocol("WM_DELETE_WINDOW", self.on_close)

            self.driver_contacted = False
            self.passenger_contacted = False
            self.response_unit_contacted = False

            self.create_gui()

            # Create a queue to communicate between the main thread and the plotting thread
            self.plot_queue = queue.Queue()

            # Start the plotting thread
            self.plot_thread = threading.Thread(target=self.plot_heart_rate_data)
            self.plot_thread.start()

        def create_gui(self):
            self.control_label = tk.Label(self.root, text="Control Status", font=("Helvetica", 16))
            self.control_label.grid(row=0, column=0, pady=10)

            self.danger_label = tk.Label(self.root, text="Danger Factors", font=("Helvetica", 16))
            self.danger_label.grid(row=0, column=1, pady=10)

            self.driver_button = tk.Button(self.root, text="Contact Driver", command=self.contact_driver)
            self.driver_button.grid(row=1, column=0, pady=10)

            self.passenger_button = tk.Button(self.root, text="Contact Passenger", command=self.contact_passenger)
            self.passenger_button.grid(row=2, column=0, pady=10)

            self.response_unit_button = tk.Button(self.root, text="Contact Response Unit", command=self.contact_response_unit)
            self.response_unit_button.grid(row=3, column=0, pady=10)

            self.status_control = tk.Label(self.root, text="Control: OK", font=("Helvetica", 12), fg="green")
            self.status_control.grid(row=1, column=1)

            self.status_danger = tk.Label(self.root, text="Danger: OK", font=("Helvetica", 12), fg="green")
            self.status_danger.grid(row=2, column=1)

            self.status_driver = tk.Label(self.root, text="Driver: Not Contacted", font=("Helvetica", 12), fg="orange")
            self.status_driver.grid(row=4, column=0, pady=10)

            self.status_passenger = tk.Label(self.root, text="Passenger: Not Contacted", font=("Helvetica", 12), fg="orange")
            self.status_passenger.grid(row=5, column=0, pady=10)

            self.status_response_unit = tk.Label(self.root, text="Response Unit: Not Contacted", font=("Helvetica", 12), fg="orange")
            self.status_response_unit.grid(row=6, column=0, pady=10)

        def contact_driver(self):
            if not self.driver_contacted:
                self.driver_contacted = True
                self.status_driver.config(text="Driver: Contacted", fg="green")

        def contact_passenger(self):
            if not self.passenger_contacted:
                self.passenger_contacted = True
                self.status_passenger.config(text="Passenger: Contacted", fg="green")

        def contact_response_unit(self):
            if not self.response_unit_contacted:
                self.response_unit_contacted = True
                self.status_response_unit.config(text="Response Unit: Contacted", fg="green")

        def on_close(self):
            self.plot_thread.join()
            self.root.destroy()

        def check_anxious_heart_rate(self):
            driver_max = np.max(self.driver_data)
            passenger_max = np.max(self.passenger_data)

            if driver_max > threshold:
                self.status_control.config(text="Control: Danger", fg="red")
                self.status_danger.config(text="Danger: Driver's heart rate is high", fg="red")
                # Add a message to the queue to update the plot with the anxious heart rate
                self.plot_queue.put("Driver's heart rate is high")

            elif passenger_max > threshold:
                self.status_control.config(text="Control: Danger", fg="red")
                self.status_danger.config(text="Danger: Passenger's heart rate is high", fg="red")
                # Add a message to the queue to update the plot with the anxious heart rate
                self.plot_queue.put("Passenger's heart rate is high")

            else:
                self.status_control.config(text="Control: OK", fg="green")
                self.status_danger.config(text="Danger: OK", fg="green")
                # Add a message to the queue to update the plot with the normal heart rate
                self.plot_queue.put("Normal heart rate")

        def plot_heart_rate_data(self):
            while True:
                # Get the next message from the queue
                message = self.plot_queue.get()

                # Update the plot with the message 
                if message == "Driver's heart rate is high":
                    self.axs[0, 0].axhline(y=140, color='r', linestyle='--', label='Anxious threshold BPM')

                elif message == "Passenger's heart rate is high":
                    self.axs[0, 1].axhline(y=140, color='r', linestyle='--', label='Anxious threshold BPM')

                elif message == "Normal heart rate":
                    self.axs[0, 0].clear()
                    self.axs[0, 1].clear()

                # Redraw the plot
                plt.draw()

                # Wait for 1 second before updating the plot again
                time.sleep(60)


def main():
    # Enable Matplotlib interactive mode
    plt.ion()

    # Read heart rate data from file
    heart_rate_data = read_heart_rate_data()

    # Extract driver and passenger data
    time_array = np.arange(0, len(heart_rate_data))
    driver_data = heart_rate_data[:, 0]
    passenger_data = heart_rate_data[:, 1]

    # Create a threading event to signal the plot thread to update
    event = threading.Event()

    # Create the initial Matplotlib plot
    fig, axs = plt.subplots(2, 2, figsize=(10, 6))

    # Start a thread to run the plot function
    plot_thread = threading.Thread(target=plot_heart_rate_data, args=(time_array, driver_data, passenger_data, fig, axs))
    plot_thread.start()

    # Start the main loop
    while True:
        # Check for an anxious heart rate and prompt driver and passenger
        check_anxious_heart_rate(driver_data, passenger_data)

        # Append new heart rate data to the arrays
        new_heart_rate_data = read_heart_rate_data()
        time_array = np.append(time_array, new_heart_rate_data[:, 0])
        driver_data = np.append(driver_data, new_heart_rate_data[:, 1])
        passenger_data = np.append(passenger_data, new_heart_rate_data[:, 1])  # Use index 1 for passenger_data

        # Call the Matplotlib plotting function in the main thread
        plot_heart_rate_data(time_array, driver_data, passenger_data, fig, axs)

        # Check if the user has pressed the Enter key to quit
        if input() == '':
            break

    # Wait for the plot thread to finish before exiting
    plot_thread.join()

# Start the GUI application
root = tk.Tk()
root.withdraw()

# Execute the main function
main()