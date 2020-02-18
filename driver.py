#[[R1, 00-1,00-2,D1], [R2, 01-0, 01-3, D2]]
#(x,y) for corrdinates
#start at R1 go to obstacle 0 point 1 go to obstacle 0 point 2 go to destination one repeat for robot 2

from Tkinter import *
import tkMessageBox
import tkSimpleDialog
import time
import json
import math
import numpy as np 

import struct
import sys, glob # for listing serial ports

try:
    import serial
except ImportError:
    tkMessageBox.showerror('Import error', 'Please install pyserial.')
    raise

connection = None
robotName = "R1"
robotPathFULL = [['R1', '00-1','00-2','D1'], ['R2', '01-0', '01-3', 'D2']]
robotPath = ['R1', '00-1','00-2','D1']
inputValues = None
robotRoute = None
currentFacingAngle = 90


TEXTWIDTH = 40 # window width, in characters
TEXTHEIGHT = 16 # window height, in lines

VELOCITYCHANGE = 200
ROTATIONCHANGE = 300

helpText = """\
Supported Keys:
P\tPassive
S\tSafe
Space\tBeep
Arrows\tMotion
If nothing happens after you connect, try pressing 'P' and then 'S' to get into safe mode.
"""
class Route:
    def __init__(self,name, start):
        self.name = name
        self.start = start
        self.end = None
        self.path = []
        self.path.append(start)

    def setEnd(self,arr):
        self.end = arr

    def addToPath(self,arr):
        self.path.append(arr)
        #self.path = path.append(start[0])

class Input:
    def __init__(self,data):
        self.__dict__ = json.loads(data)
       

class TetheredDriveApp(Tk):
    # static variables for keyboard callback -- I know, this is icky
    callbackKeyUp = False
    callbackKeyDown = False
    callbackKeyLeft = False
    callbackKeyRight = False
    callbackKeyLastDriveCommand = ''

    def __init__(self):
        Tk.__init__(self)
        self.title("iRobot Create 2 Tethered Drive")
        self.option_add('*tearOff', FALSE)

        self.menubar = Menu()
        self.configure(menu=self.menubar)

        createMenu = Menu(self.menubar, tearoff=False)
        self.menubar.add_cascade(label="Create", menu=createMenu)

        createMenu.add_command(label="Connect", command=self.onConnect)
        createMenu.add_command(label="Help", command=self.onHelp)
        createMenu.add_command(label="Quit", command=self.onQuit)

        self.text = Text(self, height = TEXTHEIGHT, width = TEXTWIDTH, wrap = WORD)
        self.scroll = Scrollbar(self, command=self.text.yview)
        self.text.configure(yscrollcommand=self.scroll.set)
        self.text.pack(side=LEFT, fill=BOTH, expand=True)
        self.scroll.pack(side=RIGHT, fill=Y)

        self.text.insert(END, helpText)

        self.bind("<Key>", self.callbackKey)
        self.bind("<KeyRelease>", self.callbackKey)

    # sendCommandASCII takes a string of whitespace-separated, ASCII-encoded base 10 values to send
    def sendCommandASCII(self, command):
        cmd = ""
        for v in command.split():
            cmd += chr(int(v))

        self.sendCommandRaw(cmd)

    # sendCommandRaw takes a string interpreted as a byte array
    def sendCommandRaw(self, command):

        global connection

        try:
            if connection is not None:
                connection.write(command)
            else:
                tkMessageBox.showerror('Not connected!', 'Not connected to a robot!')
                print "Not connected."
        except serial.SerialException:
            print "Lost connection"
            tkMessageBox.showinfo('Uh-oh', "Lost connection to the robot!")
            connection = None

        # print ' '.join([ str(ord(c)) for c in command ])
        # self.text.insert(END, ' '.join([ str(ord(c)) for c in command ]))
        # self.text.insert(END, '\n')
        # self.text.see(END)

    # getDecodedBytes returns a n-byte value decoded using a format string.
    # Whether it blocks is based on how the connection was set up.
    def getDecodedBytes(self, n, fmt):
        global connection
        
        try:
            return struct.unpack(fmt, connection.read(n))[0]
        except serial.SerialException:
            print "Lost connection"
            tkMessageBox.showinfo('Uh-oh', "Lost connection to the robot!")
            connection = None
            return None
        except struct.error:
            print "Got unexpected data from serial port."
            return None

    #goes 7.75 inches in one second 
    def goForward(self, length):
        range = float(length)/7.75
        t_end = time.time() + range
        while time.time() < t_end:
            self.sendCommandASCII('145 0 200 0 200')
        self.sendCommandASCII('145 0 0 0 0')

        return 

    #turns right by 90 degrees
    def turnRight(self, angle):
        turn = (float(angle)*1.45)/90
        t_end = time.time() + turn 
        while time.time() <= t_end:
            self.sendCommandASCII('145 255 106 0 150')
        self.sendCommandASCII('145 0 0 0 0')

        return  

    #turns left by 90 degrees
    def turnLeft(self, angle):
        turn = (float(angle)*1.45)/90
        t_end = time.time() + turn
        while time.time() <= t_end:
            self.sendCommandASCII('145 0 150 255 106')
        self.sendCommandASCII('145 0 0 0 0')

        return 

    def createRoute(self):
        global robotRoute
        for i in range(len(robotPath)): 
            #print robotPath[i]
            if ( robotPath[i] != "R1" and robotPath[i] != "D1"):
                obtArr = robotPath[i][0] + robotPath[i][1]
                obtArr = int(obtArr)
                obtNum = robotPath[i][3]
                obtNum = int(obtNum)
                cord = inputValues.obstacles[obtArr][obtNum]
                cord = cord.split(',')
                cord[0] = int(cord[0])
                cord[1] = int(cord[1])
                robotRoute.addToPath(cord)
                #print type(cord)
            elif robotPath[i] == "R1":
                cord = str(inputValues.cable[0])
                cord = cord.split(',')
                cord[0] = int(cord[0])
                cord[1] = int(cord[1])
                robotRoute = Route (robotName,cord)

            elif robotPath[i] == "D1":
                cord = inputValues.destinations[0]
                cord = cord.split(',')
                cord[0] = int(cord[0])
                cord[1] = int(cord[1])
                robotRoute.addToPath(cord)
                robotRoute.setEnd(cord)
                
    def getLength(self, list1,list2):
        return math.sqrt((list1[0]-list2[0])**2 +(list1[1]-list2[1])**2 )

    def getAngle(self,list1,list2):
        y = (list2[1] - list1[1]) 
        x = (list2[0] - list1[0])
        if ( x == 0 ): 
            slope = 0
        else: slope = float(y)/float(x)
        return   math.degrees(np.arctan(slope))
        
    def makeSureCurrent(self):
        time.sleep(4)

    def determineLength(self):
        global currentFacingAngle
        for i in range(len(robotRoute.path)-1):
            print str(i) + ":"
            leng = self.getLength(robotRoute.path[i],robotRoute.path[i+1])
            leng = leng/25
            ang = self.getAngle(robotRoute.path[i],robotRoute.path[i+1])
            print "length: " + str(leng)
            print "angle: " + str(ang)
            if (ang > 0):
                currentFacingAngle = currentFacingAngle - ang
                self.turnRight(currentFacingAngle)
                self.goForward(leng)
                self.turnLeft(currentFacingAngle)
                currentFacingAngle = currentFacingAngle + ang
            elif (ang < 0 ):
                currentFacingAngle = ang*-1      
                self.turnLeft(currentFacingAngle)
                self.goForward(leng)
                self.turnRight(currentFacingAngle)
                currentFacingAngle = 90
            else:
                self.goForward(leng)

            print "------------------"
            self.makeSureCurrent()
        
    def callbackKey(self, event):
        k = event.keysym.upper()
        motionChange = False
        
        

        if event.type == '2': # KeyPress; need to figure out how to get constant
            if k == 'P':   # Passive
                self.sendCommandASCII('128')
            elif k == 'S': # Safe
                self.sendCommandASCII('131')
            elif k == 'SPACE': # Beep
                self.sendCommandASCII('140 3 1 64 16 141 3')
            elif k =='W':
                self.createRoute()
                print robotRoute.__dict__
                self.determineLength()
            elif k == 'R':
                self.turnRight(45)   
            elif k == 'L':
                self.turnLeft(45)        
            elif k == 'UP':
                self.callbackKeyUp = True
                motionChange = True
            elif k == 'DOWN':
                self.callbackKeyDown = True
                motionChange = True
            elif k == 'LEFT':
                self.callbackKeyLeft = True
                motionChange = True
            elif k == 'RIGHT':
                self.callbackKeyRight = True
                motionChange = True
            else:
                print repr(k), "not handled"
        elif event.type == '3': # KeyRelease; need to figure out how to get constant
            if k == 'UP':
                self.callbackKeyUp = False
                motionChange = True
            elif k == 'DOWN':
                self.callbackKeyDown = False
                motionChange = True
            elif k == 'LEFT':
                self.callbackKeyLeft = False
                motionChange = True
            elif k == 'RIGHT':
                self.callbackKeyRight = False
                motionChange = True
            
        if motionChange == True:
            velocity = 0
            velocity += VELOCITYCHANGE if self.callbackKeyUp is True else 0
            velocity -= VELOCITYCHANGE if self.callbackKeyDown is True else 0
            rotation = 0
            rotation += ROTATIONCHANGE if self.callbackKeyLeft is True else 0
            rotation -= ROTATIONCHANGE if self.callbackKeyRight is True else 0

            # compute left and right wheel velocities
            vr = velocity + (rotation/2)
            vl = velocity - (rotation/2)
            
            # create drive command
            cmd = struct.pack(">Bhh", 145, vr, vl)
            if cmd != self.callbackKeyLastDriveCommand:
                self.sendCommandRaw(cmd)
                self.callbackKeyLastDriveCommand = cmd

    def onConnect(self):
        global connection, inputValues

        if connection is not None:
            tkMessageBox.showinfo('Oops', "You're already connected!")
            return

        try:
            ports = self.getSerialPorts()
            port = tkSimpleDialog.askstring('Port?', 'Enter COM port to open.\nAvailable options:\n' + '\n'.join(ports))
        except EnvironmentError:
            port = tkSimpleDialog.askstring('Port?', 'Enter COM port to open.')

        if port is not None:
            print "Trying " + str(port) + "... "
            try:
                #115200
                connection = serial.Serial(port, baudrate=57600, timeout=1)
                print "Connected!"
                tkMessageBox.showinfo('Connected', "Connection succeeded!")
            except:
                print "Failed."
                tkMessageBox.showinfo('Failed', "Sorry, couldn't connect to " + str(port))

        with open('input.json') as f:
            data = f.read()
            inputValues = Input(data)
        return inputValues

    def onHelp(self):
        tkMessageBox.showinfo('Help', helpText)

    def onQuit(self):
        if tkMessageBox.askyesno('Really?', 'Are you sure you want to quit?'):
            self.destroy()

    def getSerialPorts(self):
        """Lists serial ports
        From http://stackoverflow.com/questions/12090503/listing-available-com-ports-with-python

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of available serial ports
        """
        if sys.platform.startswith('win'):
            ports = ['COM' + str(i + 1) for i in range(256)]

        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this is to exclude your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')

        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')

        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result    

if __name__ == "__main__":
    app = TetheredDriveApp()
    app.mainloop()

