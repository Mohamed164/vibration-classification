from gpiozero import LED
from time import sleep

# Define GPIO 16 as an LED object
led = LED(16)

print("Toggling GPIO 16 (Pin 36)")

try:
    while True:
        led.on()   # Turn the LED (or GPIO 16) on
        print("GPIO 16 is HIGH")
        sleep(1)   # Wait for 1 second
        led.off()  # Turn the LED (or GPIO 16) off
        print("GPIO 16 is LOW")
        sleep(1)   # Wait for 1 second
except KeyboardInterrupt:
    print("Script interrupted. Cleaning up...")
finally:
    led.off()  # Ensure GPIO 16 is off on exit
