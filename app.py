import tensorflow as tf
from keras.preprocessing.image import img_to_array
import numpy as np
from PIL import Image
from io import BytesIO
from flask import Flask, jsonify, request, session
from flask_cors import CORS
import os
import requests
import tensorflow as tf

# Disable TensorFlow warnings
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

ms_ariane = 'https://arianeservice.azurewebsites.net/'
ms_aminoguess = 'https://aminoguessservice.azurewebsites.net/'

app = Flask(__name__)
CORS(app, origins=[ms_ariane, ms_aminoguess])

@app.route('/')
def hello():
    return 'Bienvenue chez AIService'

# Parameters
images_dir_path = os.path.join(os.getcwd(), "images")
nb_images = 10
image_width, image_height = 178, 218
model_path = os.path.join(os.getcwd(), "model_ki_s")
model = tf.keras.models.load_model(model_path)


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

            # Stockez l'image prétraitée dans une liste
            images.append(img_array)

        else:
            print("Échec du téléchargement de l'image")

    return np.array(images)

@app.route('/ml/predict/', methods=['POST'])
def load_process_predict():
    data = request.json

    predicted_labels = []

    list_path_init = data['list_path_init']
    images = load_images(list_path_init)

    predicted_labels += np.round(model.predict(images)).tolist()

    return jsonify(predicted_labels=predicted_labels)

if __name__ == '__main__':
    app.run(debug=True, port = 5003)
