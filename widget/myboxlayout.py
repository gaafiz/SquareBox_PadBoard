from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty


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
''')

class MyBoxLayout(BoxLayout):
    black = [0, 0, 0, 1]
    orange = [1, 0.6, 0.1, 1]

    background_color = ListProperty(black)

    def target_it(self):
        self.background_color = self.orange

    def untarget_it(self):
        self.background_color = self.black

    pass