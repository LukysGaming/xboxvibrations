import ctypes
import time

class Vibration(ctypes.Structure):
    _fields_ = [("left_speed", ctypes.c_ushort), ("right_speed", ctypes.c_ushort)]

class Gamepad(ctypes.Structure):
    _fields_ = [("buttons", ctypes.c_ushort)]

class State(ctypes.Structure):
    _fields_ = [("packet_number", ctypes.c_ulong), ("gamepad", Gamepad)]

xinput = ctypes.windll.xinput1_4

def set_vibration(index, left_speed, right_speed):
    vibration = Vibration(left_speed, right_speed)
    xinput.XInputSetState(index, ctypes.byref(vibration))

def is_button_pressed(state, button):
    return (state.gamepad.buttons & button) != 0

def print_vibration_intensity(left_speed, right_speed):
    left_percentage = (left_speed / 65535) * 100
    right_percentage = (right_speed / 65535) * 100

    print("Vibration Intensity:")
    print(f"   Left:  {'█' * (left_speed // 3277)}  {left_percentage:.2f}%  Value: {left_speed}")
    print(f"   Right: {'█' * (right_speed // 3277)}  {right_percentage:.2f}%  Value: {right_speed}")

def main():
    index, enabled = 0, False
    button_pressed = False

    try:
        while True:
            state = State()
            xinput.XInputGetState(index, ctypes.byref(state))

            if is_button_pressed(state, 0xFFFF):
                if not button_pressed:
                    button_pressed = True
                    enabled = not enabled
                    left_speed, right_speed = (65535, 65535) if enabled else (0, 0)
                    set_vibration(index, left_speed, right_speed)
                    print_vibration_intensity(left_speed, right_speed)
            else:
                button_pressed = False

            time.sleep(0.1)

    except KeyboardInterrupt:
        set_vibration(index, 0, 0)  # Ensure vibration is off before exiting
        print("Script terminated by user.")

if __name__ == "__main__":
    main()
