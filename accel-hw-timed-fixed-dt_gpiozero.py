import time
import board
import busio
import adafruit_adxl34x
import os
import pandas as pd
import sys
from gpiozero import Button, PWMOutputDevice
import threading

num_of_samples = 0
data = []
previous_time = 0
accumulated_time = 0
number_of_files = 0

adafruit_adxl34x.DataRate.RATE_3200_HZ
i2c = busio.I2C(board.SCL, board.SDA)
accelerometer = adafruit_adxl34x.ADXL345(i2c)

# Use gpiozero for button and LED
button = Button(16, pull_up=True)  # Button on pin 16 with pull-up resistor

led = PWMOutputDevice(18, frequency=100)  # Create PWM output on pin 18 with 100 Hz frequency
# Control the LED's brightness (0.0 to 1.0)
led.value = 0.5  # Set brightness to 50%



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

    num_of_samples = num_of_samples + 1

  if num_of_samples == 100:
    done_collecting.set()
    num_of_samples = 0


if __name__ == '__main__':
  done_collecting = threading.Event()
  done_collecting.clear()

  # Use button.when_pressed instead of GPIO interrupt
  button.when_pressed = data_acq_callback

  while number_of_files != 300:
    led.start(50)  # Start LED blinking
    # wait for data collection to finish
    done_collecting.wait()
    # led.stop()  # Stop LED blinking
    # Stop the PWM output
    led.close()
    done_collecting.clear()

    # write to a file
    i = 0
    while os.path.exists(r'tape_one_side_202310130706_a/tape_one_side.%s.csv' % i):
      i = i + 1

    with open(r'tape_one_side_202310130706_a/tape_one_side.%s.csv' % i, "w") as f:
      df = pd.DataFrame(data)
      df.to_csv(f, index=False, header=True)
      f.write("\n")

    data = []
    number_of_files = number_of_files + 1

  led.close()  # Ensure LED is off at the end
  sys.exit(0)
