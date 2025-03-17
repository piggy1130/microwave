import numpy as np
import pandas as pd
import time
from DAC import DACController
from spectrumAnalyzer import spectrumAnalyzer
from stepperMotor import StepperMotor
from ADC import ADCController

# device setup
dac = DACController() # default voltage is 3.3v 12-bit DAC
analyzer = spectrumAnalyzer()
adc = ADCController()
motor = StepperMotor()

# how to change frequency - change voltage -> change frequcny (up section)
# frequency range is 2.30 - 2.50
def get_polynomial_equation(x, y, degree):
    coeffs = np.polyfit(x, y, degree)
    poly = np.poly1d(coeffs)
    return poly

# get function
filename = "voltage_freq_0314.txt"
df = pd.read_csv(filename)
voltages = df["Voltage"] # y-axis
scan_1_freq = df[" Scan_1_Peak_Freq"]/1e9 # x-axis
poly_function = get_polynomial_equation(scan_1_freq, voltages, 6)
# # get the voltage we need to set to get the frequency we want
# voltage_required = poly_function(2.4)
# print(voltage_required)

# start the Stepper Motor scan
direction = input("Direction (-1 forward with less pace / 1 backford with more space): ")
direction = int(direction)
distance = input("Distance you want to move(mm): ")
distance = int(distance)
motor_final_position = motor.validate_move(direction, distance)

step_size = 0.1 # unit is mm
# file to record data
filename = "data0317.txt"
with open(filename, 'w') as f:
    # Write the header
    f.write("motor_position\tfrequency\tvoltage\n")
    if (direction == 1):
        while motor.current_position < motor_final_position:
            motor.move(direction, step_size)
            time.sleep(0.5)
            # get frequency range we wanted 
            for i in np.arange (2.3, 2.5, 0.01):
                voltage_required = poly_function(i)
                # set voltage to get the expected frequency
                dac.set_voltage(voltage_required)
                time.sleep(0.1)  # Stabilization delay               
                # read the voltage from ADC
                adc_voltage = adc.get_voltage()
                f.write(f"{motor.current_position}\t{i}\t{adc_voltage:.3f}\n")
                #print(f"position is {motor.current_position}, frequncy is {i} and voltage is: {adc_voltage:.3f}")  
            print(f"position is {motor.current_position}")
    if (direction == -1):
        while motor.current_position > motor_final_position:
            motor.move(direction, step_size)
            time.sleep(0.5)
            for i in np.arange (2.3, 2.5, 0.01):
                voltage_required = poly_function(i)
                # set voltage to get the expected frequency
                dac.set_voltage(voltage_required)
                time.sleep(0.1)  # Stabilization delay               
                # read the voltage from ADC            
                adc_voltage = adc.get_voltage()
                f.write(f"{motor.current_position}\t{i}\t{adc_voltage:.3f}\n")
                #print(f"position is {motor.current_position}, frequncy is {i} and voltage is: {adc_voltage:.3f}")  
            print(f"position is {motor.current_position}")

# write motor position to the file
motor.write_position(motor.current_position)
motor.cleanup()






