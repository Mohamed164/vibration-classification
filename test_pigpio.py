import pigpio
import time

# Define the GPIO pin connected to the LED
LED_PIN = 17

# Initialize the pigpio library
pi = pigpio.pi()

# Check if the connection to pigpiod was successful
if not pi.connected:
    print("Failed to connect to pigpiod.")
    exit()

# Set the GPIO pin mode to OUTPUT
pi.set_mode(LED_PIN, pigpio.OUTPUT)

# Blink the LED on and off
try:
    while True:
        pi.write(LED_PIN, 1)  # Turn the LED on
        print("LED ON")
        time.sleep(1)         # Wait for 1 second

        pi.write(LED_PIN, 0)  # Turn the LED off
        print("LED OFF")
        time.sleep(1)         # Wait for 1 second

except KeyboardInterrupt:
    # Clean up on Ctrl+C
    print("Exiting...")
    pi.write(LED_PIN, 0)  # Ensure LED is turned off
    pi.stop()             # Disconnect from pigpiod

