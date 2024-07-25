from gpiozero import DigitalInputDevice
import time

# Set up GPIO 16 as a DigitalInputDevice with internal pull-up resistor
pin = DigitalInputDevice(16, pull_up=True)

print("Monitoring GPIO 16. Press Ctrl+C to exit.")

try:
    while True:
        # Print the current state of the pin
        state = pin.value
        print(f"GPIO 16 state: {'HIGH' if state else 'LOW'}")
        time.sleep(0.5)
except KeyboardInterrupt:
    print("Script interrupted by user.")
