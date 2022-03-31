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

class Block(pygame.sprite.Sprite):
    """
    Implements a block that can be hit by a player's.
    """

    STATE_IDLE = 0
    STATE_FADE_IN = 1
    STATE_FADE_OUT = 2

    def __init__(self, screen):
        super(Block, self).__init__()

        self.screen = screen

        self.image_idle = ImageHelper.load_image(os.path.join("assets", "images", "block","1.bmp"), (Config.TILE_WIDTH, Config.TILE_HEIGHT))

        #shoot animation
        self.images_animation = [
            ImageHelper.load_image(os.path.join("assets", "images", "block", "2.bmp"), (Config.TILE_WIDTH, Config.TILE_HEIGHT)),
            ImageHelper.load_image(os.path.join("assets", "images", "block", "3.bmp"), (Config.TILE_WIDTH, Config.TILE_HEIGHT)),
            ImageHelper.load_image(os.path.join("assets", "images", "block", "4.bmp"), (Config.TILE_WIDTH, Config.TILE_HEIGHT)),
            ImageHelper.load_image(os.path.join("assets", "images", "block", "5.bmp"), (Config.TILE_WIDTH, Config.TILE_HEIGHT)),
            ImageHelper.load_image(os.path.join("assets", "images", "block", "6.bmp"), (Config.TILE_WIDTH, Config.TILE_HEIGHT)),
            ImageHelper.load_image(os.path.join("assets", "images", "block", "7.bmp"), (Config.TILE_WIDTH, Config.TILE_HEIGHT)),
            ImageHelper.load_image(os.path.join("assets", "images", "block", "8.bmp"), (Config.TILE_WIDTH, Config.TILE_HEIGHT))
        ]

        self.image = self.image_idle # initial image
        self.state = Block.STATE_FADE_IN # initial state

        # animation starts at last frame, since the block first fades in
        self.animation_frame_index = len(self.images_animation) - 1
        self.animation_frame_count = 0

        self.rect = pygame.Rect(Config.TILE_WIDTH, Config.TILE_HEIGHT, Config.TILE_WIDTH, Config.TILE_HEIGHT)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        if self.state == Block.STATE_IDLE: # block does nothing
            self.animation_frame_index = 0
            self.animation_frame_count = 0
            self.image = self.image_idle
        
        if self.state == Block.STATE_FADE_IN: # fade in animation
            self.image = self.images_animation[self.animation_frame_index]

            if self.animation_frame_count < Config.ANIMATION_SPEED:
                self.animation_frame_index -= 1
                self.animation_frame_count = 0
            else:
                self.animation_frame_count += 1

            if self.animation_frame_index <= 0:
                self.state = Block.STATE_IDLE

        if self.state == Block.STATE_FADE_OUT: # fade out animation
            self.image = self.images_animation[self.animation_frame_index]

            if self.animation_frame_count < Config.ANIMATION_SPEED:
                self.animation_frame_index += 1
                self.animation_frame_count = 0
            else:
                self.animation_frame_count += 1

            if self.animation_frame_index >= len(self.images_animation):
                self.screen.remove_block(self)

    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

    