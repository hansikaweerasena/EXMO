import serial
import time
import argparse


def plot(filename, port):
    print ("USB Port: %s" % port )
    print ("Gcode file: %s" % filename )
    s = serial.Serial(port,115200)
    print 'Opening Serial Port'
    f = open(filename,'r');
    print 'Opening gcode file'
    s.write("\n\r\n\r") # Hit enter a few times to wake the Printrbot
    time.sleep(2)   # Wait for Printrbot to initialize
    s.flushInput()  # Flush startup text in serial input
    print 'Sending gcode'

    # Stream g-code
    for line in f:
        l = removeComment(line)
        l = l.strip() # Strip all EOL characters for streaming
        if  (l.isspace()==False and len(l)>0) :
            print 'Sending: ' + l
            s.write(l + '\n') # Send g-code block
            grbl_out = s.readline() # Wait for response with carriage return
            while (grbl_out != "OK\r\n"):
                grbl_out = s.readline()
            print ' : ' + grbl_out.strip()
 
    # Close file and serial port
    f.close()
    s.close()

def removeComment(string):
	if (string.find(';')==-1):
		return string
	else:
		return string[:string.index(';')]
 
# parser = argparse.ArgumentParser(description='This is a basic gcode sender. http://crcibernetica.com')
# parser.add_argument('-p','--port',help='Input USB port',required=True)
# parser.add_argument('-f','--file',help='Gcode file name',required=True)
# args = parser.parse_args()

# plot(args.file, args.port)