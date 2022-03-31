# BlobBlast
A simple 2-player pygame game. It can be used as a simple tutorial on pygame itself, sprites, sprite animations, joystick/controller input, or simply to play the game. It requires pygame to be installed (pip install pygame).

The goal of this game is for two player to shoot blocks in the middle of the arena and get points for doing so. You can also try to hit the other player, which will cause them to loose points and also briefly block their movement. The first player that reaches the target amount of points (see config.py) wins. If a player hits a block there is a chance for a hunter to spawn. Hunters will track the other player and will try to hit them. If they do the player looses points and also will be blocked for short period of time.

## Config
Use the values in config.py to change the configuration of the game. You can activate fullscreen mode and also controller input and so on.

## Controls
By default player 1 uses "w" as up, "s" as down, "q" to shoot, "e" as start button and "d" to end a running in game in pause mode or end the game entirely if you are on the start screen.
By default player 2 uses "i" as up, "k" as down, "u" to shoot, "o" as start button and "l" to end a running in game in pause mode or end the game entirely if you are on the start screen.

You can change these buttons in config.py. If you use controllers you can see and change how their buttons are mapped in joystick.py. There is also a debug method which can be used to debug a controller and change its mapping.
