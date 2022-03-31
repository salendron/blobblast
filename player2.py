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
from config import Config
from player import Player

class Player2(Player):
    """
    Player2 inherits Player, but flips all the images and also sets its initial position to the lower right corner
    """

    def __init__(self):
        super(Player2, self).__init__()

        self.rect = pygame.Rect(Config.SCREEN_WIDTH - (2 * Config.TILE_WIDTH), Config.SCREEN_HEIGHT - Config.TILE_HEIGHT - int(Config.TILE_HEIGHT * 0.6), Config.TILE_WIDTH, Config.TILE_HEIGHT)

        self.flip_images()

    def flip_images(self):
        self.image_idle = pygame.transform.flip(self.image_idle, True, False)

        for i in range(len(self.images_shoot)):
            self.images_shoot[i] = pygame.transform.flip(self.images_shoot[i], True, False)

        for i in range(len(self.images_hit)):
            self.images_hit[i] = pygame.transform.flip(self.images_hit[i], True, False)

    