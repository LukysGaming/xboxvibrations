# XONE Vibration Control Script

## Overview

Made this cus I couldnt find anything similiar 
This Python script allows you to control the vibration intensity of your Xbox One game controller using mouse scroll events and a button press.

## Prerequisites

- Python 3.x
- [pynput](https://pypi.org/project/pynput/) library (only for the vibration adjusment one)
- XInput-compatible game controller

## Installation

1. Install the required Python libraries: 
(only for the vibration adjusment one)

    ```bash
    pip install pynput
    ```

3. Ensure you have a compatible XInput game controller connected to your system.

## Usage

### With Vibration Adjustment

1. **Clone the repository:**

    ```bash
    git clone https://github.com/lukysgaming/xboxvibrations.git
    ```

2. **Navigate to the project directory:**

    ```bash
    cd xboxvibrations
    ```

3. **Run the script:**

    ```bash
    python xboxvibrations.py
    ```

4. **Adjust vibration intensity:**
    - Scroll up or down with your mousewheel.

5. **Toggle vibration:**
    - Press any button on the game controller.

### Without Vibration Adjustment

If you prefer not to adjust vibration intensity, a simplified version is also available:

1. **Clone the repository:**

    ```bash
    git clone https://github.com/lukysgaming/xboxvibrations.git
    ```

2. **Navigate to the project directory:**

    ```bash
    cd xboxvibrations
    ```

3. **Run the script:**

    ```bash
    python xboxvibrationslite.py
    ```

4. **Toggle vibration:**
    - Press any button on the game controller.

## Notes

- Ensure that the `xinput1_4` library is available on your system.
- Terminate the script by pressing `Ctrl + C`.
- Tested on w10 with xone controller
