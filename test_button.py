from gpiozero import Button

def button_pressed():
    print("Button was pressed!")

button = Button(16, bounce_time=0.1)
button.when_pressed = button_pressed

print("Press the button...")
button.wait_for_press()
