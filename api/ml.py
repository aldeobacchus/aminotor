import tensorflow as tf
from keras.preprocessing.image import img_to_array
import numpy as np
from PIL import Image
from io import BytesIO
from flask import Flask, jsonify, request, session
from flask_cors import CORS
import os
import requests

app = Flask(__name__)
CORS(app)

# Parameters
model_path = os.path.join(os.getcwd(), "model_ki_s")
images_dir_path = os.path.join(os.getcwd(), "images")
nb_images = 10
image_width, image_height = 128, 128


def load_process_images(_image_dir_path, _nb_images):
    # Load and preprocess the images
    images = []
    filenames = os.listdir(_image_dir_path)[:_nb_images]
    for filename in filenames:
        if filename.endswith(".jpg"):
            # Load and resize the image
            img_path = os.path.join(_image_dir_path, filename)
            img = tf.keras.utils.load_img(img_path, target_size=(image_width, image_height))
            img_array = img_to_array(img)
            # Preprocess the image (you may need to adapt this based on your specific requirements)
            img_array = img_array / 255.0  # Normalize pixel values to [0, 1]

            # Append the image and label to the lists
            images.append(img_array)

    return np.array(images)

def load_images (list_images):

    images = []
    
    for image_url in list_images:

        # Utilisez requests pour télécharger l'image depuis l'URL
        response = requests.get(image_url)

        # Vérifiez si la requête a réussi
        if response.status_code == 200:
            # Ouvrez l'image téléchargée avec Pillow
            img = Image.open(BytesIO(response.content))

            # Convertissez l'image en tableau numpy
            img_array = np.array(img) / 255.0

            # Redimensionnez l'image
            img_array = tf.image.resize(img_array, [image_width, image_height])

            # Stockez l'image prétraitée dans une liste
            images.append(img_array)

        else:
            print("Échec du téléchargement de l'image")

    return np.array(images)

@app.route('/ml/predict', methods=['POST'])
def load_process_predict(_model_path=model_path):
    data = request.json

    # Load the model
    model = tf.keras.models.load_model(_model_path)

    list_path = data['list_path']
    # Load and preprocess the images
    images = load_images(list_path)

    predicted_labels = np.round(model.predict(images)).tolist()

    return jsonify(predicted_labels=predicted_labels)


if __name__ == '__main__':
    app.run(debug=True, port = 5003)
