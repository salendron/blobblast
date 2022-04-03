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
from hunter import Hunter
from infobar import InfoBar
from player1 import Player1
from player2 import Player2
from block import Block
import random


class GameScreen:
    """
    Implements the game arena and also controlls the whole game by taking
    care of collions, pause, giving points to players, spawning blocks and hunters, ....
    """

    def __init__(self, controller):
        self.running = True

        self.controller = controller

        self.player1 = Player1()
        self.player2 = Player2()

        self.winner = None

        self.blocks = [None, None, None, None, None, None, None, None, None, None]

        self.hunters = [None, None, None]

        self.sprite_group = None

        self.block_cooldown = 0

        self.hunter_cooldown = 0

        self.pause_cooldown = 0

        self.infobar = InfoBar(self.player1, self.player2)

        self.font = pygame.font.SysFont("monospace", int(30 * Config.SCALE_FACTOR))

        self.initialize_blocks()

    def process_keys(self, keys):
        if self.running:
            if keys[Config.P1_UP]:
                self.player1.move_up()
            
            if keys[Config.P1_DOWN]:
                self.player1.move_down()

            if keys[Config.P1_SHOOT]:
                self.player1.shoot(False)

            if keys[Config.P2_UP]:
                self.player2.move_up()
            
            if keys[Config.P2_DOWN]:
                self.player2.move_down()

            if keys[Config.P2_SHOOT]:
                self.player2.shoot(True)

        if keys[Config.P1_START] or keys[Config.P2_START]:
            if self.winner != None:
                self.controller.dispatch_action(1) #back to tile screen
            else:
                self.toogle_pause()

        if keys[Config.P1_EXIT] or keys[Config.P2_EXIT]:
            if self.running == False:
                self.controller.dispatch_action(1) #back to tile screen

    def draw(self, screen):
        if self.running:
            sprites = []

            sprites += [h for h in self.hunters if h != None]
            
            for laser in self.player1.lasers:
                sprites.append(laser)

            for laser in self.player2.lasers:
                sprites.append(laser)

            sprites.append(self.player1)
            sprites.append(self.player2)

            sprites += [b for b in self.blocks if b != None]

            sprites.append(self.infobar)

            self.sprite_group = pygame.sprite.Group(sprites)

            self.check_winner()
            self.check_block_collisions()
            self.check_player_collisions()
            self.respawn_blocks()
            self.check_hunter_collisions()

            self.hunter_cooldown += 1

            self.sprite_group.update()
            self.sprite_group.draw(screen)
        else:
            self.sprite_group.draw(screen)

            if self.winner == None: #PAUSE
                label_status = self.font.render("PAUSED", True, (255, 255, 255))
                label_status_x =  int((Config.SCREEN_WIDTH / 2) - (label_status.get_width() / 2))
                label_status_y =  int(((Config.TILE_HEIGHT * 0.8) / 2) - (label_status.get_height() / 2))
                self.controller.screen.blit(label_status, (label_status_x, label_status_y))
            else: # GAME ENDED
                winner_name = "PLAYER 1"
                if self.winner == self.player2:
                    winner_name = "PLAYER 2"
                
                label_status = self.font.render(f"{winner_name} won!", True, (255, 255, 255))
                label_status_x =  int((Config.SCREEN_WIDTH / 2) - (label_status.get_width() / 2))
                label_status_y =  int(((Config.TILE_HEIGHT * 0.8) / 2) - (label_status.get_height() / 2))
                self.controller.screen.blit(label_status, (label_status_x, label_status_y))
        
        self.pause_cooldown += 1

    def initialize_blocks(self):
        y = Config.TILE_HEIGHT
        x = int((Config.SCREEN_WIDTH / 2) - (Config.TILE_WIDTH / 2))

        for i in range(10):
            block = Block(self)
            block.set_position(x, y)
            self.blocks[i] = block

            y += Config.TILE_HEIGHT + int(Config.TILE_HEIGHT * 0.6)

    def respawn_blocks(self):
        if self.block_cooldown > Config.BLOCK_RESPAWN_COOLDOWN:
            rand_index = random.randint(0, len(self.blocks) - 1)
            if self.blocks[rand_index] == None:
                x = int((Config.SCREEN_WIDTH / 2) - (Config.TILE_WIDTH / 2))
                y = int(Config.TILE_HEIGHT + (Config.TILE_HEIGHT * rand_index) + ((Config.TILE_HEIGHT * 0.6) * rand_index))

                block = Block(self)
                block.set_position(x, y)
                self.blocks[rand_index] = block

            self.block_cooldown = 0
        else:
            self.block_cooldown += 1  

    def spawn_hunter(self, x, y, target, right_to_left):
        if self.hunter_cooldown > Config.HUNTER_SPAWN_COOLDOWN:
            rand_index = random.randint(0, len(self.hunters) - 1)
            if self.hunters[rand_index] == None:

                hunter = Hunter(self, target, right_to_left)
                hunter.set_position(x, y)
                self.hunters[rand_index] = hunter

            self.hunter_cooldown = 0
                
    def check_block_collisions(self):
        #player 1
        for laser in self.player1.lasers:
            for block in self.blocks:
                if block != None and block.state == Block.STATE_IDLE:
                    if self.does_collide(laser, block):
                        block.state = Block.STATE_FADE_OUT
                        self.player1.remove_laser(laser)
                        self.player1.score()
                        self.spawn_hunter(block.rect.x, block.rect.y, self.player2, False)

        #player 2
        for laser in self.player2.lasers:
            for block in self.blocks:
                if block != None and block.state == Block.STATE_IDLE:
                    if self.does_collide(laser, block):
                        block.state = Block.STATE_FADE_OUT
                        self.player2.remove_laser(laser)
                        self.player2.score()
                        self.spawn_hunter(block.rect.x, block.rect.y, self.player1, True)

    def check_hunter_collisions(self):
        #player 1
        for laser in self.player1.lasers:
            for hunter in self.hunters:
                if hunter != None:
                    if self.does_collide(laser, hunter):
                        hunter.reverse()
                        self.player1.remove_laser(laser)

        #player 2
        for laser in self.player2.lasers:
            for hunter in self.hunters:
                if hunter != None:
                    if self.does_collide(laser, hunter):
                        hunter.reverse()
                        self.player2.remove_laser(laser)

    def check_player_collisions(self):
        #player 1 hits player 2
        for laser in self.player1.lasers:
            if self.does_collide(laser, self.player2):
                self.player1.remove_laser(laser)
                self.player1.score()
                self.player2.take_hit()

        #player 2 hits player 1
        for laser in self.player2.lasers:
            if self.does_collide(laser, self.player1):
                self.player2.remove_laser(laser)
                self.player2.score()
                self.player1.take_hit()

        #hunter hits player 
        for hunter in [h for h in self.hunters if h != None]:
            if self.does_collide(hunter, self.player1):
                self.remove_hunter(hunter)
                self.player1.take_hit()

            if self.does_collide(hunter, self.player2):
                self.remove_hunter(hunter)
                self.player2.take_hit()

    def check_winner(self):
        if self.player1.points >= Config.POINTS_TO_WIN:
            self.winner = self.player1
            self.running = False

        if self.player2.points >= Config.POINTS_TO_WIN:
            self.winner = self.player2
            self.running = False

    def remove_block(self, block):
        block_index = self.blocks.index(block)
        self.blocks[block_index] = None

    def remove_hunter(self, hunter):
        hunter_index = self.hunters.index(hunter)
        self.hunters[hunter_index] = None

    def toogle_pause(self):
        if self.pause_cooldown >= Config.PAUSE_COOLDOWN:
            if self.running:
                self.running = False
                self.infobar.set_status("PAUSED")
            else:
                self.running = True
                self.infobar.set_status(None)

            self.pause_cooldown = 0

    def does_collide(self, obj1, obj2):
        offset_x = obj2.rect.x - obj1.rect.x
        offset_y = obj2.rect.y - obj1.rect.y
        return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None
