import os
from tkinter import PhotoImage

assets_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'assets/'))


class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        self.img = PhotoImage(file=assets_folder + '/' + self.suit + self.value + ".png")

    def __repr__(self):
        return " of ".join((self.value, self.suit))

    def get_file(self):
        return self.img

    @classmethod
    def get_back_file(cls):
        cls.back = PhotoImage(file=assets_folder + "/back.png")

        return cls.back