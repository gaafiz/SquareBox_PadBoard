import time
from multiprocessing import Process, Pipe

import inputs
from inputs import GamePad, DeviceManager
from inputs import iter_unpack, EVENT_TYPES, WIN


# This patch fix the following inputs library issues:
#   - Fetching game_pad events causes Severe CPU usage
#   - Plug and Play not possible because self._GamePad__check_state()
#     doesn't trigger the disconnected error in the right thread
#   - BTN_START and BTN_SELECT buttons are switched
#   - Initialize an instance of DeviceManager outside of the inputs.py file,
#     causes DeviceManager().codes['type_codes'] to be empty


class FixedDeviceManager(DeviceManager):
    def __init__(self):
        super(FixedDeviceManager, self).__init__()


    def _post_init(self):
        # Fix wrong key codes
        self.codes['Key'][0x13a] = 'BTN_START'
        self.codes['Key'][0x13b] = 'BTN_SELECT'

        # Fix type_codes empty when a DeviceManager is initialized outside of inputs namespace
        self.codes['type_codes'] = dict(((value, key) for key, value in EVENT_TYPES))

        super(FixedDeviceManager, self)._post_init()

        # Replace all Gamepads with SleepingGamepads
        i = 0
        while i < len(self.gamepads):
            self.gamepads[i].manager = self
            self.gamepads[i] = SleepingGamePad(self.gamepads[i])
            i +=1


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

    # def __iter__(self):
    #     while True:
    #         event = self._do_iter()
    #         if not event and WIN:
    #             self._GamePad__check_state()
    #         if event:
    #             yield event

    # Set listener as non-daemon to facilitate plug-and-play feature
    @property
    def _pipe(self):
        """On Windows we use a pipe to emulate a Linux style character
        buffer."""
        if self._evdev:
            return None
        if not self.__pipe:
            target_function = self._get_target_function()
            if not target_function:
                return None

            self.__pipe, child_conn = Pipe(duplex=False)
            self._listener = Process(target=target_function,
                                     args=(child_conn,))
            self._listener.start()
        return self.__pipe

inputs.devices = FixedDeviceManager()

def waitng_for_controller(controller_idx=0):
    while True:
        try:
            inputs.devices = FixedDeviceManager()
            inputs.devices.gamepads[0].read()
            return
        except:
            time.sleep(3)
            pass