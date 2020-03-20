# Std libs
import math
import time
import threading


# Kivy - Graphic
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
from kivy.config import Config
from kivy.properties import ListProperty
from kivy.properties import NumericProperty

# Kivy - Addons
from KivyOnTop import register_topmost

# Input libraries
import keyboard
from inputs import devices
from inputs import get_gamepad
from inputs import GamePad
from inputs import XinputGamepad
from inputs import iter_unpack

# custom libs
from widget.myboxlayout import MyBoxLayout
import gamepad_high_cpu_usage_patch

Window.fullscreen = False
Window.size = (300, 280)

default_letters = [
    [',','a','c','b'],
    ["'",'d', 'f', 'e'],
    ['!', "g", 'i', 'h'],
    ['-', 'j', 'l', 'k'],
    ['del', 'm', 'n', 'space'],
    ['?', 'o', 'q', 'p'],
    ['(', 'r', 't', 's'],
    [':', 'u', 'w', 'v'],
    [')', 'x', 'z', 'y']
]

caps_letters = [
    [',','A','C','B'],
    ["'",'D', 'F', 'E'],
    ['!', "G", 'I', 'H'],
    ['-', 'J', 'L', 'K'],
    ['del', 'M', 'N', 'space'],
    ['?', 'O', 'Q', 'P'],
    ['(', 'R', 'T', 'S'],
    [':', 'U', 'W', 'V'],
    [')', 'X', 'Z', 'Y']
]

class myApp(App):
    boxes_of_letters = ListProperty(default_letters)
    active_box = NumericProperty(-1)

    def on_start(self, *args):
        TITLE = 'WhatAKeyboard'
        Window.set_title(TITLE)
        register_topmost(Window, TITLE)
        #keyboard.on_press_key('t', call2 )

    def input_loop(self):
        STICK_MAX = math.pow(2, 15)
        THRESHOLD = 0.33
        y_axis = 'CENTER'
        x_axis = 'CENTER'

        while True:
            events = get_gamepad()
            for event in events:
                if event.code == 'BTN_NORTH' and event.state == 0:
                    letter = self.boxes_of_letters[self.active_box][0]
                    if letter == 'del':
                        keyboard.press_and_release('backspace')
                    else:
                        keyboard.write(letter)
                elif event.code == 'BTN_WEST'and event.state == 0:
                    letter = self.boxes_of_letters[self.active_box][1]
                    keyboard.write(letter)
                elif event.code == 'BTN_EAST' and event.state == 0:
                    letter = self.boxes_of_letters[self.active_box][2]
                    keyboard.write(letter)
                elif event.code == 'BTN_SOUTH' and event.state == 0:
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

                elif event.code == 'ABS_Y':
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

    def init_input_listening_thread(self):
        self._monitor_thread = threading.Thread(target=self.input_loop, args=())
        self._monitor_thread.daemon = True
        self._monitor_thread.start()

    def build(self):
        self.low = default_letters
        self.upp = caps_letters

        self.root_widget = BoxLayout()
        self.render_keyboard_layout(self.root_widget, self.boxes_of_letters)
        self.active_box = 4

        self.init_input_listening_thread()
        return self.root_widget

    def register_letter_label(self, label, box_idx, letter_idx):
        def update_letter(instance, value):
            label.text = '[b]' + self.boxes_of_letters[box_idx][letter_idx] + '[/b]'
        self.bind(boxes_of_letters=update_letter)

    def register_letter_box(self, box, idx):
        def target_box(instance, new_active_box):
            if new_active_box == idx:
                box.target_it()
            else:
                box.untarget_it()

        self.bind(active_box=target_box)

    def render_keyboard_layout(self, root_layout, boxes_of_letters):
        keyboard_grid_layout = GridLayout(cols=3, row_default_height=60)

        boxes_count = 0
        for each_letter_box in boxes_of_letters:
            letters_grid_layout = GridLayout(cols=3, row_default_height=20)

            # Write letters in a box
            letter_count = 0
            for letter in each_letter_box:
                letters_grid_layout.add_widget(Label(text=''))
                save_lbl = Label(text='[b]' + letter + '[/b]', markup=True, font_size='20sp')
                self.register_letter_label(save_lbl, boxes_count, letter_count)
                letters_grid_layout.add_widget(save_lbl)
                letter_count += 1
            letters_grid_layout.add_widget(Label(text=''))

            wrapper_box_layout = MyBoxLayout()
            self.register_letter_box(wrapper_box_layout, boxes_count)
            wrapper_box_layout.add_widget(letters_grid_layout)
            keyboard_grid_layout.add_widget(wrapper_box_layout)

            boxes_count = boxes_count + 1

        root_layout.clear_widgets()
        root_layout.add_widget(keyboard_grid_layout)



if __name__== "__main__":
    myApp().run()