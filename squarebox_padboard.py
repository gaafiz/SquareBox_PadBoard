# Std libs
import math
import time
from time import time as now
import threading

# Kivy
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.properties import ListProperty, NumericProperty

# Input libraries
import keyboard
import mouse
from inputs import get_gamepad

# custom libs
import inputs_library_patches
import system_window_util as window_util
import squarebox_gamepad_config as app_config
from widget import ActionsGridLayout
from actions import get_actions_by_name

tiles = app_config.tiles

class myApp(App):
    # App Details
    title = app_config.title
    is_in_pause = False
    is_hide = False
    is_mouse_mode = False

    # In seconds
    hold_button_delay = 0.4
    rapid_fired_frequency = 0.035

    # What is active on the padboard
    current_padboard_tile = 0
    current_padboard_grill = ListProperty(tiles[current_padboard_tile].foreground_grill)
    active_box = NumericProperty(-1)

    WindowYPosVelocity = 0
    WindowXPosVelocity = 0
    MouseYPosVelocity = 0
    MouseXPosVelocity = 0

    # Special keys
    is_L1_pressed = False

    is_pressed = {
        'DOWN': (False, None),
        'UP': (False, None),
        'LEFT': (False, None),
        'RIGHT': (False, None),

        'BTN_NORTH': (False, None, 0),
        'BTN_SOUTH': (False, None, 0),
        'BTN_EAST': (False, None, 0),
        'BTN_WEST': (False, None, 0),
    }

    def on_start(self, *args):
        window_util.set_always_upront(app_config.title)
        window_util.set_transparency(app_config.title, app_config.transparency_level)
        pass

    def handle_action_input(self, event, btn, action_idx):
        if not event.code == btn:
            return False
        else:
            if event.state == 1:
                action = self.current_padboard_grill[self.active_box][action_idx]
                p, h, r = get_actions_by_name(action)
                p()
                self.is_pressed[btn] = (True, now(), self.active_box)
            else:
                self.is_pressed[btn] = (False, None, 0)
                action_name = self.current_padboard_grill[self.is_pressed[btn][2]][action_idx]
                p, h, r = get_actions_by_name(action_name)
                r()



    def release_key_if_pressed(self, key):
        if keyboard.is_pressed(key):
            keyboard.release(key)

    def release_mouse_if_pressed(self, button):
        if mouse.is_pressed(button=button):
            mouse.release(button=button)

    def handle_held_button_repetition(self):
        while True:
            tick_time = now()

            on_hold = lambda: None if self.is_mouse_mode else keyboard.press('left')
            on_release = lambda: self.release_mouse_if_pressed('left') if self.is_mouse_mode else self.release_key_if_pressed('left')
            self.held_button_action(tick_time, "LEFT", on_hold, on_release)

            on_hold = lambda: mouse.press(button='right') if self.is_mouse_mode else keyboard.press('right')
            on_release = lambda: self.release_mouse_if_pressed('right') if self.is_mouse_mode else self.release_key_if_pressed('right')
            self.held_button_action(tick_time, "RIGHT", on_hold, on_release)

            on_hold = lambda: mouse.wheel(delta=1) if self.is_mouse_mode else keyboard.press('up')
            on_release = lambda: None if self.is_mouse_mode else self.release_key_if_pressed('up')
            self.held_button_action(tick_time, "UP", on_hold, on_release)

            on_hold = lambda: mouse.wheel(delta=-1) if self.is_mouse_mode else keyboard.press('down')
            on_release = lambda: None if self.is_mouse_mode else self.release_key_if_pressed('down')
            self.held_button_action(tick_time, "DOWN", on_hold, on_release)

            def get_current_action(btn, action_idx):
                action_name = self.current_padboard_grill[self.is_pressed[btn][2]][action_idx]
                return get_actions_by_name(action_name)

            for btn, action_idx in [('BTN_NORTH', 0), ('BTN_WEST', 1), ('BTN_EAST', 2), ('BTN_SOUTH', 3)]:
                on_hold = lambda : get_current_action(btn, action_idx)[1]()
                on_release = lambda : get_current_action(btn, action_idx)[2]()
                self.held_button_action(tick_time, btn, on_hold, on_release)

            time.sleep(self.rapid_fired_frequency)

    def held_button_action(self, tick_time, code, on_hold, on_release):
        is_pressed = self.is_pressed[code]
        pressed = is_pressed[0]
        pressed_time = is_pressed[1]
        if pressed:
            if (tick_time - pressed_time) > self.hold_button_delay:
                on_hold()
        else:
            on_release()


    def input_loop(self):
        ANALOG_STICK_MAX_RAW_VALUE = math.pow(2, 15)
        ANALOG_STICK_DEADZONE_THRESHOLD = 0.33
        ANALOG_STICK_DEADZONE_FOR_MOUSE = 0.12
        TRIGGER_DEADZONE_THRESHOLD = 10
        MOVING_VELOCITY_CONSTANT = 15 * 3
        MOVING_MOUSE_VELOCITY_CONSTANT = 8

        y_axis = 'CENTER'
        x_axis = 'CENTER'

        is_L2_pressed = False
        is_R2_pressed = False
        is_START_pressed = False
        is_SELECT_pressed = False

        def reset_mouse_mode_sensitive_buttons():
            self.is_pressed['UP']= (False, None)
            self.is_pressed['DOWN']= (False, None)
            self.is_pressed['LEFT'] = (False, None)
            self.is_pressed['RIGHT'] = (False, None)
            self.release_key_if_pressed('up')
            self.release_key_if_pressed('down')
            self.release_key_if_pressed('left')
            self.release_key_if_pressed('right')
            self.release_mouse_if_pressed('left')
            self.release_mouse_if_pressed('right')

        self.init_input_held_buttons_handling()

        while True:
            events = get_gamepad()
            for event in events:

                # Change Tile grid
                if event.code == 'BTN_TL':
                    if event.state == 0:
                        self.current_padboard_grill = tiles[self.current_padboard_tile].foreground_grill
                        self.is_L1_pressed = False
                    else:
                        self.current_padboard_grill = tiles[self.current_padboard_tile].background_grill
                        self.is_L1_pressed = True

                # Handle Window Hide/show
                elif event.code == 'BTN_START':
                    if event.state == 0:
                        is_START_pressed = False
                    else:
                        is_START_pressed = True
                        if self.is_L1_pressed and is_SELECT_pressed:
                            self.is_in_pause = not self.is_in_pause

                elif event.code == 'BTN_SELECT':
                    if event.state == 0:
                        is_SELECT_pressed = False
                    else:
                        is_SELECT_pressed = True
                        if self.is_L1_pressed and is_START_pressed:
                            self.is_in_pause = not self.is_in_pause
                elif self.is_in_pause:
                    continue

                # Handle ALT, CTRL, SHIFT
                elif event.code == 'ABS_Z':
                    if not ((event.state > TRIGGER_DEADZONE_THRESHOLD) == is_L2_pressed):
                        is_L2_pressed = not is_L2_pressed
                        if is_L2_pressed:
                            keyboard.press("alt")
                        else:
                            keyboard.release("alt")

                elif event.code == 'ABS_RZ':
                    if not ((event.state > TRIGGER_DEADZONE_THRESHOLD) == is_R2_pressed):
                        is_R2_pressed = not is_R2_pressed
                        if is_R2_pressed:
                            keyboard.press("ctrl")
                        else:
                            keyboard.release("ctrl")

                elif event.code == 'BTN_TR':
                    if event.state == 0:
                        keyboard.release("shift")
                    else:
                        keyboard.press("shift")

                # Handle Actions
                elif self.handle_action_input(event, 'BTN_NORTH', 0):
                    pass
                elif self.handle_action_input(event, 'BTN_WEST', 1):
                    pass
                elif self.handle_action_input(event, 'BTN_EAST', 2):
                    pass
                elif self.handle_action_input(event, 'BTN_SOUTH', 3):
                    pass

                # Handle Active Boxes
                elif event.code == 'ABS_Y' or event.code == 'ABS_X':
                    if event.code == 'ABS_Y':
                        y_val = event.state / ANALOG_STICK_MAX_RAW_VALUE
                        if y_val > ANALOG_STICK_DEADZONE_THRESHOLD:
                            y_axis = 'TOP'
                        elif y_val < -ANALOG_STICK_DEADZONE_THRESHOLD:
                            y_axis = 'BOTTOM'
                        else:
                            y_axis = 'CENTER'

                    elif event.code == 'ABS_X':
                        x_val = event.state / ANALOG_STICK_MAX_RAW_VALUE
                        if x_val > ANALOG_STICK_DEADZONE_THRESHOLD:
                            x_axis = 'RIGHT'
                        elif x_val < -ANALOG_STICK_DEADZONE_THRESHOLD:
                            x_axis = 'LEFT'
                        else:
                            x_axis = 'CENTER'

                    if y_axis == 'TOP':
                        if x_axis == 'LEFT':
                            self.active_box = 0
                        elif x_axis == 'RIGHT':
                            self.active_box = 2
                        else:
                            self.active_box = 1
                    elif y_axis == 'BOTTOM':
                        if x_axis == 'LEFT':
                            self.active_box = 6
                        elif x_axis == 'RIGHT':
                            self.active_box = 8
                        else:
                            self.active_box = 7
                    else:
                        if x_axis == 'LEFT':
                            self.active_box = 3
                        elif x_axis == 'RIGHT':
                            self.active_box = 5
                        else:
                            self.active_box = 4

                # Handle window moving
                elif event.code == 'ABS_RY' and not self.is_mouse_mode:
                    value = event.state / ANALOG_STICK_MAX_RAW_VALUE
                    if value > ANALOG_STICK_DEADZONE_THRESHOLD or value < -ANALOG_STICK_DEADZONE_THRESHOLD:
                        self.WindowYPosVelocity = - int(MOVING_VELOCITY_CONSTANT * value)
                    else:
                        self.WindowYPosVelocity = 0
                elif event.code == 'ABS_RX' and not self.is_mouse_mode:
                    value = event.state / ANALOG_STICK_MAX_RAW_VALUE
                    if value > ANALOG_STICK_DEADZONE_THRESHOLD or value < -ANALOG_STICK_DEADZONE_THRESHOLD:
                        self.WindowXPosVelocity = int(MOVING_VELOCITY_CONSTANT * value)
                    else:
                        self.WindowXPosVelocity = 0

                # Handle Tile Changing
                elif event.code == 'BTN_THUMBL':
                    if event.state == 1:
                        self.current_padboard_tile = (self.current_padboard_tile + 1) % len(tiles)
                        self.current_padboard_grill = tiles[self.current_padboard_tile].foreground_grill

                # Handle Arrows
                elif event.code == 'ABS_HAT0Y' and not self.is_mouse_mode:
                    if event.state == 1: # DOWN ARROW
                        keyboard.press("down")
                        self.is_pressed['DOWN'] = (True, now())
                    elif event.state == -1: # UP ARROW
                        keyboard.press("up")
                        self.is_pressed['UP'] = (True, now())
                    else:
                        self.is_pressed['UP']= (False, None)
                        self.is_pressed['DOWN']= (False, None)
                        self.release_key_if_pressed('up')
                        self.release_key_if_pressed('down')

                elif event.code == 'ABS_HAT0X' and not self.is_mouse_mode:
                    if event.state == -1: # LEFT ARROW
                        keyboard.press("left")
                        self.is_pressed['LEFT'] = (True, now())
                    elif event.state == 1: # RIGHT ARROW
                        keyboard.press("right")
                        self.is_pressed['RIGHT'] = (True, now())
                        pass
                    else:
                        self.is_pressed['LEFT']= (False, None)
                        self.is_pressed['RIGHT']= (False, None)
                        self.release_key_if_pressed('left')
                        self.release_key_if_pressed('right')

                # Handle Mouse mode
                elif event.code == 'BTN_THUMBR':
                    if event.state == 1:
                        reset_mouse_mode_sensitive_buttons()

                        self.is_mouse_mode = not self.is_mouse_mode
                        if self.is_mouse_mode:
                            print("MOUSE MODE ON")
                        else:
                            print("MOUSE MODE OFF")

                # Mouse Buttons
                elif event.code == 'ABS_HAT0Y' and self.is_mouse_mode:
                    if event.state == 1: # DOWN ARROW
                       mouse.wheel(delta=-1)
                       self.is_pressed['DOWN'] = (True, now())
                    elif event.state == -1: # UP ARROW
                        mouse.wheel(delta=1)
                        self.is_pressed['UP'] = (True, now())
                    else:
                        self.is_pressed['UP']= (False, None)
                        self.is_pressed['DOWN']= (False, None)
                elif event.code == 'ABS_HAT0X' and self.is_mouse_mode:
                    if event.state == -1: # LEFT ARROW
                        mouse.press(button='left')
                        self.is_pressed['LEFT'] = (True, now())
                    elif event.state == 1: # RIGHT ARROW
                        mouse.press(button='right')
                        self.is_pressed['RIGHT'] = (True, now())
                        pass
                    else:
                        self.is_pressed['LEFT'] = (False, None)
                        self.is_pressed['RIGHT'] = (False, None)
                        self.release_mouse_if_pressed('left')
                        self.release_mouse_if_pressed('right')

                # Mouse movement
                elif event.code == 'ABS_RY' and self.is_mouse_mode:
                    moving_velocity = MOVING_MOUSE_VELOCITY_CONSTANT
                    value = event.state / ANALOG_STICK_MAX_RAW_VALUE
                    if value > ANALOG_STICK_DEADZONE_FOR_MOUSE or value < -ANALOG_STICK_DEADZONE_FOR_MOUSE:
                        self.MouseYPosVelocity = - int(moving_velocity * value)
                    else:
                        self.MouseYPosVelocity = 0
                elif event.code == 'ABS_RX' and self.is_mouse_mode:
                    moving_velocity = MOVING_MOUSE_VELOCITY_CONSTANT
                    value = event.state / ANALOG_STICK_MAX_RAW_VALUE
                    if value > ANALOG_STICK_DEADZONE_FOR_MOUSE or value < -ANALOG_STICK_DEADZONE_FOR_MOUSE:
                        self.MouseXPosVelocity = int(moving_velocity * value)
                    else:
                        self.MouseXPosVelocity = 0


    def update_secondary_values(self):
        """
            Handles all the non-critical periodical updates that can be executed outside of the main thread
        """

        while True:
            if self.MouseYPosVelocity != 0 or self.MouseXPosVelocity !=0:
                if self.is_L1_pressed:
                    mouse.move(self.MouseXPosVelocity * 3, self.MouseYPosVelocity * 3, absolute=False)
                else:
                    mouse.move(self.MouseXPosVelocity, self.MouseYPosVelocity, absolute=False)

            # Window moving logic
            if self.WindowYPosVelocity != 0 or self.WindowXPosVelocity != 0:
                window_util.move_window(
                    self.title,
                    self.WindowXPosVelocity,
                    self.WindowYPosVelocity,
                    relative_cordinates = True
                )

            time.sleep(0.01)
        pass

    def build(self):
        # Build Keyboard layout and set 'Center Box" as the active one
        root_widget = self.build_keyboard_layout(self.current_padboard_grill)
        self.active_box = 4

        # Start rendering and input listening loops
        Clock.schedule_interval(self.main_thread_updates, 0.04)
        self.init_input_listening_thread()
        self.init_secondary_update_thread()

        return root_widget

    def init_input_held_buttons_handling(self):
        thread = threading.Thread(target=self.handle_held_button_repetition, args=())
        thread.daemon = True
        thread.start()

    def init_input_listening_thread(self):
        self._monitor_thread = threading.Thread(target=self.input_loop, args=())
        self._monitor_thread.daemon = True
        self._monitor_thread.start()

    def init_secondary_update_thread(self):
        self._secomdary_update_thread = threading.Thread(target=self.update_secondary_values, args=())
        self._secomdary_update_thread.daemon = True
        self._secomdary_update_thread.start()

    def main_thread_updates(self, dt):
        """
            This method updates some graphic properties of the windows.
            I could set this changes using bindings but some windows
            properties can only be touched from the main Thread.
            All the sensitive updates to be done in the main Thread
            are collected within this method
        """

        # Replaced with the window_util.move_window method because faster and less cpu consuming
        # Window moving logic
        # if self.WindowYPosVelocity != 0:
        #     Window.top += self.WindowYPosVelocity
        # if self.WindowXPosVelocity != 0:
        #     Window.left += self.WindowXPosVelocity

        # Window hiding/showing logic
        if self.is_in_pause != self.is_hide:
            if self.is_in_pause:
                Window.hide()
            else:
                Window.show()
            self.is_hide = not self.is_hide

    def build_keyboard_layout(self, active_action_grid):
        keyboard_layout = GridLayout(cols=3, row_default_height=60)

        for action_box_id, each_action_box in enumerate(active_action_grid):
            label_updater = self.label_updater_for_box(action_box_id)
            action_box_layout = ActionsGridLayout(each_action_box, label_updater, row_default_height=20)
            keyboard_layout.add_widget(action_box_layout)
            self.active_box_updater(action_box_layout, action_box_id)

        return keyboard_layout

    def active_box_updater(self, box, idx):
        def target_box(instance, new_active_box):
            if new_active_box == idx:
                box.target_it()
            else:
                box.untarget_it()
        self.bind(active_box=target_box)

    def label_updater_for_box(self, box_idx):
        def label_updater(label, action_idx):
            def update_label_text(instance, new_grill):
                label.text = new_grill[box_idx][action_idx]
            self.bind(current_padboard_grill=update_label_text)
        return label_updater



if __name__== "__main__":
    myApp().run()