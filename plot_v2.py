import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load data from CSV file
filename = "voltage_freq.txt"
df = pd.read_csv(filename)
print(df.columns.tolist())

# Extract values
voltages = df["Voltage"]
scan_1 = df[" Scan_1_Peak_Freq"]
scan_2 = df[" Scan_2_Peak_Freq"]
scan_3 = df[" Scan_3_Peak_Freq"]

# Plot each scan as a separate line
plt.figure(figsize=(8, 5))
plt.plot(voltages, scan_1, marker='o', linestyle='-', label="Scan 1")
plt.plot(voltages, scan_2, marker='s', linestyle='--', label="Scan 2")
plt.plot(voltages, scan_3, marker='^', linestyle='-.', label="Scan 3")

# Customize the plot
plt.xlabel("Voltage (V)")
plt.ylabel("Peak Frequency (Hz)")
plt.title("Voltage vs Peak Frequency for 3 Scans")
plt.legend()
plt.grid(True)

# Show the plot
plt.show()