import numpy as np
import pandas as pd
import time
from DAC import DACController
from spectrumAnalyzer import spectrumAnalyzer
from stepperMotor import StepperMotor
from ADC import ADCController

# Constants
FREQ_RANGE = np.arange(2.3, 2.5, 0.01)  # Frequency range in GHz
MOTOR_STEP_SIZE = 1  # Stepper motor step size in mm
FILENAME_VOLTAGE_FREQ = "voltage_freq_0314.txt"
FILENAME_DATA = "data0318_3dprinting_coating.txt"

# device setup
dac = DACController() # default voltage is 3.3v 12-bit DAC
analyzer = spectrumAnalyzer()
adc = ADCController()
motor = StepperMotor()

# how to change frequency - change voltage -> change frequcny (up section)
def get_polynomial_equation(x, y, degree=6):
    coeffs = np.polyfit(x, y, degree)
    poly = np.poly1d(coeffs)
    return poly

def load_voltage_frequency_data(filename):
    df = pd.read_csv(filename)
    voltages = df["Voltage"]  # y-axis
    scan_freq = df[" Scan_1_Peak_Freq"] / 1e9  # x-axis (convert Hz to GHz)
    return get_polynomial_equation(scan_freq, voltages)

def move_motor_and_record_data(direction, distance, poly_function, filename):
    motor_final_position = motor.validate_move(direction, distance)
    
    with open(filename, 'w') as f:
        f.write("motor_position\tfrequency\tvoltage\n")

        if direction == 1:
            while motor.current_position < motor_final_position:
                motor.move(direction, MOTOR_STEP_SIZE)
                time.sleep(0.5)
                
                for freq in FREQ_RANGE:
                    voltage_required = poly_function(freq)
                    dac.set_voltage(voltage_required)
                    time.sleep(0.1)  # Stabilization delay
                    adc_voltage = adc.get_voltage()
                    f.write(f"{motor.current_position}\t{freq}\t{adc_voltage:.3f}\n")
                
                print(f"Motor position: {motor.current_position}")
        
        elif direction == -1:
            while motor.current_position > motor_final_position:
                motor.move(direction, MOTOR_STEP_SIZE)
                time.sleep(0.5)
                
                for freq in FREQ_RANGE:
                    voltage_required = poly_function(freq)
                    dac.set_voltage(voltage_required)
                    time.sleep(0.1)  # Stabilization delay
                    adc_voltage = adc.get_voltage()
                    f.write(f"{motor.current_position}\t{freq}\t{adc_voltage:.3f}\n")
                
                print(f"Motor position: {motor.current_position}")

    # Save final motor position
    motor.write_position(int(motor.current_position))
    motor.cleanup()

if __name__ == "__main__":
    # Load voltage-frequency polynomial function
    poly_function = load_voltage_frequency_data(FILENAME_VOLTAGE_FREQ)
    
    # Get user input for motor movement
    direction = int(input("Direction (-1: forward with less pace / 1: backward with more space): "))
    distance = int(input("Distance to move (mm): "))
    
    # Start motor scan and data recording
    move_motor_and_record_data(direction, distance, poly_function, FILENAME_DATA)

