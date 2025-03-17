import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load data from CSV file
filename = "data0314.txt"
df = pd.read_csv(filename, delimiter="\t")
print(df.columns.tolist())

# Extract values
voltages = df["voltage"]
motor_position = df["motor_position"]


# Plot the data
plt.figure(figsize=(10, 5))
plt.plot(df["motor_position"], df["voltage"], marker='o', linestyle='-', label="Voltage vs Motor Position")

# Labels and title
plt.xlabel("Motor Position (mm)")
plt.ylabel("Voltage (V)")
plt.title("Voltage vs Motor Position")
plt.legend()
plt.grid(True)

# Show the plot
plt.show()
