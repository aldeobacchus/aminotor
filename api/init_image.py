import random
from flask import Flask, jsonify, request, session
from random import randrange
from questions import get_questions
from ml import load_process_predict, load_process_images  # Import your ML functions
from flask_cors import cross_origin  # Fix the typo in import
from features import new_features, new_questions, proba_features  # Import new features, questions, and answers
from flask_cors import CORS
import os


app = Flask(__name__)
CORS(app)

#initialisation du jeu : sélection de 1024 images
@app.route('/image/init/<int:gamemod>', methods=['GET'])

def init_game(gamemod):
    
    list_image = []
    nb_images_bdd = 40000

    if gamemod == 1:
        grid_size = 1024
    elif gamemod == 2:
        grid_size = 28

    while len(list_image) < grid_size:
        r = randrange(0, nb_images_bdd) + 52000 #the number of the images start at 52000
        if r not in list_image:
            list_image.append(r)

    

    # envoie liste d'id images
    return jsonify(list_image=list_image)



if __name__ == '__main__':
    app.run(debug=True, port = 5001)