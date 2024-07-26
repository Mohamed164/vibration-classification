import os
import sys
import signal
import time
import io
import threading
import getopt
import numpy as np
import busio
import board
import adafruit_adxl34x
import tflite_runtime.interpreter as tflite
from gpiozero import Button, PWMOutputDevice
import scipy

# Variables
num_of_samples = 0
data = []
previous_time = 0
accumulated_time = 0
done_collecting = threading.Event()

# Accelerometer setup
i2c = busio.I2C(board.SCL, board.SDA)
accelerometer = adafruit_adxl34x.ADXL345(i2c)

# GPIO setup
button = Button(16, pull_up=True)
pwm = PWMOutputDevice(18)

def tflite_model_inference(model_path, input_data):
    # Load the TFLite model
    interpreter = tflite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()

    # Get input and output tensors
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # Check the input type
    input_dtype = input_details[0]['dtype']
    
    # Ensure input_data is of the correct type
    if input_dtype == np.float32:
        inputs = input_data.astype(np.float32)
    elif input_dtype == np.uint8:
        scaling_factor = 15 / np.max(input_data)
        inputs = np.uint8(input_data * scaling_factor)
    else:
        raise ValueError(f"Unsupported input data type: {input_dtype}")

    input_shape = input_details[0]['shape']
    inputs = inputs.reshape(input_shape)

    # Set input tensor
    interpreter.set_tensor(input_details[0]['index'], inputs)

    # Perform inference
    interpreter.invoke()

    # Get output tensor
    output_data = interpreter.get_tensor(output_details[0]['index'])
    return output_data

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

        data.append(accel[0])
        data.append(accel[1])
        data.append(accel[2])

        num_of_samples += 1
    
    if num_of_samples == 100:
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
    dir_path = os.path.dirname(os.path.realpath(__file__))
    modelfile = os.path.join(dir_path, model_path)

    pwm.value = 0.5  # Start PWM with 50% duty cycle
    done_collecting.wait()
    pwm.off()

    input_data = np.array(data)

    predictions = tflite_model_inference(modelfile, input_data)

    print(predictions)
    np.set_printoptions(suppress=True, precision=6)
    softmaxed_pred = scipy.special.softmax(predictions)
    print(softmaxed_pred.shape)
    print("centre: ", softmaxed_pred[0][0])
    print("edge: ", softmaxed_pred[0][1])
    print("off: ", softmaxed_pred[0][2])
    print("on: ", softmaxed_pred[0][3])

if __name__ == '__main__':
    button.when_pressed = data_acq_callback
    main(sys.argv[1:])
