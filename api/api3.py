#!/bin/env python

import random
from flask import Flask, jsonify, request, session
from random import randrange
from questions import get_questions
from ml import load_process_predict, load_process_images  # Import your ML functions
from flask_cors import cross_origin  # Fix the typo in import
from features import new_features, new_questions, proba_features, answers  # Import new features, questions, and answers
from flask_cors import CORS
from flask_session import Session
import os


app = Flask(__name__)
#app.secret_key = os.environ.get('SECRET_KEY') #KEEP THIS LINE AND ADD THE KEY ON AZURE
app.secret_key = 'you-will-never-guess' # DON'T FORGET TO DELETE THIS LINE ON DEPLOYMENT
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = True
Session(app)
CORS(app)

#initialisation du jeu : sélection de 28 images 
#MODIFIER le ms des images pour qu'il prenne en compte le 3e mode de jeu (on génère une grille de 28)
@app.route('/api/init/<int:gamemod>', methods=['GET'])
@cross_origin(supports_credentials=True, origins="http://localhost:3000")
def init_game(gamemod):
    session['list_image'] = []
    list_image = session['list_image']
    
    nb_images_bdd = 40000

    if gamemod == 1:
        grid_size = 1024
    elif gamemod == 2:
        grid_size = 28
    elif gamemod == 3: ###A MODIF DANS LE MS INIT LISTE D IMAGES
        grid_size = 28

    while len(session['list_image']) < grid_size:
        r = randrange(0, nb_images_bdd) + 52000 #the number of the images start at 52000
        if r not in list_image:
            list_image.append(r)

    session['list_image'] = list_image

    # envoie liste d'id images
    return jsonify(list_image)

@app.route('/api3/start', methods=['POST'])
@cross_origin(supports_credentials=True, origins="http://localhost:3000")
def start_game():
    list_image = session['list_image'] 

    #choix de l'image par l'ordi
    nb_images = len(list_image)
    img_choice = randrange(0, nb_images)   

    # list_features est égal à la valeur de new_features
    list_features_ordi = new_features.copy()
    list_features_joueur = new_features.copy()
    list_answers_joueur = answers.copy()


    #initialisation des variables de session
    session['max_questions'] = 10
    session['max_guess'] = 3

    session['nb_questions_ordi'] = 0
    session['last_feature'] = None
    session['nb_guess_ordi'] = 0
    session['proba_list'] = [1]*len(list_image)
    session['list_features_ordi'] = []


    session['list_answer'] = []
    session['img_choice'] = None
    session['list_features_joueur'] = []
    session['nb_guess_joueur'] = 0
    session['nb_questions_joueur'] = 0

    # create a list of path from the list of images
    list_path = []  
    for i in range(len(list_image)):
        list_path.append("https://etud.insa-toulouse.fr/~alami-mejjat/0"+str(list_image[i])+".jpg")

    #predict labels on selected images
    predicted_labels = load_process_predict(list_path)

    #eliminate irrelevant features from players list
    nb_rows = len(predicted_labels) #number of elements in the grid
    nb_col = len(predicted_labels[0]) #number of features
    for i in range(0,nb_col):
        if list_features_joueur[i]!= None:
            count = 0
            for j in range(0, nb_rows):
                if predicted_labels[j][i] is not None :
                    count = count + predicted_labels[j][i]
            if count == 0 : #to do : vérifier qu'on garde bien cette partie
                list_features_joueur[i] == None

    #donner la première question de l'ordi au joueur
    feature = get_questions(list_features_ordi, predicted_labels)
    question = new_questions[feature]
    nb_questions_ordi = session['nb_questions_ordi']
    nb_questions_ordi =+ 1

    #update the session variables
    session['list_images'] = list_image
    session['last_feature'] = feature
    session['nb_questions'] = 1
    session['predicted_labels'] = predicted_labels

    session['list_features_ordi'] = list_features_ordi
    session['nb_questions_ordi'] = nb_questions_ordi

    session['img_choice'] = img_choice
    session['list_features_joueur'] = list_features_joueur

    return jsonify(
        feature=feature,
        question=question
    )

#update pour chaque question que l'on pose
@app.route('/api3/answer/<int:answer>', methods=['GET'])
@cross_origin(supports_credentials=True, origins="http://localhost:3000")
def get_response_and_next_question(answer):
    #--------------------1 : réponse du joueur à la question de l'ordi et posage de nouvelle question à l'ordi
    #actualisation des probas
    if answer != 2:
        update_probabilities(answer) #modifier l'appel à cette fonction car ça a été modifié ?

    list_features_ordi = session['list_features_ordi']
    last_feature = session['last_feature']
    proba_list = session['proba_list']
    list_images = session['list_images']
    nb_questions_ordi = session['nb_questions_ordi']
    max_questions = session['max_questions']
    nb_guess_ordi = session('nb_guess_ordi')

    list_features_ordi[list_features_ordi.index(last_feature)] = None

    # Si le max est 2 fois plus grand que le deuxième max, on peut proposer une réponse
    if max(proba_list) > 2*sorted(proba_list)[-2] or nb_questions_ordi == max_questions :
        guess_index = proba_list.index(max(proba_list))
        guess = list_images[guess_index]
        nb_guess_ordi +=1

        session['nb_guess_ordi'] = nb_guess_ordi

        return jsonify(
            character=guess
        ) 
    # Si les probas sont trop faibles, on peut déclarer forfait
    elif max(proba_list) < 0.05 :
        return jsonify(
            fail=True
        )
    # Sinon on continue à jouer en posant une nouvelle question
    else :
        predicted_labels = session['predicted_labels']
        feature = get_questions(list_features_ordi, predicted_labels)

        # Prepare the response
        question = new_questions[feature]

        nb_questions_ordi +=1

        #update the session variables
        session['nb_questions'] = nb_questions_ordi
        session['last_feature'] = feature

        return jsonify(
            feature=feature,
            question=question,
        ) 
    



# Update the probabilities based on the user's answer
def update_probabilities(user_answer):
    list_features = session['list_features']
    last_feature = session['last_feature']
    final_img_list = session['final_img_list']
    predicted_labels = session['predicted_labels']
    proba_list = session['proba_list']
    
    #update probabilities from players' answer
    index = list_features.index(last_feature)
    for i in range(len(final_img_list)):

        if user_answer == predicted_labels[i][index]:
            proba_list[i] *= proba_features[index]
        else:
            proba_list[i] *=  (1-proba_features[index])

    #update the session variables
    session['proba_list'] = proba_list


if __name__ == '__main__':
    app.run(debug=True)