import time
import smbus2

# ADXL345 I2C address
ADXL345_ADDRESS = 0x53

# ADXL345 register addresses
POWER_CTL = 0x2D
DATA_FORMAT = 0x31
DATAX0 = 0x32
DATAX1 = 0x33
DATAY0 = 0x34
DATAY1 = 0x35
DATAZ0 = 0x36
DATAZ1 = 0x37

# Initialize I2C bus
bus = smbus2.SMBus(1)  # For Raspberry Pi, bus number is usually 1

def init_adxl345():
    # Power down the ADXL345
    bus.write_byte_data(ADXL345_ADDRESS, POWER_CTL, 0x00)
    time.sleep(0.1)
    # Set to measurement mode
    bus.write_byte_data(ADXL345_ADDRESS, POWER_CTL, 0x08)
    time.sleep(0.1)
    # Set data format to full resolution
    bus.write_byte_data(ADXL345_ADDRESS, DATA_FORMAT, 0x08)

def read_axis(axis_lsb_reg, axis_msb_reg):
    # Read 2 bytes of data from the accelerometer
    lsb = bus.read_byte_data(ADXL345_ADDRESS, axis_lsb_reg)
    msb = bus.read_byte_data(ADXL345_ADDRESS, axis_msb_reg)
    
    # Combine the bytes and convert to a signed 16-bit integer
    value = (msb << 8) | lsb
    if value & 0x8000:
        value -= 1 << 16  # Convert from unsigned to signed

    return value

def read_accelerometer():
    x = read_axis(DATAX0, DATAX1)
    y = read_axis(DATAY0, DATAY1)
    z = read_axis(DATAZ0, DATAZ1)
    return x, y, z

def main():
    init_adxl345()
    while True:
        x, y, z = read_accelerometer()
        print(f"X: {x} Y: {y} Z: {z}")
        time.sleep(0.5)

if __name__ == "__main__":
    main()
