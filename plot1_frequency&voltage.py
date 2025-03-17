import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load data from CSV file
filename = "voltage_freq_0314.txt"
df = pd.read_csv(filename)
print(df.columns.tolist())

# Extract values
voltages = df["Voltage"]
scan_1 = df[" Scan_1_Peak_Freq"]
scan_2 = df[" Scan_2_Peak_Freq"]
scan_3 = df[" Scan_3_Peak_Freq"]

# Plot each scan with frequency as x-axis and voltage as y-axis
plt.figure(figsize=(8, 5))
plt.plot(scan_1, voltages, marker='o', linestyle='-', label="Scan 1")
plt.plot(scan_2, voltages, marker='s', linestyle='--', label="Scan 2")
plt.plot(scan_3, voltages, marker='^', linestyle='-.', label="Scan 3")

# Customize the plot
plt.xlabel("Peak Frequency (Hz)")
plt.ylabel("Voltage (V)")
plt.title("Peak Frequency vs Voltage for 3 Scans")
plt.legend()
plt.grid(True)

# Show the plot
plt.show()
