from gpiozero import PWMOutputDevice
import time

# Initialize the PWM output device on pin 18
pwm = PWMOutputDevice(18, frequency=1000)  # 1 kHz frequency

def test_pwm():
    print("Starting PWM test...")
    
    # Test different duty cycles
    for duty_cycle in [0, 0.25, 0.5, 0.75, 1.0]:
        print(f"Setting PWM duty cycle to {duty_cycle * 100}%")
        pwm.value = duty_cycle
        time.sleep(2)  # Wait for 2 seconds to observe the change

    print("Stopping PWM.")
    pwm.off()  # Stop the PWM signal

if __name__ == '__main__':
    try:
        test_pwm()
    except KeyboardInterrupt:
        print("Test interrupted by user.")
        pwm.off()
