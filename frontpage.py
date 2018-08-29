import curses
from api.bars import StatusBar
from api.base import BaseWidget, Text

class FrontPage(BaseWidget):
    def __init__(self, window, text):
        super().__init__(window)
        self.uptime = 0
        self.cursor_x = 0
        self.cursor_y = 0
        self.sb = StatusBar(self.window, " | ")
        self.text = text
        self.uptime = 0
        self.key = 0

        self.quit_text = Text(window, "Press 'q' to exit")
        self.uptime_text = Text(window, "Uptime: 0")
        self.uptime_text.template = "Uptime: {}"
        self.position_text = Text(window, "Pos: 0, 0")
        self.position_text.template = "Pos: {}, {}"

        self.sb.items = [self.quit_text, self.position_text, self.uptime_text]

        window.clear()
        window.refresh()

    def display(self):
        super().display()

        self.window.clear()

        # Declaration of strings
        title = "Curses example"[:self.width-1]
        subtitle = "Written by {}".format(self.text)[:self.width-1]
        keystr = "Last key pressed: {}".format(self.key)[:self.width-1]
        if self.key == 0:
            keystr = "No key press detected..."[:self.width-1]

        # Centering calculations
        start_x_title = int((self.width // 2) -
                            (len(title) // 2) - len(title) % 2)
        start_x_subtitle = int((self.width // 2) -
                                (len(subtitle) // 2) - len(subtitle) % 2)
        start_x_keystr = int((self.width // 2) -
                                (len(keystr) // 2) - len(keystr) % 2)
        start_y = int((self.height // 2) - 2)

        # Rendering some text
        whstr = "Width: {}, Height: {}".format(self.width, self.height)
        self.window.addstr(0, 0, whstr, curses.color_pair(1))

        # Render status bar
        self.sb.display()

        # Turning on attributes for title
        self.window.attron(curses.color_pair(2))
        self.window.attron(curses.A_BOLD)

        # Rendering title
        self.window.addstr(start_y, start_x_title, title)

        # Turning off attributes for title
        self.window.attroff(curses.color_pair(2))
        self.window.attroff(curses.A_BOLD)

        # Print rest of text
        self.window.addstr(start_y + 1, start_x_subtitle, subtitle)
        self.window.addstr(start_y + 3, (self.width // 2) - 2, '-' * 4)
        self.window.addstr(start_y + 5, start_x_keystr, keystr)
        self.window.move(self.cursor_y, self.cursor_x)

        # Refresh the screen
        self.window.refresh()

        return False
    
    def update(self):
        self.uptime +=1
        self.uptime_text.string = self.uptime_text.template.format(self.uptime)
        self.position_text.string = self.position_text.template.format(self.cursor_y, self.cursor_x)
        self.sb.update()

    
    def handle_input(self, key):
        if key == curses.KEY_DOWN:
            self.cursor_y = self.cursor_y + 1
        elif key == curses.KEY_UP:
            self.cursor_y = self.cursor_y - 1
        elif key == curses.KEY_RIGHT:
            self.cursor_x = self.cursor_x + 1
        elif key == curses.KEY_LEFT:
            self.cursor_x = self.cursor_x - 1

        self.cursor_x = min(self.width-1, max(0, self.cursor_x))
        self.cursor_y = min(self.height-1, max(0, self.cursor_y))

        self.position_text.text = self.position_text.template.format(self.cursor_y, self.cursor_x)
        self.sb.update()

        return False
