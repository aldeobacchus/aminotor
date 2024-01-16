import random
from flask import Flask, jsonify, request, session
from random import randrange
from questions import get_questions
from ml import load_process_predict, load_process_images  # Import your ML functions
from flask_cors import cross_origin  # Fix the typo in import
from features import new_features, new_questions, proba_features  # Import new features, questions, and answers
from flask_cors import CORS
from flask_session import Session
import json
import os
import requests


app = Flask(__name__)
#app.secret_key = os.environ.get('SECRET_KEY') #KEEP THIS LINE AND ADD THE KEY ON AZURE
app.secret_key = 'you-will-never-guess' # DON'T FORGET TO DELETE THIS LINE ON DEPLOYMENT
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = True
Session(app)
CORS(app)

#initialisation du jeu : sélection de 1024 images
@app.route('/api/init/<int:gamemod>', methods=['GET'])
@cross_origin(supports_credentials=True, origins="http://localhost:3000" )
def init_game(gamemod):
    response = requests.get(f'http://localhost:5001/image/init/{gamemod}').json()
    session['list_image'] = response.get('list_image')
    return jsonify(session['list_image'])


#première question du jeu
@app.route('/api/start/<int:nb_images>', methods=['GET'])
@cross_origin(supports_credentials=True, origins="http://localhost:3000")
def start_game(nb_images):

    session['list_features'] = new_features.copy()
    session['nb_images'] = nb_images
    data={
        'list_features': session['list_features'],
        'nb_images': session['nb_images'],
        'list_image': session['list_image']
    }
    
    response = requests.post('http://localhost:5002/aminoguess/start', json=data).json()

    #initialisation et update the session variables
    session['max_questions'] = 10
    session['last_feature'] = None
    session['proba_list'] = [1]*nb_images
    session['final_img_list'] = response.get("final_img_list")
    session['last_feature'] = response.get("feature")
    session['question'] = response.get("question")
    session['nb_questions'] = 1
    session['predicted_labels'] = response.get("predicted_labels")

    return jsonify(
        feature=response.get("feature"),
        question=response.get("question")
    )


#update pour chaque question que l'on pose
@app.route('/api/answer/<int:answer>', methods=['GET'])
@cross_origin(supports_credentials=True, origins="http://localhost:3000")
def get_response_and_next_question(answer):
    #actualisation des probas
    if answer != 2:
        update_probabilities(answer)

    list_features = session['list_features']
    last_feature = session['last_feature']
    proba_list = session['proba_list']
    final_img_list = session['final_img_list']
    nb_questions = session['nb_questions']
    max_questions = session['max_questions']

    list_features[list_features.index(last_feature)] = None

    # Si le max est 2 fois plus grand que le deuxième max, on peut proposer une réponse
    if max(proba_list) > 2*sorted(proba_list)[-2] or nb_questions == max_questions :
        guess_index = proba_list.index(max(proba_list))
        guess = final_img_list[guess_index]
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
        feature = get_questions(list_features, predicted_labels)

        # Prepare the response
        question = new_questions[feature]

        nb_questions +=1

        #update the session variables
        session['nb_questions'] = nb_questions
        session['last_feature'] = feature

        return jsonify(
            feature=feature,
            question=question,
        ) 
    
@app.route('/api/proposition/', methods=['GET'])
@cross_origin(supports_credentials=True, origins="http://localhost:3000")
def continue_next_question():
    proba_list = session['proba_list']
    final_img_list = session['final_img_list']
    list_features = session['list_features']
    predicted_labels = session['predicted_labels']

    guess_index = proba_list.index(max(proba_list))
    guess = final_img_list[guess_index]
    
    final_img_list[final_img_list.index(guess)] = None
    proba_list[guess_index] = 0

    feature = get_questions(list_features, predicted_labels)

    # Prepare the response
    question = new_questions[feature]

    #update the session variables
    session['nb_questions'] = 0
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
    app.run(debug=True, port = 5000)