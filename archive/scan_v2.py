import board
import busio
import adafruit_mcp4725
from tinySA import tinySA
import numpy as np
import time

def write_to_file(filename, data):
    with open(filename, "w") as file:
        # write header
        file.write("Voltage, Scan_1_Peak_Freq, Scan_2_Peak_Freq, Scan_3_Peak_Freq\n")
        # write data
        for row in data:
            file.write(",".join(map(str, row))+"\n")

# Function to set DAC voltage (0V to 3.3V)
def set_voltage(voltage):
    if voltage < 0 or voltage > 3.3:
        print("Voltage out of range (0-3.3V)")
        return

    max_dac_value = 4095  # 12-bit DAC (0-4095)
    vcc = 3.3  # Set VCC to 4.5V
    dac_value = int((voltage / vcc) * max_dac_value)
    dac.raw_value = dac_value  # Set DAC output
    print(f"Setting Voltage: {voltage}V")


# Create I2C bus and DAC
i2c = busio.I2C(board.SCL, board.SDA)
dac = adafruit_mcp4725.MCP4725(i2c)
# spectrum analyzer
analyzer = tinySA()

filename = 'voltage_freq.txt'

# Scan parameters
start_voltage = 0
stop_voltage = 3.3
step_size = 0.1
num_of_scans = 3

# Prepare a list of voltages for scanning
voltages = [round(start_voltage + i * step_size, 2) for i in range(int((stop_voltage - start_voltage) / step_size) + 1)]
scan_data = {v: [] for v in voltages}  # Dictionary to store results per voltage


# Perform 3 full scans
for scan_num in range(num_of_scans):
    print(f"Starting Scan {scan_num + 1}...")
    
    for voltage in voltages:
        set_voltage(voltage)
        time.sleep(3)  # Stabilization delay

        peak_freq = analyzer.marker_value_freq()
        scan_data[voltage].append(peak_freq)
        time.sleep(1)  # Small delay between scans

# Convert dictionary to a list format
formatted_data = [[voltage] + scan_data[voltage] for voltage in voltages]

# Write the formatted data to file
write_to_file(filename, formatted_data)

print(f"Scanning complete. Results saved to {filename}.")
