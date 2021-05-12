from loguru import logger
from simple_term_menu import TerminalMenu
from cli.helpers.page import Page


class Menu(Page):
    def __init__(self, header=None, description=None):
        super().__init__(header=header, description=description)
        self.menu_items = []

    def add_child(self, text, handler):
        self.menu_items.append((text, handler))
        return self

    def __call__(self, settings):
        menu_exit = False
        menu = TerminalMenu([item[0] for item in self.menu_items])

        while not menu_exit:
            self.pre_menu(settings)

            choice = menu.show()

            # menu_exit = self.menu_items[choice][1](settings)
            try:
                menu_exit = self.menu_items[choice][1](settings)
            # NOTE: This catches ALL exceptions thrown and not handled, causing
            # the menu to fail without saying what happened.
            except TypeError:  # catch ESC key to go back
                menu_exit = True
            except Exception as e:
                logger.debug(e)
                menu_exit = True
