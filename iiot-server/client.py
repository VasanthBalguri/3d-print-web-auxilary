import cv2
import socketio
import time
import base64
import sys
import time
import threading
import json
import configuration

from printrun.printcore import printcore
from printrun.utils import setup_logging
from printrun import gcoder


sio = socketio.Client()

cap= ""

enable = 0

class monitorThread (threading.Thread):
   def __init__(self, threadID, name, q):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
   def run(self):
      print "Starting monitoring " + self.name
      monitor()
      print "Exiting monitoring" + self.name

@sio.event
def connect():
	print("CONNECTED")
	global cap
	global enable
	cap=cv2.VideoCapture(0)
	enable = 1

@sio.event
def connect_error(data):
    print("The connection failed!")
    print(data)

@sio.on('print')
def print(data):
    p = printcore(port, baud)
    p.loud = loud
    time.sleep(2)
    gcode = [i.strip() for i in open(filename)]
    gcode = gcoder.LightGCode(gcode)
    p.startprint(gcode)
    

def monitor():
    while enable:
        if(cap.isOpened()):
            ret,img=cap.read()
            if ret:
                img = cv2.resize(img, (0,0), fx=0.5, fy=0.5)
                frame = cv2.imencode('.jpg', img)[1].tobytes()
                frame= base64.encodebytes(frame).decode("utf-8")
                #sio.emit('iiot-video-feed',"data:image/jpeg;base64,"+frame+"==")
                sio.emit('iiot-video-feed',frame)
                time.sleep(1/60)

@sio.on("enable_monitor")
def enable_monitor():
    global enable
    enable = 1

@sio.on("disable_monitor")
def disbale_monitor():
    global enable
    enable = 0

@sio.event
def disconnect():
	print("DISCONNECTED")
	enable = 0
	cap.release()


sio.connect("http://192.168.0.5:3000")
p = printcore(port, baud)
p.loud = loud
time.sleep(2)

