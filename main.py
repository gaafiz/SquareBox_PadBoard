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
import gamepad_high_cpu_usage_patch

Window.fullscreen = False
Window.size = (300, 280)

Builder.load_string('''
<MyBoxLayout>
    canvas.before:
        Color:
            rgba: .5, .5, .5, 1
        Line:
            width: 2
            rectangle: self.x, self.y, self.width, self.height

<TargetBoxLayout>
    canvas.before:
        Color:
            rgba: 1, 0.6, 0.1, 1
        Rectangle:
            pos: self.pos
            size: self.size
        Color:
            rgba: .5, .5, .5, 1
        Line:
            width: 2
            rectangle: self.x, self.y, self.width, self.height
''')

# This class stores the info of .kv file
# when it is called goes to my.kv file
class MainWidget(GridLayout):
    pass

class MyBoxLayout(BoxLayout):
    pass

class TargetBoxLayout(BoxLayout):
    pass


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
    def on_start(self, *args):
        TITLE = 'WhatAKeyboard'
        Window.set_title(TITLE)
        register_topmost(Window, TITLE)
        #keyboard.on_press_key('t', call2 )

    def input_loop(self):
        STICK_MAX = math.pow(2, 15)
        THRESHOLD = 0.1
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


    def build(self):
        self.low = default_letters
        self.upp = caps_letters

        self.active_box = 4
        self.boxes_of_letters = default_letters
        self.root_widget = BoxLayout()

        self.render_keyboard_layout(self.root_widget, self.boxes_of_letters, self.active_box)

        self._monitor_thread = threading.Thread(target=self.input_loop, args=())
        self._monitor_thread.daemon = True
        self._monitor_thread.start()


        #Clock.schedule_interval(self.update, 1.0/40.0)

        return self.root_widget

    def update(self, dt):
        abc =str(self.active_box)
        self.render_keyboard_layout(self.root_widget, self.boxes_of_letters, self.active_box)
        pass


    def render_keyboard_layout(self, root_layout, boxes_of_letters, targeted_box):
        keyboard_grid_layout = GridLayout(cols=3, row_default_height=60)

        boxes_count = 0
        for each_letter_box in boxes_of_letters:
            letters_grid_layout = GridLayout(cols=3, row_default_height=20)

            # Write letters in a box
            for letter in each_letter_box:
                letters_grid_layout.add_widget(Label(text=''))
                letters_grid_layout.add_widget(Label(text='[b]' + letter + '[/b]', markup=True, font_size='20sp'))
            letters_grid_layout.add_widget(Label(text=''))

            if boxes_count == targeted_box:
                wrapper_box_layout = TargetBoxLayout()
            else:
                wrapper_box_layout = MyBoxLayout()

            wrapper_box_layout.add_widget(letters_grid_layout)
            keyboard_grid_layout.add_widget(wrapper_box_layout)

            boxes_count = boxes_count + 1

        root_layout.clear_widgets()
        root_layout.add_widget(keyboard_grid_layout)



if __name__== "__main__":
    myApp().run()