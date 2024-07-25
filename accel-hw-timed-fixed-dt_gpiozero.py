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
    else:
        print(f"Samples collected: {num_of_samples}")

if __name__ == '__main__':
    done_collecting = threading.Event()
    done_collecting.clear()

    GPIO.add_event_detect(16, GPIO.RISING, 
        callback=data_acq_callback, bouncetime=10)
        
    while number_of_files != 300:   
        p.start(50)
        #wait for data collection to finish
        done_collecting.wait()
        p.stop()
        done_collecting.clear()

        #write to a file
        i = 0
        while os.path.exists(r'tape_one_side_202310130706_a/tape_one_side.%s.csv' % i):
            i = i + 1

        with open(r'tape_one_side_202310130706_a/tape_one_side.%s.csv' % i, "w") as f:
            df = pd.DataFrame(data)
            df.to_csv(f, index=False, header=True)
            f.write("\n")

        data = []       
        number_of_files = number_of_files + 1

    p.stop()
    GPIO.cleanup()
    sys.exit(0)