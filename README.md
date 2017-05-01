# Tic Tac Toe Playing Robot for EXMO

This repository contains Python code for a Tic Tac Toe playing robot. And firmware used for the Makebot XY plotter.

To configure and run the program follow follwing steps.

- First assmble the plotter. And upload the `EXMO/Firmware/xybot.ino` to the plotter by connecting the plotter to your machine through COM port. Or else you can use mDraw Version 1.2.2 http://download.makeblock.com/mdraw/mDraw_V1.2.2_mac.app.zip and upload the firmware using it. 

- You can test the plotter and firmware using the above mention software and then by `EXMO/Testing code/draw from GCOde file.py` make sure to use the correct COM port to run the code.

```python
python draw from GCOde file.py -p COM3 -f test.g
```

- To configure and test machine vision module frist mount the USB web camera steadily on top and then run `EXMO/Testing code/getboardfromcamera.py`

- After configuring both modules seperately you may run the main application to fully automate the robot. 

```python
python minmax.py -p COM3
```

#### --------------------------------------
