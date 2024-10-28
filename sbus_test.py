import serial
import time

# Replace 'COMx' with your actual serial port (e.g., 'COM3' on Windows or '/dev/ttyUSB0' on Linux)
serial_port = '/dev/ttyUSB2'
baud_rate = 100000
inverted = True  # SBUS is typically inverted, but it depends on your hardware setup

# Open the serial port
ser = serial.Serial(serial_port, baud_rate, timeout=1)

# Define the SBUS frame you want to send
sbus_frame = b"T\0\0\0\0\0\0\0\0\x0F\xEA\xD3\x88\xFA\xD4\xA7>\x8DhD}\xB2\x11\x8A"

# Function to invert bits (if needed)
def invert_data(data):
    return bytes(~b & 0xFF for b in data)

try:
    while True:
        # If the SBUS signal is inverted, invert the data
        if inverted:
            data_to_send = invert_data(sbus_frame)
        else:
            data_to_send = sbus_frame
        
        # Send the data over the serial port
        ser.write(data_to_send)
        
        # Wait for 14ms before sending the next frame
        time.sleep(0.01)

except KeyboardInterrupt:
    # Close the serial port when exiting the program
    ser.close()
    print("Serial port closed.")

