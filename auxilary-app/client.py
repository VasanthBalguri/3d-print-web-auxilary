import time
import Slic3rModule

from flask import Flask, redirect, url_for, request

app = Flask(__name__)
slicer = Slic3rModule.Slic3rModule()

@app.route('/slice',methods = ['POST'])
def slice():
   if request.method == 'POST':
    #slicer.addModel(request.form.stlPath)
    print(request.json["filepath"])
    filepath = request.json["filepath"]
    outpath = "gcodes/" +  request.json["name"] + ".gcode"
    print(outpath)
    slicer.addModel(filepath)
    slicer.slice(outpath ,0,0)
    #os.replace(request.form.name + ".gcode" , "../gcodes/" + request.json.name + ".gcode")
    return outpath
   else:
      return 'GET not supported'


