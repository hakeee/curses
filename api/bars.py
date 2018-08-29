import curses
from .base import BaseWidget, Text

class StatusBar(BaseWidget):
    def __init__(self, window, delimiter = None):
        super().__init__(window)
        self.delimiter = delimiter
        self.__subwindow = self.window.subwin(self.height, 0)
        self.__items = []

    @property
    def items(self):
        return self.__items

    @property
    def subwindow(self):
        return self.__subwindow

    @items.setter
    def items(self, items):
        self.__items = []

        for _, item in enumerate(items):
            if isinstance(item, Text):
                item.window = self.subwindow
                self.__items.append(item)

    def display(self):
        super().display()

        string = ""
        for _, item in enumerate(self.items):
            string += item.string + self.delimiter

        string = string.strip(self.delimiter)

        self.subwindow.attron(curses.color_pair(3))
        self.subwindow.addstr(0, 0, string)
        self.subwindow.addstr(0, len(string), " " * (self.width - len(string) - 1))
        self.subwindow.attroff(curses.color_pair(3))
        self.subwindow.refresh()

    def update(self):
        self.display()

    def handle_input(self, key):
        for _, item in enumerate(self.items):
            if item.handle_input(key):
                return True
        return False


class ProgressBar(BaseWidget):
    def __init__(self, window, max, text):
        super().__init__(window)
        self.max = max
        self.__current = 0
        self.text = text
        self.template = "{:^{width}}"
        self.update()

    @property
    def current(self):
        return self.__current

    @current.setter
    def current(self, current):
        self.__current = min(self.max, max(0, current))

    def display(self):
        super().display()

        text = self.text.format(current=self.current, max=self.max)
        self.string = self.template.format(text, width=self.width)[:self.width-1]

        percent = self.current / self.max
        self.p = int(self.width * percent + 0.5)

        self.window.attron(curses.color_pair(3))
        self.window.addstr(0, 0, self.string[:self.p])
        self.window.attroff(curses.color_pair(3))

        if not self.p == self.width:
            self.window.attron(curses.color_pair(4))
            self.window.addstr(0, self.p, self.string[self.p:])
            self.window.attroff(curses.color_pair(4))

        self.window.refresh()


class TestProgressBar(ProgressBar):
    def __init__(self, window, max, text):
        super().__init__(window, max, text)

    def handle_input(self, key):
        if key == curses.KEY_DOWN:
            self.current -= 3 
            return True
        elif key == curses.KEY_UP:
            self.current += 3
            return True
        return False