#from kivy.config import Config
#Config.read('kivy-conf.ini')
# set config
#Config.write()
from tile import Tile

tiles = [
    Tile(
        [
            ["'",'a','c','b'],
            ['!','d', 'f', 'e'],
            ["?", "g", 'i', 'h'],
            ['(', 'j', 'l', 'k'],
            ['bkspace', 'm', 'n', 'space'],
            [')', 'o', 'q', 'p'],
            [':', 'r', 't', 's'],
            ['.', 'u', 'w', 'v'],
            [';', 'x', 'z', 'y']
        ],
        [
            ['1','2','3','4'],
            ["5",'6', '7', '8'],
            ['9', "0", '#', '='],
            ['[', '{', '}', '@'],
            ['del', 'esc', 'tab', 'enter'],
            [']', '<', '>', '^'],
            ['"', '$', '&', ';'],
            ['~', '\\', '_', '|'],
            ['+', '%', '/', '*']
        ],

    ),
    Tile(
        [
            ['F1','F2','F3','F4'],
            ["F5",'F6', 'F7', 'F8'],
            ['F9', "F10", 'F11', 'F12'],
            ['', 'à', 'á', 'ä'],
            ['vol+', '<-', '->', 'vol-'],
            ['', 'è', 'é', 'ë'],
            ['', 'ì', 'í', 'ï'],
            ['play', 'ò', 'ó', 'ö'],
            ['', 'ù', 'ú', 'ü']
        ],
        [
            ['F1','F2','F3','F4'],
            ["F5",'F6', 'F7', 'F8'],
            ['F9', "F10", 'F11', 'F12'],
            ['', 'À', 'Á', 'Ä'],
            ['vol+', '<-', '->', 'vol-'],
            ['', 'È', 'É', 'Ë'],
            ['', 'Ì', 'Í', 'ï'],
            ['play', 'Ò', 'Ó', 'Ö'],
            ['', 'Ù', 'Ú', 'Ü']
        ],
    ),


]

title = 'SquareBox PadBoard'
transparency_level = 210

from kivy.core.window import Window

Window.fullscreen = False
Window.borderless = True
Window.size = (300, 280)
