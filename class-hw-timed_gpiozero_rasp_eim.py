import os
import sys
import signal
import threading
import numpy as np
import busio
import board
import adafruit_adxl34x
from gpiozero import Button, PWMOutputDevice
import edge_impulse_linux

# Variables
num_of_samples = 0
data = []
done_collecting = threading.Event()

# Accelerometer setup
i2c = busio.I2C(board.SCL, board.SDA)
accelerometer = adafruit_adxl34x.ADXL345(i2c)

# GPIO setup
button = Button(16, pull_up=True)
pwm = PWMOutputDevice(18)

def data_acq_callback():
    global num_of_samples
    global data

    if not done_collecting.is_set():
        accel = accelerometer.acceleration
        data.extend(accel)
        num_of_samples += 1

    if num_of_samples == 100:  # Adjust as per the model's expected input length
        done_collecting.set()
        num_of_samples = 0

def signal_handler(sig, frame):
    print('Interrupted')
    pwm.off()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def help():
    print('python3 claa-hw-time.py <path-to-eim-model.eim>')

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "h", ["--help"])
    except getopt.GetoptError:
        help()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            help()
            sys.exit()

    if len(args) != 1:
        help()
        sys.exit(2)

    model_path = args[0]

    pwm.value = 0.5  # Start PWM with 50% duty cycle
    done_collecting.wait()
    pwm.off()

    # Convert data to numpy array and reshape to match the model's expected input shape
    input_data = np.array(data, dtype=np.float32).reshape(1, -1)  # Adjust shape as necessary

    # Load and run the Edge Impulse model
    model = edge_impulse_linux.InferenceRunner(model_path)
    result = model.run(input_data)

    # Process and print the results
    print(result)
    for index, value in enumerate(result['result']['classification']):
        print(f"{result['result']['classification'][index]['label']}: {value['value']}")

if __name__ == '__main__':
    button.when_pressed = data_acq_callback
    main(sys.argv[1:])
