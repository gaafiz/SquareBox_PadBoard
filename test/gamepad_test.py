import inputs
from inputs import get_gamepad
import keyboard

import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import inputs_library_patches

if __name__== "__main__":
    print('\nGamepads:')
    for device in inputs.devices.gamepads:
        print(device)

    print('\nEvents')
    while 1:
        # events = get_gamepad()
        events = inputs.devices.gamepads[0].read()
        for event in events:
            print(str(event.code) + ' - ' + str(event.state) + " - " + str(event.ev_type))
