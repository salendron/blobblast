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

import sys
import pygame
from config import Config

class Joystick:
    """
    A helper for pygame.joystick that requires two connected game controllers
    It will read all command from the game pads and map them to defined events
    that can be used like pygame.events later on in the game.
    To make this work with a specific game pad, use the debug method,
    comment in and out what you want to debug, and then change the mapping in
    get_events to fit your controllers.
    """

    def __init__(self):
        self.joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

        for joy in self.joysticks:
            joy.init()

        if len(self.joysticks) != 2:
            print("Could not detect two controllers!")
            sys.exit(0)

    def get_events(self):
        events = {}

        # joaystick 1
        j_1 = self.joysticks[0]
        
        # up / down
        j_1_axis_1 = round(j_1.get_axis(1))
        events[Config.P1_UP] = True if j_1_axis_1 < 0 else False
        events[Config.P1_DOWN] = True if j_1_axis_1 > 0 else False

        # shoot, pause, exit
        events[Config.P1_SHOOT] = True if j_1.get_button(0) == 1 else False
        events[Config.P1_START] = True if j_1.get_button(6) == 1 else False
        events[Config.P1_EXIT] = True if j_1.get_button(4) == 1 else False

        # joaystick 2
        j_2 = self.joysticks[1]
        
        # up / down
        j_2_axis_1 = round(j_2.get_axis(1))
        events[Config.P2_UP] = True if j_2_axis_1 < 0 else False
        events[Config.P2_DOWN] = True if j_2_axis_1 > 0 else False

        # shoot, pause, exit
        events[Config.P2_SHOOT] = True if j_2.get_button(0) == 1 else False
        events[Config.P2_START] = True if j_2.get_button(6) == 1 else False
        events[Config.P2_EXIT] = True if j_2.get_button(4) == 1 else False

        #if len(events.keys()) > 0:
        print(events)

        return events

    def debug(self):
        # joystick buttons
        for j in range(len(self.joysticks)):
            joystick = pygame.joystick.Joystick(j)
            #name = joystick.get_name()
            #print("Joystick name: {}".format(name) )
        
            #axes = joystick.get_numaxes()
            #print("Number of axes: {}".format(axes) )
        
            #for i in range( axes ):
            #    axis = joystick.get_axis( i )
            #    print("Axis {} value: {:>6.0f}".format(i, axis) )
        
            buttons = joystick.get_numbuttons()
            #print("Number of buttons: {}".format(buttons) )
        
            for i in range( buttons ):
                button = joystick.get_button( i )
                print("Button {:>2} value: {}".format(i,button) )
        
            #hats = joystick.get_numhats()
            #print("Number of hats: {}".format(hats) )
        
            #for i in range( hats ):
            #    hat = joystick.get_hat( i )
            #    print("Hat {} value: {}".format(i, str(hat)) )

