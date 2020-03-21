from tile import Tile

tiles = [
    Tile(
        [
            [',','a','c','b'],
            ["'",'d', 'f', 'e'],
            ['!', "g", 'i', 'h'],
            ['-', 'j', 'l', 'k'],
            ['del', 'm', 'n', 'space'],
            ['?', 'o', 'q', 'p'],
            ['(', 'r', 't', 's'],
            [':', 'u', 'w', 'v'],
            [')', 'x', 'z', 'y']
        ],
        [
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
    )

]

title = 'SquareBox PadBoard'
transparency_level = 210

from kivy.core.window import Window

Window.fullscreen = False
Window.borderless = True
Window.size = (300, 280)
Window.set_title(title)