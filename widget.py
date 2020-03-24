from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ListProperty
from kivy.uix.label import Label
from kivy.utils import escape_markup
from kivy.properties import ListProperty


black = [0, 0, 0, 1]
orange = [1, 0.6, 0.1, 1]
white = [1, 1, 1, 1]
gray = [0.77, 0.77, 0.77, 1]

Builder.load_string('''
#:import black widget.black

<ActionsGridLayout>
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
    color: black
    bold: True
    font_size: '22sp'
''')


class ActionsGridLayout(GridLayout):
    default_background_color = gray
    target_background_color = orange

    background_color = ListProperty()

    def __init__(self, actions, label_updater, **kwargs):
        kwargs['cols'] = 3
        super(ActionsGridLayout, self).__init__(**kwargs)

        for action_idx, action in enumerate(actions):
            self.add_widget(Label())
            action_label = Label(text=action)
            label_updater(action_label, action_idx)
            self.add_widget(action_label)
        self.add_widget(Label())

        self.untarget_it()

    def target_it(self):
        self.background_color = self.target_background_color

    def untarget_it(self):
        self.background_color = self.default_background_color

    pass
