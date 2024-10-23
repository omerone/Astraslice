from flask import Flask, request, jsonify, render_template
import requests
import cv2
import numpy as np
import base64
from io import BytesIO
from PIL import Image

app = Flask(__name__)

# ngrok url
path = "https://f49f-34-19-0-185.ngrok-free.app"

@app.route('/')
def index():
    return render_template('index.html', path=path)

@app.route('/segment', methods=['POST'])
def segment_image():
    data = request.get_json()
    image_data = data['imageData']
    points = data['points']

    colab_url = f"{path}/segment"
    response = requests.post(colab_url, json={'imageData': image_data, 'points': points})
    
    if response.status_code == 200:
        segmented_image_url = response.json()['segmentedImage']
        full_url = f"{path}/{segmented_image_url}"
        return jsonify({'segmentedImage': full_url})
    else:
        return jsonify({'error': 'Failed to process image'}), 500

if __name__ == '__main__':
    app.run(debug=True)