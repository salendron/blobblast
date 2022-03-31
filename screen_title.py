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
import os
from image_helper import ImageHelper
from config import Config

class TitleLogo(pygame.sprite.Sprite):

    def __init__(self, width, height):
        super(TitleLogo, self).__init__()

        self.width = width
        self.height = height
        self.x = int(Config.SCREEN_WIDTH / 2) - int(width / 2)
        self.y = int(Config.SCREEN_HEIGHT / 2) - int(height / 2) - int(Config.SCREEN_HEIGHT / 10)
        
        self.image = ImageHelper.load_image(os.path.join("assets","images","title_screen", "title.bmp"), (self.width, self.height))

        self.rect = pygame.Rect(self.x, self.y, width, height)

class TitleScreen:
    """
    Implements the title screen and takes care of starting a new game or quitting the game.
    """

    def __init__(self, controller):
        self.controller = controller

        self.logo = TitleLogo(int(800 * Config.SCALE_FACTOR), int(224 * Config.SCALE_FACTOR))
        self.sprite_group = pygame.sprite.Group(self.logo)

        self.start_cooldown = 0

        font = pygame.font.SysFont("monospace", int(50 * Config.SCALE_FACTOR))
        self.label = font.render("PRESS START", True, (0, 0, 0))
        self.font_x = int(Config.SCREEN_WIDTH / 2) - int(self.label.get_width() / 2)
        self.font_y = self.logo.y + self.logo.height + int(Config.SCREEN_HEIGHT / 10)

    def process_keys(self, keys):
        if (keys[Config.P1_START] or keys[Config.P2_START]) and self.start_cooldown > Config.PAUSE_COOLDOWN:
            self.controller.dispatch_action(self.controller.ACTION_TITLE_SCREEN_START)

        if (keys[Config.P1_EXIT] or keys[Config.P2_EXIT]) and self.start_cooldown > Config.PAUSE_COOLDOWN:
            self.controller.dispatch_action(self.controller.ACTION_QUIT_GAME)

        self.start_cooldown += 1

    def draw(self, screen):
        self.sprite_group.update()
        self.sprite_group.draw(screen)

        screen.blit(self.label, (self.font_x, self.font_y))