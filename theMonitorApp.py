import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import threading
import queue

threshold = 140  # Set the threshold heart rate for anxiety
control_threshold = 160  # Set the threshold heart rate for control

class HeartRateMonitorApp:
    def __init__(self, root, data_file):
        self.root = root
        self.root.title("Heart Rate Monitor")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.driver_contacted = False
        self.passenger_contacted = False
        self.response_unit_contacted = False

        self.create_gui()
        self.create_plot()

        # Create a queue to communicate between the main thread and the plotting thread
        self.plot_queue = queue.Queue()

        # Load heart rate data from the file (skip header)
        self.heart_rate_data = np.loadtxt(data_file, delimiter=',', skiprows=1)

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

    def create_plot(self):
        self.fig, self.axs = plt.subplots(1, 2, figsize=(10, 4), tight_layout=True)
        self.axs[0].set_title('Driver Heart Rate')
        self.axs[1].set_title('Passenger Heart Rate')

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=1, column=2, rowspan=6, padx=10)

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

    def plot_heart_rate_data(self):
        while True:
            for heart_rate_entry in self.heart_rate_data:
                driver_heart_rate, passenger_heart_rate = heart_rate_entry

                # Update the plot
                self.axs[0].clear()
                self.axs[0].plot([driver_heart_rate], 'bo-', label='Driver Heart Rate')
                self.axs[0].set_title('Driver Heart Rate')
                self.axs[0].axhline(y=threshold, color='r', linestyle='--', label='Anxious threshold BPM')
                self.axs[0].legend()

                self.axs[1].clear()
                self.axs[1].plot([passenger_heart_rate], 'bo-', label='Passenger Heart Rate')
                self.axs[1].set_title('Passenger Heart Rate')
                self.axs[1].axhline(y=threshold, color='r', linestyle='--', label='Anxious threshold BPM')
                self.axs[1].legend()

                # Check for danger and control thresholds
                if driver_heart_rate > control_threshold or passenger_heart_rate > control_threshold:
                    self.status_control.config(text="Control: High BPM", fg="red")
                else:
                    self.status_control.config(text="Control: OK", fg="green")

                if driver_heart_rate > threshold or passenger_heart_rate > threshold:
                    self.status_danger.config(text="Danger: High BPM", fg="orange")
                else:
                    self.status_danger.config(text="Danger: OK", fg="green")

                # Redraw the canvas
                self.canvas.draw()

                # Wait for a short interval before updating the plot again
                time.sleep(1)

def main():
    data_file = 'heart_rate_data.txt'  # Provide the correct path to your data file
    root = tk.Tk()
    app = HeartRateMonitorApp(root, data_file)
    root.mainloop()

if __name__ == "__main__":
    main()
