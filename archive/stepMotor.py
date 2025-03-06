import time
from time import sleep
import RPi.GPIO as GPIO
# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

def write_to_file(filename, distance, voltage):
    fileObject = open(filename, "a")
    fileObject.write(str(distance))
    fileObject.write('\t')
    fileObject.write(str(voltage))
    fileObject.write('\n')
    fileObject.flush()

# Software SPI configuration:
CLK  = 17
MISO = 27
MOSI = 22
CS   = 26
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

# postion get
file_path = 'position.txt'
with open(file_path, 'r') as file:
    for line in file:
        POSITION = int(line)
print("Current position of Stepper Motor is: ", POSITION)

GPIO.setmode(GPIO.BCM)

# variables setup
direction = input("Please enter direction(0 flase/1 true): ")
direction = int(direction)
distance = input("Please enter the distance you want to move(mm): ")
distance = int(distance)

if (direction == 1):
    UPDATED_POSITON = POSITION + distance
    if (UPDATED_POSITON>200):
        print("Invalid Input - Can not move that far!")
        exit()
if (direction == 0):
    UPDATED_POSITON = POSITION - distance
    if (UPDATED_POSITON < 0):
        print("Invalid Input - Can not move that far!")
        exit()

# pin define
pulsePin = 23
directionPin = 24
GPIO.setup(pulsePin, GPIO.OUT)
GPIO.setup(directionPin, GPIO.OUT)

# calculation
PULSES_EACH_ROUND = 200 # user setup
DISTANCE_EACH_ROUND = 5 # 5mm - user measure manually
DISTANCE_EACH_PULSE = DISTANCE_EACH_ROUND / PULSES_EACH_ROUND
total_number_pulses = (distance/DISTANCE_EACH_ROUND) * PULSES_EACH_ROUND
SLEEP_TIME = 0.005

filename = "data.txt"

pulse_count = 0
vol_count = 0
try:
    if direction == 1:
        GPIO.output(directionPin, True)
    else:
        GPIO.output(directionPin, False)

    while pulse_count < total_number_pulses:
        GPIO.output(pulsePin, True)
        sleep(SLEEP_TIME)
        GPIO.output(pulsePin, False)
        sleep(SLEEP_TIME)
        pulse_count += 1
        vol_count += 1
        if vol_count == 20:  # move 0.5mm
            vol_count = 0
            # take voltage
            # sleep(SLEEP_TIME)
            voltage = mcp.read_adc(0)
            move_distance = pulse_count * DISTANCE_EACH_PULSE 
            write_to_file(filename, move_distance, voltage)

        
    # write the updated position into the file
    with open(file_path, 'w') as file:
        file.write(f"{UPDATED_POSITON}")
        

finally:
    GPIO.cleanup()


