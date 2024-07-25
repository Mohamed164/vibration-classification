import time
import board
import busio
from adafruit_adxl34x import ADXL345

# Initialize I2C bus and ADXL345 sensor
i2c = busio.I2C(board.SCL, board.SDA)
accelerometer = ADXL345(i2c)

def read_accelerometer():
    x, y, z = accelerometer.acceleration
    return x, y, z

def main():
    print("Starting ADXL345 sensor")
    while True:
        x, y, z = read_accelerometer()
        print(f"X: {x:.2f} m/s^2, Y: {y:.2f} m/s^2, Z: {z:.2f} m/s^2")
        time.sleep(0.5)

if __name__ == "__main__":
    main()
