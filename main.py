import flask
import os
import random
from ccn_model import CNN
from classifier import classifier
import torch


from flask import Flask

app = Flask(__name__)


@app.route('/')
def home():
    return "Machine Learning Micro-Service"


@app.route('/stock')
def stock():
    return "Retrieve last stock from DB"


@app.route('/demo', methods=['GET'])
def demo():
    response = []
    # Init Convolutional Neural Network Model
    model = CNN()
    device = torch.device('cpu')
    model.load_state_dict(torch.load('flowershop_inventory_cnn.pth', map_location=device))
    model.eval()
    dir_types = ['rose', 'lily', 'daisy', 'carnation']
    for dir_type in dir_types:
        demo_dir = f"demo/{dir_type}"
        image_file = random.choice([x for x in os.listdir(demo_dir)
                                    if os.path.isfile(os.path.join(demo_dir, x)) and x.endswith('.jpg')])
        if image_file:
            image_path = os.path.join(demo_dir, image_file)
            prediction = classifier(model, image_path)
            response.append({'type': dir_type, 'status': prediction, 'image': image_path})
        else:
            print(image_file)
            response.append({'type': dir_type, 'status': 'out of stock', 'image': 'error'})

    return flask.jsonify(response)


if __name__ == "__main__":
    website_url = 'localhost:5000'
    app.config['SERVER_NAME'] = website_url
    app.run()
