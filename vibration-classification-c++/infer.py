import time
import board
import busio
import adafruit_adxl34x
import os
import sys
import subprocess
from gpiozero import Button, PWMLED
import threading

num_of_samples = 0
data = []
previous_time = 0
accumulated_time = 0

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

        # Save only the accelerometer data (X, Y, Z)
        data.append(accel)
        num_of_samples += 1
    
    if num_of_samples == 100:
        done_collecting.set()
        num_of_samples = 0

def launch_inference():
    # Flatten the data to pass it as command-line arguments
    input_args = []
    for sample in data:
        input_args.extend([str(sample[0]), str(sample[1]), str(sample[2])])
    
    # Command to launch the C++ program with the input buffer
    command = ["./main"] + input_args
    
    # Run the C++ inference program
    subprocess.run(command)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Error: The 'path' argument is required.")
        sys.exit(1)
    
    path = sys.argv[1]
    
    done_collecting = threading.Event()
    done_collecting.clear()

    button.when_pressed = data_acq_callback
    
    while True:   
        led.value = 0.5  # Start LED PWM at 50%
        # Wait for data collection to finish
        done_collecting.wait()
        led.value = 0  # Stop LED PWM
        done_collecting.clear()

        # Launch the inference with the acquired data
        launch_inference()

        # Clear the data buffer for the next collection
        data = []

    led.value = 0  # Ensure LED is turned off
    sys.exit(0)
