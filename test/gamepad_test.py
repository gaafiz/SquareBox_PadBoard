from inputs import devices
from inputs import get_gamepad
import keyboard

import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

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
            print(str(event.code) + ' - ' + str(event.state))
