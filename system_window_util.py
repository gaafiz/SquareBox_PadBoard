from kivy.core.window import Window
from KivyOnTop import register_topmost

import win32gui
import win32con
import win32api

'''
The Implementation of this file is OS specific and at the moment only Windows is supported
'''

def set_always_upront(window_title):
    register_topmost(Window, window_title)

def set_transparency(window_title, transparency_level):
    window_handler = win32gui.FindWindow(None, window_title)
    win32gui.SetWindowLong(
        window_handler,
        win32con.GWL_EXSTYLE,
        win32gui.GetWindowLong(window_handler, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED
    )
    win32gui.SetLayeredWindowAttributes(
        window_handler,
        win32api.RGB(0, 0, 0),
        transparency_level,
        win32con.LWA_ALPHA
    )

def move_window(window_title, new_x, new_y, relative_cordinates=False):
    window_handler = win32gui.FindWindow(None, window_title)
    x, y, w, h = win32gui.GetWindowRect(window_handler)
    w -= x
    h -= y
    if relative_cordinates:
        new_x = x + new_x
        new_y = y + new_y

    win32gui.MoveWindow(window_handler, new_x, new_y, w, h, True)