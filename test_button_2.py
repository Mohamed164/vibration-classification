from gpiozero import PWMOutputDevice, DigitalInputDevice
import time

# Set up GPIO 16 as DigitalInputDevice with internal pull-up resistor
pin_input = DigitalInputDevice(16, pull_up=True)

# Set up GPIO 18 as PWMOutputDevice
pwm_output = PWMOutputDevice(18)

# Function to detect rising edge
def detect_rising_edge():
    print("Detected rising edge on GPIO 16!")

print("Generating PWM on GPIO 18 and monitoring GPIO 16 for rising edges. Press Ctrl+C to exit.")

try:
    # Initialize previous state
    previous_state = pin_input.value
    
    # Start PWM signal with 50% duty cycle
    pwm_output.value = 0.5
    
    while True:
        # Check current state of GPIO 16
        current_state = pin_input.value
        
        # Detect rising edge
        if not previous_state and current_state:
            detect_rising_edge()
        
        # Update previous state
        previous_state = current_state
        
        time.sleep(0.1)  # Short delay to reduce CPU usage

except KeyboardInterrupt:
    print("Script interrupted by user.")
finally:
    pwm_output.off()  # Turn off PWM output on exit
