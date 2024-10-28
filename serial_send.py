import serial

# Configure the serial port
ser = serial.Serial(
    port='/dev/ttyUSB0',       # Replace with your port name, e.g., 'COM3' on Windows or '/dev/ttyUSB0' on Linux
    baudrate=115200,   # Set baud rate to 100000
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    timeout=1          # Read timeout in seconds
)

# Data to send
data = bytearray([0x5A, 0xA5, 0x06, 0x83, 0x10, 0x05, 0x01, 0x01])

# Send the data
ser.write(data)

# Optional: Read response (if any)
response = ser.read(8)  # Adjust the number of bytes to read as per your protocol
print(f"Received: {response}")

# Close the serial port
ser.close()
