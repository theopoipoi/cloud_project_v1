import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import requests
import cv2
import base64
from flask_restful import Api
from flask_cors import CORS
from flask_socketio import SocketIO

app = Flask(__name__)
#model = pickle.load(open('model.pkl', 'rb'))
cors = CORS(app, resources={r"/": {"origins": ""}}) 
# creating an API object 
api = Api(app) 
socketio = SocketIO(app,cors_allowed_origins="*")

respDet=['','','','']
respArt=['','','','']

@socketio.on('img')
def handleMessage(msg):
    print('img')
    respDet[0]=msg

    

@socketio.on('art')
def handleMessage(msg):
    print('art')
    respArt[1]=msg

    
@socketio.on('det')
def handleMessage(msg):
    print('det')
    respDet[1]=msg


def from_base64(buf):
    jpg_original = base64.b64decode(buf)
    jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
    img = cv2.imdecode(jpg_as_np, flags=1)

    return img

@app.route('/')
def home():
    return render_template('index.html', click='no-click')

@app.route('/hotdog/')
def hotdog():
    return render_template('recognition.html', click='no-click')

@app.route('/get_img_paint',methods=['GET'])
def get_img_paint():
    socketio.emit('getImg','getImg',broadcast=True)
    return render_template('index.html', click='no-click')

@app.route('/get_img_hotdog', methods=['GET'])
def get_img_hotdog():
    socketio.emit('getDet','getDet',broadcast=True)    
    return render_template('recognition.html', click='no-click')

@app.route('/show_hotdog_a',methods=['GET'])
def show_hotdog_a():
    if respDet[0]!='' and respDet[1]!='':
        img = from_base64(respDet[0])
        cv2.imwrite('static/true.jpg',img)
        img = from_base64(respDet[1])
        cv2.imwrite('static/det.jpg',img)
    return render_template('recognition.html', original_image='static/true.jpg')

@app.route('/show_hotdog_b',methods=['GET'])
def get_data_hotdog_b():
    return render_template('recognition.html', original_image='static/true.jpg', treated_image='static/det.jpg')

@app.route('/show_paint_a', methods=['GET'])
def get_data_paint_a():
    if respDet[0]!='' and respArt[1]!='':
        img = from_base64(respDet[0])
        cv2.imwrite('static/true.jpg',img)
        img = from_base64(respArt[1])
        cv2.imwrite('static/art.jpg',img)
    return render_template('index.html', original_image='static/true.jpg')

@app.route('/show_paint_b', methods=['GET'])
def get_data_paint_b():
    return render_template('index.html', original_image='static/true.jpg', treated_image='static/art.jpg')


if __name__ == "__main__":
    socketio.run(app,host="0.0.0.0")
