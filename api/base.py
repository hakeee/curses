import curses
from typing import List, Set, Dict, Tuple, Optional, NamedTuple
from curses import panel

class BaseWidget(object):
    def __init__(self, window):
        self.window = window

    @property
    def window(self):
        return self.__window

    @window.setter
    def window(self, window):
        window.keypad(1)
        self.panel = panel.new_panel(window)
        self.panel.hide()
        panel.update_panels()

        self.height, self.width = window.getmaxyx()
        self.__window = window

    @property
    def length(self):
        return None

    def handle_input(self, key):
        return False

    def display(self):
        self.panel.top()
        self.panel.show()
        self.window.clear()
        
    def update(self):
        pass

class Text(BaseWidget):
    def __init__(self, window, string=""):
        super().__init__(window)
        self.string = string
    
    @property
    def string(self):
        return self.__string

    @string.setter
    def string(self, string):
        self.__string = string.format(width=self.width)[:self.width - 1]

    @property
    def length(self):
        return len(self.string)
    
    def display(self):
        super().display()
        self.window.addstr(0, 0, self.string)
        self.window.refresh()

class CProps(NamedTuple):
    color_pair: int = None

class Component(object):

    def __init__(self, props: CProps = CProps(), children: [] = []):
        self.props = props
        self._children: List = children

    @property
    def children(self):
        return self._children

    @children.setter
    def children(self, children: []):
        self._children = children

    def render(self, window):
        self.height, self.width = window.getmaxyx()

class View(Component):
    def __init__(self, props: CProps = CProps(), children: List[Component] = []):
        super().__init__(props, children)

    @Component.children.setter
    def children(self, children: List[Component]):
        self._children = []
        for child in self._children:
            if isinstance(child, Component):
                self._children = children

    def render(self, window):
        for component in self.children:
            if self.props.color_pair:
                window.attron(curses.color_pair(self.props.color_pair))
            component.render(window)
        
        if self.props.color_pair:
            window.attroff(curses.color_pair(self.props.color_pair))
        


class CText(Component):
    def __init__(self, props: CProps = CProps(), children: List[str] = []):
        super().__init__(props, children)

    @Component.children.setter
    def children(self, children: List[str]):
        # check so its only of type "str"
        self._children = []
        for child in self._children:
            if type(child) == str:
                self._children = children

    def render(self, window):
        super().render(window)
        if self.props.color_pair:
            window.attron(curses.color_pair(self.props.color_pair))
        for index, text in enumerate(self.children):
            if self.height > index:
                window.addstr(index, 0, text[:self.width - 1])
        
        if self.props.color_pair:
            window.attroff(curses.color_pair(self.props.color_pair))
        window.refresh()
        