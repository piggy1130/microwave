import board
import busio
import adafruit_mcp4725

# Create I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize MCP4725 DAC
dac = adafruit_mcp4725.MCP4725(i2c)

# Function to set DAC voltage (0V to 4.5V)
def set_voltage(voltage):
    if voltage < 0 or voltage > 4.5:
        print("Voltage out of range (0-4.5V)")
        return

    max_dac_value = 4095  # 12-bit DAC (0-4095)
    vcc = 4.5  # Set VCC to 4.5V
    dac_value = int((voltage / vcc) * max_dac_value)

    dac.value = dac_value  # Set DAC output
    print(f"Setting Voltage: {voltage}V")

# Example: Sweep voltage from 0V to 4.5V
import time
# for v in range(0, 46):  # 0V to 4.5V in 0.1V steps
#     set_voltage(v / 10.0)
#     print(f"Setting Voltage: {v/10.0}V")
#     time.sleep(0.5)  # Wait 0.5 seconds
set_voltage(3)
