from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty

black = [0, 0, 0, 1]
orange = [1, 0.6, 0.1, 1]
white = [1, 1, 1, 1]
gray = [0.77, 0.77, 0.77, 1]

Builder.load_string('''
<MyBoxLayout>
    canvas.before:
        Color: 
            rgba: self.background_color
        Rectangle:
            pos: self.pos
            size: self.size
        Color:
            rgba: .5, .5, .5, 1
        Line:
            width: 2
            rectangle: self.x, self.y, self.width, self.height
<Label>
    color: [0, 0, 0, 1]
''')

class MyBoxLayout(BoxLayout):
    default_background_color = gray
    target_background_color = orange

    background_color = ListProperty(default_background_color)

    def target_it(self):
        self.background_color = self.target_background_color

    def untarget_it(self):
        self.background_color = self.default_background_color

    pass