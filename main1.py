import numpy as np
import time
from DAC import DACController
from spectrumAnalyzer import spectrumAnalyzer

def write_to_file(filename, data):
    with open(filename, "w") as file:
        # write header
        file.write("Voltage, Scan_1_Peak_Freq, Scan_2_Peak_Freq, Scan_3_Peak_Freq\n")
        # write data
        for row in data:
            file.write(",".join(map(str, row))+"\n")

# device setup
dac = DACController() # default voltage is 3.3v 12-bit DAC
analyzer = spectrumAnalyzer()

# Scan parameters
start_voltage = 0
stop_voltage = 3.3
step_size = 0.1

# Prepare a list of voltages for scanning
voltages = []
num_steps = int((stop_voltage - start_voltage) / step_size) + 1 # Calculate the number of steps required
for i in range(num_steps):
    voltage = start_voltage + i * step_size  # Calculate the voltage for the current step
    voltage = round(voltage, 2)  # Round the voltage to 2 decimal places
    voltages.append(voltage)  # Add the voltage to the list

# overall scan data saved in a dictionary
scan_data = {}
for voltage in voltages:
    scan_data[voltage] = [] # Add the voltage as a key with an empty list as the value

# Perform 3 full scans
num_of_scans = 3
for scan_num in range(num_of_scans):
    print(f"Starting Scan {scan_num + 1}...")
    for voltage in voltages:
        dac.set_voltage(voltage)
        time.sleep(3)  # Stabilization delay
        peak_freq = analyzer.get_peak_frequency()
        scan_data[voltage].append(peak_freq)
        time.sleep(1)  # Small delay between scans

# change the dictionary format to save into the file
formatted_data = []
for voltage in voltages:
    row = [voltage] + scan_data[voltage]  # Create a row with voltage followed by scan results
    formatted_data.append(row)

filename = 'voltage_freq_0314.txt'
write_to_file(filename, formatted_data)

print(f"Scanning complete. Results saved to {filename}.")