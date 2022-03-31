"""
MIT License
Copyright (c) 2022 Bruno Hautzenberger

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import pygame
from pygame.locals import *
from config import Config
from screen_game import GameScreen
from screen_title import TitleScreen

class Controller:
    """
    Is used to control which scene is currently displayed and also draws the background.
    """

    ACTION_TITLE_SCREEN_START = 0
    ACTION_TITLE_SCREEN_TITLE = 1
    ACTION_QUIT_GAME = 2

    def __init__(self, screen):
        self.screen = screen
        self.is_running = True
        self.current_screen = TitleScreen(self)

    def process_keys(self, keys):
        self.current_screen.process_keys(keys)

    def dispatch_action(self, action):
        if action == self.ACTION_TITLE_SCREEN_START:
            self.current_screen = GameScreen(self)

        if action == self.ACTION_TITLE_SCREEN_TITLE:
            self.current_screen = TitleScreen(self)

        if action == self.ACTION_QUIT_GAME:
            self.is_running = False   

    def draw(self):
        self.screen.fill(Config.BACKGROUND_COLOR)
        self.current_screen.draw(self.screen)
        pygame.display.flip()
