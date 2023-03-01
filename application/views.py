from flask import render_template, request
from flask import redirect, url_for
from PIL import Image
import os
from application.utils import pipeline_model

UPLOAD_FOLDER = 'static/uploads'

def base():
    return render_template("base.html")

def index():
    return render_template("index.html")

def face():
    return render_template("face.html")

def getwidth(path):
    img = Image.open(path)
    size = img.size #width & height
    aspect = size[0] / size[1]
    w = 300 * aspect
    return int(w)
    
    

def faceapp():
    if request.method == 'POST':
        f = request.files['image']
        filename = f.filename
        print(filename)
        path = os.path.join(UPLOAD_FOLDER, filename)
        print(path)
        f.save(path)
        w = getwidth(path)
        #prediction (pass to pipeline model)
        pipeline_model(path, filename, color='bgr')
        return render_template("faceapp.html", fileupload=True, img_name=filename, w=w)
        
    return render_template("faceapp.html", fileupload=False, img_name="stardust.png", w=300)