import ctypes
import time

class Vibration(ctypes.Structure):
    _fields_ = [("left_speed", ctypes.c_ushort), ("right_speed", ctypes.c_ushort)]

class Gamepad(ctypes.Structure):
    _fields_ = [("buttons", ctypes.c_ushort)]

class State(ctypes.Structure):
    _fields_ = [("packet_number", ctypes.c_ulong), ("gamepad", Gamepad)]

xinput = ctypes.windll.xinput1_4

BUTTON_NAMES = {
    0x1000: "A",
    0x2000: "B",
    0x4000: "X",
    0x8000: "Y",
    # Add more button mappings as needed
}

# Replace the ASCII art with your own representation
BUTTON_ART = {
    "A": [" .----------------. ", "| .--------------. |", "| |      __      | |", "| |     /  \\     | |", "| |    / /\\ \\    | |", "| |   / ____ \\   | |", "| | _/ /    \\ \\_ | |", "| ||____|  |____|| |", "| |              | |", "| '--------------' |", " '----------------' "],
    "B": [" .----------------. ", "| .--------------. |", "| |   ______     | |", "| |  |_   _ \\    | |", "| |    | |_) |   | |", "| |    |  __'.   | |", "| |   _| |__) |  | |", "| |  |_______/   | |", "| |              | |", "| '--------------' |", " '----------------' "],
    "X": [" .----------------. ", "| .--------------. |", "| |  ____  ____  | |", "| | |_  _||_  _| | |", "| |   \\ \\  / /   | |", "| |    > `' <    | |", "| |  _/ /'`\\ \\_  | |", "| | |____||____| | |", "| |              | |", "| '--------------' |", " '----------------' "],
    "Y": [" .----------------. ", "| .--------------. |", "| |  ____  ____  | |", "| | |_  _||_  _| | |", "| |   \\ \\  / /   | |", "| |    \\ \\/ /    | |", "| |    _|  |_    | |", "| |   |______|   | |", "| |              | |", "| '--------------' |", " '----------------' "],
    # Add more button ASCII art as needed
}

def set_vibration(index, left_speed, right_speed):
    vibration = Vibration(left_speed, right_speed)
    xinput.XInputSetState(index, ctypes.byref(vibration))

def is_button_pressed(state, button):
    return (state.gamepad.buttons & button) != 0

def get_pressed_button(state):
    for button, name in BUTTON_NAMES.items():
        if is_button_pressed(state, button):
            return name
    return None

def print_button_art(button_name):
    art_lines = BUTTON_ART.get(button_name, ["", "", ""])
    for line in art_lines:
        print(line)

def print_vibration_intensity(left_speed, right_speed):
    left_percentage = (left_speed / 65535) * 100
    right_percentage = (right_speed / 65535) * 100

    print("Vibration Intensity:")
    print(f"   Left:  {'█' * int(left_speed / 3277)}  {left_percentage:.2f}%  Value: {left_speed}")
    print(f"   Right: {'█' * int(right_speed / 3277)}  {right_percentage:.2f}%  Value: {right_speed}")

def main():
    index, enabled = 0, False
    button_pressed = False

    try:
        while True:
            state = State()
            xinput.XInputGetState(index, ctypes.byref(state))

            pressed_button = get_pressed_button(state)

            if pressed_button is not None:
                if not button_pressed:
                    button_pressed = True
                    enabled = not enabled
                    left_speed, right_speed = (65535, 65535) if enabled else (0, 0)
                    set_vibration(index, left_speed, right_speed)
                    print_vibration_intensity(left_speed, right_speed)
                    print(f"Button {pressed_button} pressed")
                    print_button_art(pressed_button)
            else:
                button_pressed = False

            time.sleep(0.1)

    except KeyboardInterrupt:
        set_vibration(index, 0, 0)  # Ensure vibration is off before exiting
        print("Script terminated by user.")

if __name__ == "__main__":
    main()
