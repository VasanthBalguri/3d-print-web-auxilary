import cv2
import socketio
import time
import base64
import sys
import time
import threading
import json
import configuration
import json

from printrun.printcore import printcore
from printrun.utils import setup_logging
from printrun import gcoder

from flask import Flask, redirect, url_for, request

app = Flask(__name__)

sio = socketio.Client()
port = "/dev/ttyUSB0"
baud = 115200
cap= ""
temprature = ""
enable = 0
idle = 0
state = "idle"

p = printcore(port, baud)
p.loud = True
p.tempcb = temp_callback

class MonitorThread (threading.Thread):
   def __init__(self, threadID, name):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
   def run(self):
      print "Starting monitoring " + self.name
      while enable:
        monitor()
      print "Exiting monitoring" + self.name

def monitor():
    frame = ""
    data = ""
    if(p.printing):
        progress = 0
        if(p.mainqueue != "None"):
            progress = 100 * float(p.queueindex) / len(p.mainqueue)
            p.send_now("M105")
            #sio.emit('iiot-video-feed',"data:image/jpeg;base64,"+frame+"==")
            data = "{"+"temprature:" + temprature + ",progress:" + progress + ",status:" + state)
    else:
        global state
        state = "printed"
        data = "{"+"temprature:" + temprature + ",progress:" + progress + ",status:" + state
        print("finished")
    if(cap.isOpened()):
        ret,img=cap.read()
        if ret:
            img = cv2.resize(img, (0,0), fx=0.5, fy=0.5)
            frame = cv2.imencode('.jpg', img)[1].tobytes()
            frame= base64.encodebytes(frame).decode("utf-8")
            
    sio.emit('getIiotData',data + ",frame:" frame "}")
    time.sleep(1/60)

m = Monitorthread()


@sio.event
def connect():
	print("CONNECTED")
	#global cap
	#global enable
	#cap=cv2.VideoCapture(0)
	#enable = 1

@sio.event
def connect_error(data):
    print("The connection failed!")
    print(data)


#not used
'''
@sio.on('get-iiot-data')
def get-iiot-data(data):
    progress = 0
    if(p.mainqueue != "None"):
        progress = 100 * float(p.queueindex) / len(p.mainqueue)
    p.send_now("M105")
    #sio.emit('iiot-video-feed',"data:image/jpeg;base64,"+frame+"==")
    data = "{"+"temprature:" + temprature + ",progress:" + progress + ",status:" + p.printing
    if(cap.isOpened()):
        ret,img=cap.read()
        if ret:
            img = cv2.resize(img, (0,0), fx=0.5, fy=0.5)
            frame = cv2.imencode('.jpg', img)[1].tobytes()
            frame= base64.encodebytes(frame).decode("utf-8")
            sio.emit('getIiotData',data + ",frame:" frame "}")

@sio.on('print')
def print(data):
    if(not p.printing):
        gcode = [i.strip() for i in open(filename)]
        gcode = gcoder.LightGCode(gcode)
        p.startprint(gcode)

@sio.on("enable_monitor")
def enable_monitor():
    global idle
    idle = 1

@sio.on("disable_monitor")
def disbale_monitor():
    global idle
    idle = 0

@sio.event
def disconnect():
	print("DISCONNECTED")
'''
#not used
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/connect',methods = ['POST'])
def connect():
   if request.method == 'POST':
    #slicer.addModel(request.form.stlPath)
    #slicer.slice("out.gcode",0,0)
    sio.connect(request.link)
    sio.emit("init-iiot-endpoint",request.id)
    #m.start()
    return 'connecting'
   else:
      return 'GET not supported'
#not used
@app.route('/enableMonitor')
def enableMonitor():
    global idle
    idle = 0
    return 'monitoring_enabled'

@app.route('/print', methods = ['POST'])
def print():
    if request.method == 'POST':
        gcode = request.files['out.gcode']
        if(not p.printing):
            #gcode = [i.strip() for i in open(filename)]
            global idle
            global state
            idle = 0
            gcode = gcoder.LightGCode(gcode)
            p.startprint(gcode)
            state = "printing"
            return "printing"
        else:
            return "busy"
#not used    
@app.route('/disableMonitor')
def disbaleMonitor():
    global idle
    idle = 1
    return 'monitoring_disabled'
    
@app.route('/finishPrint')
def finishPrint():
    global state
    state = "idle"
    return 'finished_print'

@app.route('/disconnect',methods = ['DELETE'])
def disconnect():
    if request.method = 'DELETE'
    enable = 0
    m.join()
    sio.disconnect()
	cap.release()
	retrun "disconnected"

def temp_callback(a):
    global temprature
    temprature = a.split()[1][2:]
    return temprature

#sio.connect("http://192.168.0.5:3000")


