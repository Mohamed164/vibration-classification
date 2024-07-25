from gpiozero import Button
import time

# Define GPIO 16 as a Button object
button = Button(16, bounce_time=0.1)  # Adjust bounce_time if needed

def button_pressed():
    print("Button was pressed!")

def button_released():
    print("Button was released!")

# Set the callback functions for button press and release
button.when_pressed = button_pressed
button.when_released = button_released

print("Press and release the button to test. Press Ctrl+C to exit.")

try:
    while True:
        time.sleep(1)  # Keep the script running
except KeyboardInterrupt:
    print("Script interrupted by user.")
