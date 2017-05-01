# Tic Tac Toe Playing Robot for EXMO

This repository contains Python code for a Tic Tac Toe playing robot. And firmware used for the Makebot XY plotter.

To configure and run the program follow follwing steps.

- First assmble the plotter. And upload the `EXMO/Firmware/xybot.ino` to the plotter by connecting the plotter to your machine through COM port. Or else you can use mDraw Version 1.2.2 http://download.makeblock.com/mdraw/mDraw_V1.2.2_mac.app.zip and upload the firmware using it. 

- You can test the plotter and firmware using the above mention software and then by `EXMO/Testing code/draw from GCOde file.py` make sure to use the correct COM port to run the code.

`python draw from GCOde file.py -p COM3 -f test.g`

- To configure and test machine vision module frist mount the USB web camera steadily on top and then run `EXMO/Testing code/getboardfromcamera.py`

- After configuring both modules seperately you may run the main application to fully automate the robot. 

`python minmax.py -p COM3`

#### Other important points

* count.txt and wins.txt will save the number of times game played and number of wins
* IF you want to reset the counts and wins manually reset them before playing the game
* https://notezbyhanz.wordpress.com/2017/04/30/tic-tac-toe-playing-robot-at-exmo2017/ will have a demostation how the code works.
