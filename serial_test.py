import serial
import threading

from time import sleep

# Set up the serial connection
ser = serial.Serial(
    port='/dev/ttyUSB1',  # Replace with your port name
    baudrate=19200,       # Set the baud rate to 19200
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    timeout=1             # Read timeout in seconds
)

# Function to receive and print frames starting with 0x5A 0xA5
def receive_and_print_frames():
    try:
        buffer = bytearray()  # Buffer to accumulate data
        frame_start_sequence = bytearray([0x5A, 0xA5])  # Define the start sequence
        frame_active = False  # Flag to indicate if we're within a frame

        while True:
            # Read one byte at a time
            data = ser.read(1)

            if data:
                # Add the byte to the buffer
                buffer.extend(data)
                
                # Check if the buffer has detected the start sequence
                if len(buffer) >= 2 and buffer[-2:] == frame_start_sequence:
                    if frame_active:
                        # If a frame was active, we have reached the start of the next frame
                        # Print the previous frame
                        print("Frame received:", ' '.join(f'{byte:02X}' for byte in buffer[:-2]))
                        # Start new frame with the new start sequence
                        buffer = bytearray(frame_start_sequence)
                    else:
                        # Start of the first frame
                        frame_active = True
                elif frame_active:
                    # Continue collecting bytes for the current frame
                    continue

    except KeyboardInterrupt:
        # Close the serial port on a keyboard interrupt
        ser.close()
        print("Serial connection closed.")

# Function to send a predefined byte string
def set_run_mode():
    byte_array = bytearray([0x5A, 0xA5, 0x06, 0x83, 0x10, 0x05, 0x01, 0x00, 0x00])
    ser.write(byte_array)
    print(f"Frame sent: {' '.join(f'{byte:02X}' for byte in byte_array)}")

def set_set_mode():
    byte_array = bytearray([0x5A, 0xA5, 0x06, 0x83, 0x10, 0x05, 0x01, 0x00, 0x01])
    ser.write(byte_array)
    print(f"Frame sent: {' '.join(f'{byte:02X}' for byte in byte_array)}")

def set_motor_mode(motor_mode):
    byte_array = bytearray([0x5A, 0xA5, 0x06, 0x83, 0x00, 0x10, 0x01, 0x00, motor_mode])
    ser.write(byte_array)
    print(f"Frame sent: {' '.join(f'{byte:02X}' for byte in byte_array)}")
    sleep(0.1)

    byte_array = bytearray([0x5A, 0xA5, 0x06, 0x83, 0x00, 0x11, 0x01, 0x00, motor_mode])
    ser.write(byte_array)
    print(f"Frame sent: {' '.join(f'{byte:02X}' for byte in byte_array)}")
    sleep(0.1)

    # byte_array = bytearray([0x5A, 0xA5, 0x06, 0x83, 0x00, 0x12, 0x01, 0x00, 0x01])
    # ser.write(byte_array)
    # print(f"Frame sent: {' '.join(f'{byte:02X}' for byte in byte_array)}")


def set_motor_max_speed(max_speed):
    # m1
    byte_array = bytearray([0x5A, 0xA5, 0x06, 0x83, 0x00, 0x16, 0x01, max_speed[0], max_speed[1]])
    ser.write(byte_array)
    print(f"Frame sent: {' '.join(f'{byte:02X}' for byte in byte_array)}")
    sleep(0.1)

    # m2
    byte_array = bytearray([0x5A, 0xA5, 0x06, 0x83, 0x00, 0x17, 0x01, max_speed[0], max_speed[1]])
    ser.write(byte_array)
    print(f"Frame sent: {' '.join(f'{byte:02X}' for byte in byte_array)}")
    sleep(0.1)

    # byte_array = bytearray([0x5A, 0xA5, 0x06, 0x83, 0x00, 0x12, 0x01, 0x00, 0x01])
    # ser.write(byte_array)
    # print(f"Frame sent: {' '.join(f'{byte:02X}' for byte in byte_array)}")


def set_pwm_mode(pwm_mode):
    byte_array = bytearray([0x5A, 0xA5, 0x06, 0x83, 0x00, 0x25, 0x01, 0x00, pwm_mode])
    ser.write(byte_array)
    print(f"Frame sent: {' '.join(f'{byte:02X}' for byte in byte_array)}")

speed_1000 = [0x03, 0xE8]
speed_2000 = [0x07, 0xD0]

PWM_MIX = 0x00
PWM_IND = 0x01

def user_input_thread():
    while True:
        user_input = input("Enter '1' to send the byte frame or 'exit' to quit: ")
        if user_input == '0':
            set_run_mode()
        if user_input == '1':
            set_set_mode()
        if user_input == '2':
            set_motor_mode(0x01)
        if user_input == '3':
            set_motor_max_speed(speed_1000)
        if user_input == '4':
            set_pwm_mode(PWM_IND)
        elif user_input.lower() == 'exit':
            ser.close()
            print("Serial connection closed.")
            break
        else:
            print("Invalid input. Please enter '1' to send the frame or 'exit' to quit.")

if __name__ == "__main__":
    # Start the receiving function in a separate thread
    receive_thread = threading.Thread(target=receive_and_print_frames, daemon=True)
    receive_thread.start()
    
    # Start the user input thread for sending data
    user_input_thread()
