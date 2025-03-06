import time
from time import sleep
import RPi.GPIO as GPIO

class StepperMotor:
    """Class to control a stepper motor with GPIO on a Raspberry Pi."""

    def __init__(self, pulse_pin=23, direction_pin=24, position_file="position.txt", max_position=200):
        self.pulse_pin = pulse_pin
        self.direction_pin = direction_pin
        self.position_file = position_file
        self.max_position = max_position

        # Stepper motor movement parameters
        self.pulses_per_rev = 200  # User-defined
        self.distance_per_rev = 5   # 5mm per revolution
        self.distance_per_pulse = self.distance_per_rev / self.pulses_per_rev
        self.sleep_time = 0.01  # Delay per step

        # Setup GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pulse_pin, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.direction_pin, GPIO.OUT, initial=GPIO.LOW)

    def read_position(self):
        """Reads the stepper motor position from a file."""
        try:
            with open(self.position_file, 'r') as file:
                return int(file.read().strip())
        except (FileNotFoundError, ValueError):
            print("Error reading position file. Defaulting to 0.")
            return 0

    def write_position(self, position):
        """Writes the updated stepper motor position to file."""
        with open(self.position_file, 'w') as file:
            file.write(str(position))

    def move(self, direction, distance):
        """Moves the stepper motor a specified distance in a given direction."""
        position = self.read_position()
        updated_position = position + distance if direction == 1 else position - distance

        # Validate position bounds
        if not (0 <= updated_position <= self.max_position):
            print("Invalid Input - Movement out of bounds!")
            return

        # Set direction
        GPIO.output(self.direction_pin, direction)

        pulse_count = 0
        total_pulses = int(distance / self.distance_per_pulse)

        try:
            for _ in range(total_pulses):
                GPIO.output(self.pulse_pin, True)
                time.sleep(self.sleep_time)
                GPIO.output(self.pulse_pin, False)
                time.sleep(self.sleep_time)
                pulse_count += 1

            # Update position *only if the loop completes successfully*
            self.write_position(updated_position)
            print(f"Movement complete. New position: {updated_position} mm")

        except KeyboardInterrupt:
            print("\nMovement interrupted. Position may not be accurate.")

    def cleanup(self):
        """Cleans up GPIO pins when finished."""
        GPIO.cleanup()


# Main script for user interaction
if __name__ == "__main__":
    motor = StepperMotor()

    print(f"Current position of Stepper Motor: {motor.read_position()} mm")

    try:
        direction = int(input("Enter direction (-1: foward with less space, 1: backford with more space): "))
        distance = int(input("Enter movement distance (mm): "))
        motor.move(direction, distance)
    except KeyboardInterrupt:
        print("\nProcess interrupted.")
    finally:
        motor.cleanup()
