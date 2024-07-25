from gpiozero import LED
from time import sleep

# Define the GPIO pin connected to the LED
LED_PIN = 17

# Create an LED object
led = LED(LED_PIN)

# Blink the LED on and off
try:
    while True:
        led.on()   # Turn the LED on
        print("LED ON")
        sleep(1)   # Wait for 1 second

        led.off()  # Turn the LED off
        print("LED OFF")
        sleep(1)   # Wait for 1 second

except KeyboardInterrupt:
    # Clean up on Ctrl+C
    print("Exiting...")
    led.off()  # Ensure LED is turned off

