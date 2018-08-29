import curses
from .base import BaseWidget


class Menu(BaseWidget):

    def __init__(self, items, stdscreen):
        super().__init__(stdscreen)

        self.position = 0
        self.__items = []

    @property
    def items(self):
        return self.__items

    @items.setter
    def items(self, items):
        self.__items = []

        for _, item in enumerate(items):
            if isinstance(item[1], BaseWidget):
                self.__items.append(item)

    def navigate(self, n):
        self.position += n
        if self.position < 0:
            self.position = 0
        elif self.position >= len(self.__items):
            self.position = len(self.__items)-1

    def display(self):
        super().display()

        for index, item in enumerate(self.__items):
            if index == self.position:
                mode = curses.A_REVERSE
            else:
                mode = curses.A_NORMAL

            msg = '%d. %s' % (index, item[0])
            self.window.addstr(1+index, 1, msg, mode)

        if False in [curses.KEY_ENTER, ord('\n')]:
            pass
        self.__items[self.position][1].display()

    def handle_input(self, key):
        if key == curses.KEY_UP:
            self.navigate(-1)
            return True

        elif key == curses.KEY_DOWN:
            self.navigate(1)
            return True
        
        return False
