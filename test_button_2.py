from gpiozero import DigitalInputDevice
import time

# Set up GPIO 16 as a DigitalInputDevice object with internal pull-up resistor
pin = DigitalInputDevice(16, pull_up=True)

print("Monitoring GPIO 16 for state changes. Press Ctrl+C to exit.")

try:
    # Initial state
    previous_state = pin.value

    while True:
        # Check current state
        current_state = pin.value
        
        # Detect rising edge
        if not previous_state and current_state:
            print("Detected rising edge!")
        
        # Update previous state
        previous_state = current_state
        
        time.sleep(0.1)  # Short delay to reduce CPU usage

except KeyboardInterrupt:
    print("Script interrupted by user.")
