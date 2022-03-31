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

class Config:
    """
    This is the configuration for the whole game. 
    """

    SCALE_FACTOR = 0.5 # scales all elements up or down.

    FPS = 30 #frame rate
    BACKGROUND_COLOR = (252,206,141)

    SCREEN_WIDTH = 1920 
    SCREEN_HEIGHT = 1080 

    TILE_WIDTH = 64 
    TILE_HEIGHT = 64  

    ANIMATION_SPEED = int(FPS / 10)
    PLAYER_SHOOT_COOLDOWN = FPS
    BLOCK_RESPAWN_COOLDOWN = int(FPS * 1.0)
    HUNTER_SPAWN_COOLDOWN = int(FPS * 3)
    PAUSE_COOLDOWN = int(FPS)

    POINTS_PER_BLOCK = 1
    POINTS_TO_WIN = 20

    USE_CONTROLERS = False
    FULLSCREEN = False

    #keyboard controls
    K_P1_UP = pygame.K_w
    K_P1_DOWN = pygame.K_s
    K_P1_SHOOT = pygame.K_q
    K_P1_START = pygame.K_e
    K_P1_EXIT = pygame.K_d
    K_P2_UP = pygame.K_i
    K_P2_DOWN = pygame.K_k
    K_P2_SHOOT = pygame.K_u
    K_P2_START = pygame.K_o
    K_P2_EXIT = pygame.K_l

    #controller controls
    C_P1_UP = "C_P1_UP"
    C_P1_DOWN = "C_P1_DOWN"
    C_P1_SHOOT = "C_P1_SHOOT"
    C_P1_START = "C_P1_START"
    C_P1_EXIT = "C_P1_EXIT"
    C_P2_UP = "C_P2_UP"
    C_P2_DOWN = "C_P2_DOWN"
    C_P2_SHOOT = "C_P2_SHOOT"
    C_P2_START = "C_P2_START"
    C_P2_EXIT = "C_P2_EXIT"

    #default controls
    P1_UP = K_P1_UP
    P1_DOWN = K_P1_DOWN
    P1_SHOOT = K_P1_SHOOT
    P1_START = K_P1_START
    P1_EXIT = K_P1_EXIT
    P2_UP = K_P2_UP
    P2_DOWN = K_P2_DOWN
    P2_SHOOT = K_P2_SHOOT
    P2_START = K_P2_START
    P2_EXIT = K_P2_EXIT

    @classmethod
    def set_screen_size(cls, width, height, scale_factor):
        cls.SCALE_FACTOR = scale_factor
        cls.SCREEN_WIDTH = int(width * cls.SCALE_FACTOR)
        cls.SCREEN_HEIGHT = int(height * cls.SCALE_FACTOR)
        cls.TILE_WIDTH = int(64 * cls.SCALE_FACTOR)
        cls.TILE_HEIGHT = int(64 * cls.SCALE_FACTOR)

    @classmethod
    def activate_controler_mode(cls):
        cls.P1_UP = cls.C_P1_UP
        cls.P1_DOWN = cls.C_P1_DOWN
        cls.P1_SHOOT = cls.C_P1_SHOOT
        cls.P1_START = cls.C_P1_START
        cls.P1_EXIT = cls.C_P1_EXIT
        cls.P2_UP = cls.C_P2_UP
        cls.P2_DOWN = cls.C_P2_DOWN
        cls.P2_SHOOT = cls.C_P2_SHOOT
        cls.P2_START = cls.C_P2_START
        cls.P2_EXIT = cls.C_P2_EXIT