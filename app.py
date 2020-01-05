import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import requests
import cv2

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html', click='no-click')

@app.route('/hotdog/')
def hotdog():
    return render_template('hotdog.html', click='no-click')

@app.route('/get_image_hotdog_a',methods=['GET', 'POST'])
def get_data_hotdog_a():
    #Picture_request = requests.get('http://127.0.0.1:5000/get_image')
    #if Picture_request.status_code == 200:
        #with open("static/image.jpg", 'wb') as f:
            #f.write(Picture_request.content)
    return render_template('hotdog.html', original_image='static/image_a.jpg')

@app.route('/get_image_hotdog_b',methods=['GET', 'POST'])
def get_data_hotdog_b():
    return render_template('hotdog.html', original_image='static/image_b.jpg', treated_image='static/image_a.jpg')

@app.route('/get_image_paint_a',methods=['GET', 'POST'])
def get_data_paint_a():
    return render_template('index.html', original_image='static/image_b.jpg')

@app.route('/get_image_paint_b',methods=['GET', 'POST'])
def get_data_paint_b():
    return render_template('index.html', original_image='static/image_b.jpg', treated_image='static/image_a.jpg')

# route http posts to this method
@app.route('/upload', methods=['POST'])
def test():
    r = request
    # convert string of image data to uint8
    nparr = np.fromstring(r.data, np.uint8)
    # decode image
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # do some fancy processing here....
    #store the image
    cv2.imwrite('current_picture.jpg', img)

    # build a response dict to send back to client
    response = {'message': 'image received. size={}x{}'.format(img.shape[1], img.shape[0])
                }
    # encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)

    return Response(response=response_pickled, status=200, mimetype="application/json")


if __name__ == "__main__":
    app.run(debug=True, port=80)