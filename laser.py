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
from config import Config
from image_helper import ImageHelper

class Laser(pygame.sprite.Sprite):
    """
    A laser shot by a player
    """

    def __init__(self, player, right_to_left):
        super(Laser, self).__init__()

        self.player = player

        self.velocity = int(Config.SCREEN_WIDTH / (4 * Config.FPS))

        self.image = ImageHelper.load_image(os.path.join("assets", "images", "laser","1.bmp"), (Config.TILE_WIDTH, Config.TILE_HEIGHT))

        if right_to_left: #player 2
            self.velocity = self.velocity * -1
            self.image = pygame.transform.flip(self.image, True, False)

        self.rect = pygame.Rect(Config.TILE_WIDTH, Config.TILE_HEIGHT, Config.TILE_WIDTH, Config.TILE_HEIGHT)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        if self.rect.x <= Config.SCREEN_WIDTH + Config.TILE_WIDTH and self.rect.x > (0 - Config.TILE_WIDTH):
            self.rect.x += self.velocity
        else:
            self.player.remove_laser(self)

    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

    