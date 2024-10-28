# import serial

# # Open serial port with SBUS settings
# ser = serial.Serial(
#     port='/dev/ttyUSB0',  # Replace with your serial port
#     baudrate=100000,      # SBUS uses 100000 baudrate
#     parity=serial.PARITY_EVEN,
#     stopbits=serial.STOPBITS_TWO,
#     bytesize=serial.EIGHTBITS,
#     timeout=0.1           # Non-blocking mode
# )

# def invert_byte(byte):
#     # Invert the bits of the byte (0xFF - byte) is another method
#     return byte ^ 0xFF

# def invert_data(data):
#     # Apply inversion to all bytes in the data frame
#     return bytes(invert_byte(byte) for byte in data)

# while True:
#     # Read 25 bytes from the SBUS port
#     data = ser.read(25)
    
#     if data:
#         # Invert the data to get the correct SBUS frame
#         inverted_data = invert_data(data)
        
#         # Print the raw inverted byte frame
#         print("Raw Inverted SBUS Frame:", inverted_data.hex().upper())

# # Don't forget to close the serial port when done
# ser.close()
