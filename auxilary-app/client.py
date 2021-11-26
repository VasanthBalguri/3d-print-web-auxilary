import time
import Slic3rModule

from flask import Flask, redirect, url_for, request

app = Flask(__name__)
slicer = Slic3rModule.Slic3rModule()

@app.route('/slice',methods = ['POST'])
def slice():
   if request.method == 'POST':
    slicer.addModel(request.form.stlPath)
    slicer.slice(request.form.name + ".gcode",0,0)
    os.replace(request.form.name + ".gcode" , "../gcodes/" + request.form.name + ".gcode")
    return request.form.name + ".gcode"
   else:
      return 'GET not supported'


