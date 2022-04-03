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

class Hunter(pygame.sprite.Sprite):
    """
    Hunters have a chance to spawn when a block is hit. They will travel into the direction
    of the other player and try to hit him.
    """

    STATE_REVERSE = 0
    STATE_HUNTING = 1

    def __init__(self, screen, target, right_to_left):
        super(Hunter, self).__init__()

        self.screen = screen
        self.target = target

        self.velocity = int(Config.SCREEN_WIDTH / (4 * Config.FPS))

        self.images_animation = [
            ImageHelper.load_image(os.path.join("assets", "images", "hunter", "1.bmp"), (Config.TILE_WIDTH, Config.TILE_HEIGHT)),
            ImageHelper.load_image(os.path.join("assets", "images", "hunter", "2.bmp"), (Config.TILE_WIDTH, Config.TILE_HEIGHT)),
            ImageHelper.load_image(os.path.join("assets", "images", "hunter", "3.bmp"), (Config.TILE_WIDTH, Config.TILE_HEIGHT)),
            ImageHelper.load_image(os.path.join("assets", "images", "hunter", "4.bmp"), (Config.TILE_WIDTH, Config.TILE_HEIGHT)),
            ImageHelper.load_image(os.path.join("assets", "images", "hunter", "5.bmp"), (Config.TILE_WIDTH, Config.TILE_HEIGHT)),
            ImageHelper.load_image(os.path.join("assets", "images", "hunter", "6.bmp"), (Config.TILE_WIDTH, Config.TILE_HEIGHT)),
            ImageHelper.load_image(os.path.join("assets", "images", "hunter", "7.bmp"), (Config.TILE_WIDTH, Config.TILE_HEIGHT)),
            ImageHelper.load_image(os.path.join("assets", "images", "hunter", "8.bmp"), (Config.TILE_WIDTH, Config.TILE_HEIGHT))
        ]

        self.image = self.images_animation[0]

        self.animation_frame_index = 0
        self.animation_frame_count = 0

        self.state = Hunter.STATE_HUNTING
        self.reverse_frame_count = 0
        self.reverse_frame_cooldown = Config.FPS

        if right_to_left:
            self.velocity = self.velocity * -1

        self.rect = pygame.Rect(Config.TILE_WIDTH, Config.TILE_HEIGHT, Config.TILE_WIDTH, Config.TILE_HEIGHT)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        if self.animation_frame_count < Config.ANIMATION_SPEED:
            self.animation_frame_index += 1
            self.animation_frame_count = 0
        else:
            self.animation_frame_count += 1

        if self.animation_frame_index >= len(self.images_animation):
            self.animation_frame_index = 0

        self.image = self.images_animation[self.animation_frame_index]

        if self.rect.x <= Config.SCREEN_WIDTH + Config.TILE_WIDTH and self.rect.x > (0 - Config.TILE_WIDTH):
            self.rect.x += self.velocity
        else:
            self.screen.remove_hunter(self)

        if self.rect.x >= Config.SCREEN_WIDTH * 0.25 and self.rect.x <= Config.SCREEN_WIDTH * 0.75:
            if self.rect.y < self.target.rect.y:
                self.rect.y += abs(self.velocity)
            
            if self.rect.y > self.target.rect.y:
                self.rect.y -= abs(self.velocity)

        if self.state == Hunter.STATE_REVERSE:
            self.reverse_frame_count += 1

            if self.reverse_frame_count >= self.reverse_frame_cooldown:
                self.state = Hunter.STATE_HUNTING
                self.reverse_frame_count = 0

    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def reverse(self):
        if self.state == Hunter.STATE_HUNTING:
            self.state = Hunter.STATE_REVERSE
            self.reverse_frame_count = 0
            self.velocity = self.velocity * -1

    