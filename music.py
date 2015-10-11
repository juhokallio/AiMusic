__author__ = 'juho'


class Motif:
    def __init__(self, notes):
        self.notes = notes


class Variation:
    types = {

    }

    def __init__(self, music, type):
        self.origin = music
        self.type = type
        self.notes = self.types[type](music)
