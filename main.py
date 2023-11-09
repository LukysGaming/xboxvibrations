# Import necessary libraries
import ctypes
import time
from pynput import mouse

# Define a structure for vibration parameters
class Vibration(ctypes.Structure):
    _fields_ = [("left_speed", ctypes.c_ushort), ("right_speed", ctypes.c_ushort)]

# Define a structure for gamepad buttons
class Gamepad(ctypes.Structure):
    _fields_ = [("buttons", ctypes.c_ushort)]

# Define a structure for the overall state including packet number and gamepad
class State(ctypes.Structure):
    _fields_ = [("packet_number", ctypes.c_ulong), ("gamepad", Gamepad)]

# Load the xinput library
xinput = ctypes.windll.xinput1_4

# Function to set vibration intensity
def set_vibration(index, left_speed, right_speed):
    vibration = Vibration(left_speed, right_speed)
    xinput.XInputSetState(index, ctypes.byref(vibration))

# Function to check if a button is pressed
def is_button_pressed(state, button):
    return (state.gamepad.buttons & button) != 0

# Function to print vibration intensity in a human-readable format
def print_vibration_intensity(left_speed, right_speed):
    left_percentage = (left_speed / 65535) * 100
    right_percentage = (right_speed / 65535) * 100

    print("Vibration Intensity:")
    print(f"   Left:  {'█' * (left_speed // 3277)}  {left_percentage:.2f}%  Value: {left_speed}")
    print(f"   Right: {'█' * (right_speed // 3277)}  {right_percentage:.2f}%  Value: {right_speed}")

# Callback function for mouse scroll events
def on_scroll(x, y, dx, dy):
    global left_speed, right_speed
    left_speed = max(0, min(65535, left_speed + int(dy * 6553.5)))
    right_speed = max(0, min(65535, right_speed + int(dy * 6553.5)))
    set_vibration(0, left_speed, right_speed)
    print_vibration_intensity(left_speed, right_speed)

# Main function
def main():
    global left_speed, right_speed
    left_speed, right_speed = 0, 0

    index, enabled = 0, False
    button_pressed = False

    # Start the mouse listener for scroll events
    listener = mouse.Listener(on_scroll=on_scroll)
    listener.start()

    try:
        while True:
            # Get the current state of the game controller
            state = State()
            xinput.XInputGetState(index, ctypes.byref(state))

            # Check if a specific button is pressed to toggle vibration
            if is_button_pressed(state, 0xFFFF):
                if not button_pressed:
                    button_pressed = True
                    enabled = not enabled
                    left_speed, right_speed = (65535, 65535) if enabled else (0, 0)
                    set_vibration(index, left_speed, right_speed)
                    print_vibration_intensity(left_speed, right_speed)
            else:
                button_pressed = False

            # Sleep for a short duration to avoid high CPU usage
            time.sleep(0.1)

    except KeyboardInterrupt:
        # Turn off vibration and stop the script on user interruption
        set_vibration(index, 0, 0)
        print("Script terminated by user.")
        listener.stop()
        listener.join()

# Entry point of the script
if __name__ == "__main__":
    main()
