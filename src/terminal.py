import questionary
from assets.texts import R2D2_MSG, WAIT_MSG, VALIDATION_CONFIG_MSG, VALIDATION_AFIP_MSG, VALIDATION_AFIP_MSG


class Terminal():
    def start(self):
        questionary.print(R2D2_MSG, style="bold  fg:white")
        questionary.print(WAIT_MSG, style="italic")

    def show_startup_result(self, auth_config: bool, afip_working: bool):
        questionary.print(
            '\n'.join([f'   * {VALIDATION_CONFIG_MSG} {self.__check_helper(auth_config)}',
                       f'   * {VALIDATION_AFIP_MSG} {self.__check_helper(afip_working)}']))

    def __check_helper(self, valid: bool):
        if (valid):
            return '\u2705'
        return '\u274C'


term = Terminal()
term.start()
term.show_startup_result(True, False)
