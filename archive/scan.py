import board
import busio
import adafruit_mcp4725
from tinySA import tinySA
import numpy as np
import time

def write_to_file(filename, voltage, frequency):
    fileObject = open(filename, "a")
    fileObject.write(str(voltage))
    fileObject.write('\t')
    fileObject.write(str(frequency))
    fileObject.write('\n')
    fileObject.flush()

# Function to set DAC voltage (0V to 4.5V)
def set_voltage(voltage):
    if voltage < 0 or voltage > 3.3:
        print("Voltage out of range (0-4.5V)")
        return

    max_dac_value = 4095  # 12-bit DAC (0-4095)
    vcc = 3.3  # Set VCC to 4.5V
    dac_value = int((voltage / vcc) * max_dac_value)
    print(f"dac value: {dac_value}")

    dac.raw_value = dac_value  # Set DAC output
    print(f"Setting Voltage: {voltage}V")


# Create I2C bus
i2c = busio.I2C(board.SCL, board.SDA)
# Initialize MCP4725 DAC
dac = adafruit_mcp4725.MCP4725(i2c)
# spectrum analyzer
analyzer = tinySA()

filename = 'voltage_freq.txt'

start_voltage = 0
stop_voltage = 3.3
step_size = 0.1

voltage = start_voltage
while voltage <= stop_voltage:
    set_voltage(voltage)
    time.sleep(3)
    peak_freq = analyzer.marker_value_freq()
    write_to_file(filename, voltage, peak_freq)
    voltage += step_size    
