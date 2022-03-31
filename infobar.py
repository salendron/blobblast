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

class InfoBar(pygame.sprite.Sprite):
    """
    The infobar on top of the game.
    """

    def __init__(self, player1, player2):
        super(InfoBar, self).__init__()

        self.player1 = player1
        self.player2 = player2

        self.height = int(Config.TILE_HEIGHT * 0.8)
        self.tile_width = self.height

        self.image = ImageHelper.load_image(os.path.join("assets", "images", "infobar","1.bmp"), (Config.SCREEN_WIDTH, self.height))

        self.laser_image = ImageHelper.load_image(os.path.join("assets", "images", "laser","1.bmp"), (self.height, self.tile_width))
        self.laser_image_2 = pygame.transform.flip(self.laser_image, True, False)

        self.rect = pygame.Rect(0,0,Config.SCREEN_WIDTH,self.height)
        self.mask = pygame.mask.from_surface(self.image)

        self.font = pygame.font.SysFont("monospace", int(30 * Config.SCALE_FACTOR))

        self.label_player1 = self.font.render("PLAYER 1", True, (255, 255, 255))
        self.label_player1_x =  self.tile_width * 4
        self.label_player1_y =  int((self.height / 2) - (self.label_player1.get_height() / 2))

        self.label_player2 = self.font.render("PLAYER 2", True, (255, 255, 255))
        self.label_player2_x = Config. SCREEN_WIDTH - (self.tile_width * 4) - self.label_player2.get_width()
        self.label_player2_y =  int((self.height / 2) - (self.label_player2.get_height() / 2))

        self.status = None

    def update(self):
        self.image.fill((0,0,0))
        
        # PLAYER 1
        self.image.blit(self.label_player1, (self.label_player1_x, self.label_player1_y))
        label_player1_points = self.font.render(str(self.player1.points), True, Config.BACKGROUND_COLOR)
        self.image.blit(label_player1_points, (self.label_player1_x + self.label_player1.get_width() + self.tile_width, self.label_player1_y))

        for i in range(3 - len(self.player1.lasers)):
            self.image.blit(self.laser_image, (int(((self.tile_width + (self.tile_width * 0.25))) * i + int((self.tile_width * 0.25))), 0))

        # PLAYER 2
        self.image.blit(self.label_player2, (self.label_player2_x, self.label_player2_y))
        label_player2_points = self.font.render(str(self.player2.points), True, Config.BACKGROUND_COLOR)
        self.image.blit(label_player2_points, (self.label_player2_x - self.tile_width, self.label_player2_y))

        for i in range(3 - len(self.player2.lasers)):
            self.image.blit(self.laser_image_2, (
                    int(
                        (
                            Config.SCREEN_WIDTH - (((self.tile_width + (self.tile_width * 0.25))) * i + int((self.tile_width * 0.25))) - self.tile_width
                        )
                    ), 
                    0
                )
            )

    def set_status(self, status):
        self.status = status


    