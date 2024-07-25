import time
import board
import busio
import adafruit_adxl34x
import os
import pandas as pd
import sys
from gpiozero import Button, PWMOutputDevice
import threading

# Initialize global variables
num_of_samples = 0
data = []
previous_time = 0
accumulated_time = 0
number_of_files = 0

print("Initializing I2C and accelerometer...")

# Configure I2C and accelerometer
i2c = busio.I2C(board.SCL, board.SDA)
accelerometer = adafruit_adxl34x.ADXL345(i2c)
print("Accelerometer initialized.")

# Initialize button and PWM output
print("Initializing button and PWM output...")
button = Button(16, pull_up=True)
pwm = PWMOutputDevice(18, frequency=100)
print("Button and PWM output initialized.")

def data_acq_callback():
    global num_of_samples
    global data
    global previous_time
    global accumulated_time

    print("Button pressed; collecting data...")

    if not done_collecting.is_set():
        accel = accelerometer.acceleration
        if num_of_samples == 0:
            ts = 0
            accumulated_time = ts
            previous_time = 0
        else:
            current_time = previous_time + 10
            ts = (current_time - previous_time)
            accumulated_time = accumulated_time + ts
            previous_time = current_time 

        data_dict = {'timestamp': accumulated_time, 'accX': accel[0], 'accY': accel[1], 'accZ': accel[2]}
        data.append(data_dict)

        num_of_samples += 1
        print(f"Sample {num_of_samples}: {data_dict}")

    if num_of_samples == 100:
        print("100 samples collected; setting done_collecting event.")
        done_collecting.set()
        num_of_samples = 0

if __name__ == '__main__':
    done_collecting = threading.Event()
    done_collecting.clear()
    button.when_pressed = data_acq_callback

    print("Entering main loop...")

    while number_of_files != 300:
        print("Setting PWM value to 0.5")
        pwm.value = 0.5

        # Wait for data collection to finish
        print("Waiting for data collection to finish...")
        done_collecting.wait()
        print("Data collection finished.")

        # Turn off PWM
        pwm.off()
        print("PWM turned off.")

        # Find the next available file number
        i = 0
        while os.path.exists(f'tape_one_side_202310130706_a/tape_one_side.{i}.csv'):
            i += 1
        print(f"Saving data to file: tape_one_side_202310130706_a/tape_one_side.{i}.csv")

        # Write data to file
        with open(f'tape_one_side_202310130706_a/tape_one_side.{i}.csv', "w") as f:
            df = pd.DataFrame(data)
            df.to_csv(f, index=False, header=True)
            f.write("\n")

        print(f"Data written to tape_one_side.{i}.csv")

        # Reset data for next collection
        data = []
        number_of_files += 1
        print(f"File number {number_of_files} completed.")

    # End of script
    print("Completed 300 files. Turning off PWM and exiting.")
    pwm.off()
    sys.exit(0)
