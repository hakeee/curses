import sys
import os
import curses
from threading import Thread, Event
import time
from api.bars import StatusBar, TestProgressBar
from api.base import BaseWidget, Text, CText, CProps, View
from api.menu import Menu
from api.tabbar import Tabbar
from frontpage import FrontPage

class App:
    def __init__(self, stdscr):
        curses.curs_set(0)
        self.stdscr = stdscr
        self.tabbar = Tabbar(stdscr)
        self.tabbar.subwindow
        self.key = 0
        self.update_thread = Thread(target=self.update)
        self.view = View(props=CProps(color_pair=3), children=[
            CText(props=CProps(color_pair=1), children=[
                "Text"
            ]),
            CText(children=[
                "Te",
                "Text2",
                "Text3"
            ]),
            CText(props=CProps(color_pair=2), children=[
                "T",
                "Text2"
            ]),
            CText(children=[
                "",
                "",
                "",
                "Text4"
            ]),
        ])

        # Clear and refresh the screen for a blank canvas
        stdscr.clear()
        stdscr.refresh()

        # Start colors in curses
        curses.start_color()
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)

        # Set all tabs
        self.tabbar.items = [
            ("Frontpage" , FrontPage(self.tabbar.subwindow, "first")),
            ("Progressbar ", TestProgressBar(self.tabbar.subwindow, 100, "second {current}/{max}")),
            ("Text ", Text(self.tabbar.subwindow, "second {width}"))
        ]

        self.update_thread.start()
        while (self.key != ord('q')):
            self.tabbar.handle_input(self.key)
            self.tabbar.display()
            self.view.render(self.tabbar.subwindow)

            curses.doupdate()

            # Wait for next input
            self.key = self.stdscr.getch()
        
        self.update_thread.join()

    def update(self):
        while (self.key != ord('q')):
            time.sleep(1)
            self.tabbar.update()

def main():
    curses.wrapper(App)


if __name__ == "__main__":
    main()
