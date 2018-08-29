import curses
from .base import BaseWidget


class Tabbar(BaseWidget):

    def __init__(self, stdscreen):
        super().__init__(stdscreen)

        self.__subwindow = self.window.subwin(1, 0)
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

    @property
    def subwindow(self):
        return self.__subwindow

    def navigate(self, n):
        self.position += n
        if self.position < 0:
            self.position = 0
        elif self.position >= len(self.items):
            self.position = len(self.items)-1

    def display(self):
        super().display()

        length = 0
        for index, item in enumerate(self.items):
            if index == self.position:
                mode = curses.A_REVERSE
            else:
                mode = curses.A_NORMAL

            msg = item[0]
            self.window.addstr(0, length, msg, mode)
            length += len(msg)

        self.items[self.position][1].display()
        self.window.refresh()

    def update(self):
        self.items[self.position][1].update()

    def handle_input(self, key):

        if self.items[self.position][1].handle_input(key):
            return True

        if key == curses.KEY_LEFT:
            self.navigate(-1)
            return True

        elif key == curses.KEY_RIGHT:
            self.navigate(1)
            return True

        return False
