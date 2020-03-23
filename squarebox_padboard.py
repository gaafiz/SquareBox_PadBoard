from kivy.config import Config
#Config.read('kivy-conf.ini')
# set config
#Config.write()

# Std libs
import math
import time
import threading


import kivy
from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.properties import ListProperty
from kivy.properties import NumericProperty
from kivy.utils import escape_markup
from kivy.lang import Builder


# Kivy - Addons

# Input libraries
import keyboard
from inputs import devices
from inputs import get_gamepad
from inputs import GamePad
from inputs import XinputGamepad
from inputs import iter_unpack

# custom libs
from widget import ActionsGridLayout
import gamepad_high_cpu_usage_patch
import system_window_util as window_util
import squarebox_gamepad_config as app_config


default_letters = app_config.tiles[0].foreground_grill
caps_letters = app_config.tiles[0].background_grill

class myApp(App):
    title = app_config.title
    is_in_pause = False
    boxes_of_letters = ListProperty(default_letters)
    active_box = NumericProperty(-1)
    yVel = 0
    xVel = 0
    is_hide = False

    low = default_letters
    upp = caps_letters

    def on_start(self, *args):
        window_util.set_always_upront(app_config.title)
        window_util.set_transparency(app_config.title, app_config.transparency_level)
        pass


    def input_loop(self):
        STICK_MAX = math.pow(2, 15)
        THRESHOLD = 0.33
        TRIGGER_THRESHOLD = 10
        y_axis = 'CENTER'
        x_axis = 'CENTER'
        velocity_constant = 15

        is_L2_pressed = False
        is_R2_pressed = False

        while True:
            events = get_gamepad()
            for event in events:
                if event.code == 'ABS_Z':
                    is_L2_pressed = event.state > TRIGGER_THRESHOLD
                elif event.code == 'ABS_RZ':
                    is_R2_pressed = event.state > TRIGGER_THRESHOLD
                elif event.code == 'BTN_SELECT' and event.state == 1:
                    if is_L2_pressed and is_R2_pressed:
                        self.is_in_pause = not self.is_in_pause
                elif self.is_in_pause:
                    continue

                elif event.code == 'BTN_NORTH' and event.state == 1:
                    letter = self.boxes_of_letters[self.active_box][0]
                    if letter == 'del':
                        keyboard.press_and_release('backspace')
                    else:
                        keyboard.write(letter)
                elif event.code == 'BTN_WEST'and event.state == 1:
                    letter = self.boxes_of_letters[self.active_box][1]
                    keyboard.write(letter)
                elif event.code == 'BTN_EAST' and event.state == 1:
                    letter = self.boxes_of_letters[self.active_box][2]
                    keyboard.write(letter)
                elif event.code == 'BTN_SOUTH' and event.state == 1:
                    letter = self.boxes_of_letters[self.active_box][3]
                    if letter == 'enter':
                        keyboard.press_and_release('enter')
                    elif letter == 'space':
                        keyboard.write(' ')
                    else:
                        keyboard.write(letter)

                elif event.code == 'BTN_TL' and event.state == 1:
                    self.boxes_of_letters = self.upp
                elif event.code == 'BTN_TL' and event.state == 0:
                    self.boxes_of_letters = self.low

                elif event.code == 'ABS_Y' or event.code == 'ABS_X':
                    if event.code == 'ABS_Y':
                        y_val = event.state / STICK_MAX
                        if y_val > THRESHOLD:
                            y_axis = 'TOP'
                        elif y_val < -THRESHOLD:
                            y_axis = 'BOTTOM'
                        else:
                            y_axis = 'CENTER'

                    elif event.code == 'ABS_X':
                        x_val = event.state / STICK_MAX
                        if x_val > THRESHOLD:
                            x_axis = 'RIGHT'
                        elif x_val < -THRESHOLD:
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

                elif event.code == 'ABS_RY':
                    value = event.state / STICK_MAX
                    if value > THRESHOLD or value < -THRESHOLD:
                        self.yVel = - int(velocity_constant * value)
                    else:
                        self.yVel = 0
                elif event.code == 'ABS_RX':
                    value = event.state / STICK_MAX
                    if value > THRESHOLD or value < -THRESHOLD:
                        self.xVel = int(velocity_constant * value)
                    else:
                        self.xVel = 0


    def build(self):
        # Build Keyboard layout and set 'Center Box" as the active one
        self.root_widget = self.build_keyboard_layout(self.boxes_of_letters)
        self.active_box = 4

        # Start rendering and input listening loops
        Clock.schedule_interval(self.update_window, 0.01)
        self.init_input_listening_thread()

        return self.root_widget

    def init_input_listening_thread(self):
        self._monitor_thread = threading.Thread(target=self.input_loop, args=())
        self._monitor_thread.daemon = True
        self._monitor_thread.start()

    def update_window(self, dt):
        """
            This method updates some graphic properties of the windows.
            I could set this changes using bindings but some windows
            properties can only be touched from the main Thread.
            All the sensitive updates to be done in the main Thread
            are collected within this method
        """

        # Window moving logic
        if self.yVel != 0:
            Window.top += self.yVel
        if self.xVel != 0:
            Window.left += self.xVel

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
            def update_label_text(instance, value):
                #label.set_text_with_default_style(value[box_idx][action_idx])
                pass
            self.bind(boxes_of_letters=update_label_text)



if __name__== "__main__":
    myApp().run()