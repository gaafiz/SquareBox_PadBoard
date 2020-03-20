import time

from inputs import devices
from inputs import get_gamepad
from inputs import GamePad
from inputs import iter_unpack

'''
\brief - This sub-class aims to patch a High CPU usage issue with
         the GamePad parent class.
         
         The class override the _do_iter method adding a little sleep
         instruction to avoid infinite active loop fetching for the 
         next gamepad event.
'''
class SleepingGamePad(GamePad):
    def __init__(self, gamepad):
        super(SleepingGamePad, self).__init__(gamepad.manager,
                                              gamepad._device_path,
                                              gamepad._character_device_path)

    def _do_iter(self):
        read_size = self._get_total_read_size()
        data = self._get_data(read_size)
        if not data:
            time.sleep(0.0001)
            return None
        evdev_objects = iter_unpack(data)
        events = [self._make_event(*event) for event in evdev_objects]
        return events

devices.gamepads[0] = SleepingGamePad(devices.gamepads[0])
default_gamepad = devices.gamepads[0]