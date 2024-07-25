import time
import board
import busio
import adafruit_adxl34x
from gpiozero import Button
import threading

num_of_samples = 0
data = []
previous_time = 0
accumulated_time = 0

i2c = busio.I2C(board.SCL, board.SDA)
accelerometer = adafruit_adxl34x.ADXL345(i2c)

# Setup GPIO pins
button = Button(16, bounce_time=0.01)

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

        data_dict = {'timestamp': accumulated_time, 'accX': accel[0], 'accY': accel[1], 'accZ': accel[2]}
        data.append(data_dict)

        print(f"Timestamp: {accumulated_time}, X: {accel[0]}, Y: {accel[1]}, Z: {accel[2]}")

        num_of_samples += 1
    
    if num_of_samples == 100:
        done_collecting.set()
        num_of_samples = 0

if __name__ == '__main__':
    done_collecting = threading.Event()
    done_collecting.clear()

    # Set the callback for the button press
    button.when_pressed = data_acq_callback
    
    print("Press the button to start data acquisition.")

    try:
        # Wait for data collection to finish
        done_collecting.wait()
    except KeyboardInterrupt:
        print("Data collection interrupted by user.")

    print("Data collection complete.")
