from flask import Flask, request, send_file
import io
import os
import sys

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types


app = Flask(__name__)

@app.route('/', methods=['POST'])
def posty():
    file = request.files['inputfile']
    if file:
        candidate = file.read()


        client = vision.ImageAnnotatorClient()

        image = types.Image(content=candidate)

        # Performs label detection on the image file
        response = client.label_detection(image=image)
        labels = response.label_annotations

        label_list = []
        compost = ['food', 'snack', 'produce']
        recycle = ['plastic', 'wood', 'glass', 'paper', 'cardboard', 'metal', 'aluminum', 'tin', 'carton']
        donate = ['clothes', 'clothing', 'shirt', 'pants', 'jacket', 'footwear', 'shoe']

        for label in labels:
            label_list.append(label.description)

        print(label_list)

        solution = False

        for label in label_list:
            new = label.split()
            if new[0].lower() in compost:
                return 'Compost this, you hippie'
                solution = True
                break
            elif new[0].lower() in recycle:
                return 'Recycle this, you tree hugger'
                solution = True
                break
            elif new[0].lower() in donate:
                return 'Donate this, you consumeristic sheep'

        if  not solution:
            return 'This is trash and you are trash'
    else:
        return 'Upload a damn image file'

@app.route('/', methods=['GET'])
def getty():
    return send_file('index.html')

@app.route('/images/<string:pid>')
def design(pid):
    return send_file('images\\'+pid)


if __name__ == '__main__':
    app.run(debug=True)
