import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the data from the file
file_path = "data0317.txt"  # Replace with the actual path if needed
data = pd.read_csv(file_path, sep="\t")

# # double frequency
# data['frequency'] *= 2

# Convert data to a matrix (NumPy array)
matrix = data.to_numpy()

# Plot the data
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(projection='3d')

# Scatter plot in 3D
# x: motor position; y: frequency; z: voltage; color represents the voltage values
ax.scatter(matrix[:, 0], matrix[:, 1], matrix[:, 2], c=matrix[:, 2], cmap='viridis', marker='o')

# Labels and title
ax.set_xlabel("Motor Position")
ax.set_ylabel("Frequency")
ax.set_zlabel("Voltage")
ax.set_title("3D Scatter Plot of Motor Position, Frequency, and Voltage")

plt.show()

