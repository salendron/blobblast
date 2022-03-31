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
import pygame
import os
from config import Config
from image_helper import ImageHelper
from laser import Laser


class Player(pygame.sprite.Sprite):
    """
    Super of the two players, implementing everything a player needs to work.
    See player1.py and player2.py for the differences.
    """

    STATE_IDLE = 0
    STATE_SHOOT = 1
    STATE_HIT = 2

    def __init__(self):
        super(Player, self).__init__()

        self.velocity = int((4 * 30) / Config.FPS)

        self.image_idle = ImageHelper.load_image(os.path.join("assets", "images", "player1","idle.bmp"), (Config.TILE_WIDTH, Config.TILE_HEIGHT))

        #shoot animation
        self.images_shoot = [
            ImageHelper.load_image(os.path.join("assets", "images", "player1", "shoot", "1.bmp"), (Config.TILE_WIDTH, Config.TILE_HEIGHT)),
            ImageHelper.load_image(os.path.join("assets", "images", "player1", "shoot", "2.bmp"), (Config.TILE_WIDTH, Config.TILE_HEIGHT)),
            ImageHelper.load_image(os.path.join("assets", "images", "player1", "shoot", "3.bmp"), (Config.TILE_WIDTH, Config.TILE_HEIGHT)),
            ImageHelper.load_image(os.path.join("assets", "images", "player1", "shoot", "4.bmp"), (Config.TILE_WIDTH, Config.TILE_HEIGHT)),
            ImageHelper.load_image(os.path.join("assets", "images", "player1", "shoot", "5.bmp"), (Config.TILE_WIDTH, Config.TILE_HEIGHT)),
            ImageHelper.load_image(os.path.join("assets", "images", "player1", "shoot", "6.bmp"), (Config.TILE_WIDTH, Config.TILE_HEIGHT)),
            ImageHelper.load_image(os.path.join("assets", "images", "player1", "shoot", "7.bmp"), (Config.TILE_WIDTH, Config.TILE_HEIGHT))
        ]

        #hit animation
        self.images_hit = [
            ImageHelper.load_image(os.path.join("assets", "images", "player1", "hit", "1.bmp"), (Config.TILE_WIDTH, Config.TILE_HEIGHT)),
            ImageHelper.load_image(os.path.join("assets", "images", "player1", "hit", "2.bmp"), (Config.TILE_WIDTH, Config.TILE_HEIGHT)),
            ImageHelper.load_image(os.path.join("assets", "images", "player1", "hit", "3.bmp"), (Config.TILE_WIDTH, Config.TILE_HEIGHT)),
            ImageHelper.load_image(os.path.join("assets", "images", "player1", "hit", "4.bmp"), (Config.TILE_WIDTH, Config.TILE_HEIGHT)),
            ImageHelper.load_image(os.path.join("assets", "images", "player1", "hit", "5.bmp"), (Config.TILE_WIDTH, Config.TILE_HEIGHT)),
            ImageHelper.load_image(os.path.join("assets", "images", "player1", "hit", "6.bmp"), (Config.TILE_WIDTH, Config.TILE_HEIGHT)),
            ImageHelper.load_image(os.path.join("assets", "images", "player1", "hit", "7.bmp"), (Config.TILE_WIDTH, Config.TILE_HEIGHT)),
            ImageHelper.load_image(os.path.join("assets", "images", "player1", "hit", "8.bmp"), (Config.TILE_WIDTH, Config.TILE_HEIGHT))
        ]

        self.image = self.image_idle
        self.state = Player.STATE_IDLE

        self.animation_frame_index = 0
        self.animation_frame_count = 0
        self.shoot_cooldown_frames = 0
        self.shoot_cooldown = False

        self.lasers = []
        self.points = 0

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        if self.state == Player.STATE_IDLE:
            self.animation_frame_index = 0
            self.animation_frame_count = 0
            self.image = self.image_idle
        
        if self.state == Player.STATE_SHOOT:
            self.image = self.images_shoot[self.animation_frame_index]

            if self.animation_frame_count < Config.ANIMATION_SPEED:
                self.animation_frame_index += 1
                self.animation_frame_count = 0
            else:
                self.animation_frame_count += 1

            if self.animation_frame_index >= len(self.images_shoot):
                self.state = Player.STATE_IDLE

        if self.state == Player.STATE_HIT:
            self.image = self.images_hit[self.animation_frame_index]

            if self.animation_frame_count < Config.ANIMATION_SPEED:
                self.animation_frame_index += 1
                self.animation_frame_count = 0
            else:
                self.animation_frame_count += 1

            if self.animation_frame_index >= len(self.images_hit):
                self.state = Player.STATE_IDLE

        if self.shoot_cooldown:
            self.shoot_cooldown_frames += 1

            if self.shoot_cooldown_frames >= Config.PLAYER_SHOOT_COOLDOWN:
                self.shoot_cooldown = False
                self.shoot_cooldown_frames = 0

    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def move_up(self):
        if self.state != Player.STATE_HIT:
            if self.rect.y > Config.TILE_HEIGHT:
                self.rect.y -= self.velocity
            else:
                self.rect.y = Config.TILE_HEIGHT 

    def move_down(self):
        if self.state != Player.STATE_HIT:
            if self.rect.y < Config.SCREEN_HEIGHT - Config.TILE_HEIGHT:
                self.rect.y += self.velocity
            else:
                self.rect.y = Config.SCREEN_HEIGHT - Config.TILE_HEIGHT

    def shoot(self, right_to_left):
        if not self.shoot_cooldown and len(self.lasers) < 3 and self.state != Player.STATE_HIT:
            self.shoot_cooldown = True
            self.state = Player.STATE_SHOOT

            laser = Laser(self, right_to_left)
            laser.set_position(self.rect.x, self.rect.y)
            self.lasers.append(laser)

    def remove_laser(self, laser):
        self.lasers.remove(laser)

    def score(self):
        self.points += Config.POINTS_PER_BLOCK

    def take_hit(self):
        self.points -= Config.POINTS_PER_BLOCK
        self.state = Player.STATE_HIT
        self.animation_frame_index = 0
        self.animation_frame_count = 0

        