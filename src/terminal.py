import questionary
from questionary import Validator, ValidationError, prompt

from assets.texts import WELCOME_MSG
from assets.texts import R2D2_MSG


class Terminal():
    def start(self):
        questionary.print(R2D2_MSG, style="bold  fg:white")

    def show_options():
        pass


Terminal().start()
