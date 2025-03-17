import numpy as np
import pandas as pd
import time
from stepperMotor import StepperMotor
from ADC import ADCController

# def get_polynomial_equation(x, y, degree):
#     coeffs = np.polyfit(x, y, degree)
#     poly = np.poly1d(coeffs)
#     return poly

# # get function
# filename = "voltage_freq.txt"
# df = pd.read_csv(filename)
# voltages = df["Voltage"] # y-axis
# scan_1 = df[" Scan_1_Peak_Freq"]/1e9 # x-axis

# poly_function = get_polynomial_equation(scan_1, voltages, 6)
# voltage_required = poly_function(2.4)
# print(voltage_required)

motor = StepperMotor()
adc = ADCController()
print(f"Current position of Stepper Motor: {motor.current_position} mm")
filename = "data0314.txt"
with open(filename, "w") as f:
    f.write("motor_position\tvoltage\n")

direction = input("Direction (-1 forward with less pace / 1 backford with more space): ")
direction = int(direction)
distance = input("Distance you want to move(mm): ")
distance = int(distance)
motor_final_position = motor.validate_move(direction, distance)

step_size = 0.1 # unit is mm

with open(filename, 'w') as f:
    # Write the header
    f.write("motor_position\tvoltage\n")  
    if (direction == 1):
        while motor.current_position < motor_final_position:
            motor.move(direction, step_size)
            time.sleep(0.5)
            adc_voltage = adc.get_voltage()
            f.write(f"{motor.current_position}\t{adc_voltage:.3f}\n")
            print(f"position is {motor.current_position} and voltage is: {adc_voltage:.3f}")  
    if (direction == -1):
        while motor.current_position > motor_final_position:
            motor.move(direction, step_size)
            time.sleep(0.5)
            adc_voltage = adc.get_voltage()
            f.write(f"{motor.current_position}\t{adc_voltage:.3f}\n")
            print(f"position is {motor.current_position} and voltage is: {adc_voltage:.3f}")  

motor.write_position(motor.current_position)
motor.cleanup()
