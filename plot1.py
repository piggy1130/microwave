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

# Load data from CSV file
filename2 = "voltage_freq_0223.txt"
df2 = pd.read_csv(filename2)
scan_4 = df2[" Scan_1_Peak_Freq"]
scan_5 = df2[" Scan_2_Peak_Freq"]
scan_6 = df2[" Scan_3_Peak_Freq"]


# Plot each scan as a separate line
plt.figure(figsize=(8, 5))
plt.plot(voltages, scan_1, marker='o', linestyle='-', label="Scan 1 0314")
plt.plot(voltages, scan_2, marker='s', linestyle='--', label="Scan 2 0314")
plt.plot(voltages, scan_3, marker='^', linestyle='-.', label="Scan 3 0314")
plt.plot(voltages, scan_4, marker='o', linestyle='-', label="Scan 1 0223")
plt.plot(voltages, scan_5, marker='s', linestyle='--', label="Scan 2 0223")
plt.plot(voltages, scan_6, marker='^', linestyle='-.', label="Scan 3 0223")

# Customize the plot
plt.xlabel("Voltage (V)")
plt.ylabel("Peak Frequency (Hz)")
plt.title("Voltage vs Peak Frequency for 3 Scans")
plt.legend()
plt.grid(True)

# Show the plot
plt.show()