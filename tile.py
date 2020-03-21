
class Tile:
    def __init__(self, foreground_grill, background_grill):
        self.foreground_grill = foreground_grill
        self.background_grill = background_grill or foreground_grill
