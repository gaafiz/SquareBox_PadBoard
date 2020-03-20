from inputs import devices
from inputs import get_gamepad
import keyboard

import gamepad_high_cpu_usage_patch

if __name__== "__main__":
    print('\nGamepads:')
    for device in devices.gamepads:
        print(device)

    is_shift = False

    print('\nEvents')
    while 1:
        events = get_gamepad()
        for event in events:
            print(event.code)
