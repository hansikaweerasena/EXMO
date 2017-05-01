# Tic Tac Toe Playing Robot for EXMO

This repository contains Python code for a Tic Tac Toe playing robot. And firmware used for the Makebot XY plotter.

To configure and run the program follow follwing steps.

- First assmble the plotter. And upload the `EXMO/Firmware/xybot.ino` to the plotter by connecting the plotter to your machine through COM port. Or else you can use mDraw Version 1.2.2 http://download.makeblock.com/mdraw/mDraw_V1.2.2_mac.app.zip and upload the firmware using it. 

- You can test the plotter and firmware using the above mention software and then by `EXMO/Testing code/draw from GCOde file.py` make sure to use the correct COM port to run the code.
  - Serial program
  - Parallel program (based on Pthreads) with one mutex for the entire linked list
  - Parallel program (based on Pthreads) with read-write locks for the entire linked list
  
All these implementation of the linked list supports Member( ), Insert( ), and Delete( ) functions of the linked list.

- timer.h -: Header file for calculating execution time.
- run.sh -: Shell script to run all combinations and get results.

1. Run the run.sh file using following command and get the command line output to text file.
	
	`./run.sh > output.txt`

#### ------------- Executing serial version -----------------------

1. Compile the serial_version.c using following command.
```C
	gcc serial_version.c -g -Wall -o serial_version -lpthread -lm
```
2. Run the serial_version using following command with wanted parameters.  
	./serial_version <m_f> <i_f> <d_f> <no_of_samples>  
	eg -: `./serial_version 0.99 0.005 0.005 200`


* m_f -: fraction of member operations
* m_i -: fraction of insert operations
* m_d -: fraction of delete operations
