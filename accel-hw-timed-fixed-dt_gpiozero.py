import time
import board
import busio
import adafruit_adxl34x
import os
import pandas as pd
import sys
from gpiozero import Button, PWMLED
import threading

num_of_samples = 0
data = []
previous_time = 0
accumulated_time = 0
number_of_files = 0

# Initialize the accelerometer
adafruit_adxl34x.DataRate.RATE_3200_HZ
i2c = busio.I2C(board.SCL, board.SDA)
accelerometer = adafruit_adxl34x.ADXL345(i2c)

# Initialize GPIO
button = Button(16, pull_up=True)
led = PWMLED(18)

def data_acq_callback():
    global num_of_samples
    global data
    global previous_time
    global accumulated_time

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

        data_dict = {'timestamp':accumulated_time, 'accX':accel[0], 'accY':accel[1], 'accZ':accel[2]}
        data.append(data_dict)

        num_of_samples += 1
    
    if num_of_samples == 100:
        done_collecting.set()
        num_of_samples = 0

if __name__ == '__main__':
    done_collecting = threading.Event()
    done_collecting.clear()

    button.when_pressed = data_acq_callback
    
    while number_of_files != 300:   
        led.value = 0.5  # Start LED PWM at 50%
        # Wait for data collection to finish
        done_collecting.wait()
        led.value = 0  # Stop LED PWM
        done_collecting.clear()

        # Write to a file
        i = 0
        while os.path.exists(f'output/tape_one_side.{i}.csv'):
            i += 1

        with open(f'output/tape_one_side.{i}.csv', "w") as f:
            df = pd.DataFrame(data)
            df.to_csv(f, index=False, header=True)
            f.write("\n")

        data = []       
        number_of_files += 1

    led.value = 0  # Ensure LED is turned off
    sys.exit(0)
