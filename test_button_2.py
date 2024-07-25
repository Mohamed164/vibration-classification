from gpiozero import DigitalInputDevice
import time

# Define GPIO 16 as a DigitalInputDevice object with internal pull-up resistor
pin = DigitalInputDevice(16, pull_up=True)

def detect_rising_edge():
    # Check for a rising edge
    if pin.value:
        print("Detected rising edge!")
    else:
        print("Pin is low.")

print("Monitoring GPIO 16 for state changes. Press Ctrl+C to exit.")

try:
    # Initial state
    previous_state = pin.value

    while True:
        # Check current state
        current_state = pin.value
        
        # Detect rising edge
        if not previous_state and current_state:
            detect_rising_edge()
        
        # Update previous state
        previous_state = current_state
        
        time.sleep(0.1)  # Short delay to reduce CPU usage

except KeyboardInterrupt:
    print("Script interrupted by user.")
