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

#première question du jeu
@app.route('/aminoguess/start', methods=['POST'])
def start_game():
    data = request.json
    final_img_list = []
    nb_image = data['nb_images']
    list_image = data['list_image']
    list_features = data['list_features']
    #create img list from size selected by user
    for i in range(nb_image):
        final_img_list.append(list_image[i])
    # create a list of path from the list of images
    list_path = []  
    for i in range(nb_image):
        list_path.append("https://etud.insa-toulouse.fr/~alami-mejjat/0"+str(final_img_list[i])+".jpg")
    #predict labels on selected images
    predicted_labels = load_process_predict(list_path)
    #donner la première question
    feature = get_questions(list_features, predicted_labels)
    question = new_questions[feature]
    return jsonify(
        final_img_list=final_img_list,
        predicted_labels=predicted_labels.tolist(),
        feature=feature,
        question=question
    )


#update pour chaque question que l'on pose
#@app.route('/aminoguess/answer/<int:answer>', methods=['GET'])
#def get_response_and_next_question(answer):
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
    
#@app.route('/aminoguess/proposition/', methods=['GET'])
#def continue_next_question():
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
    app.run(debug=True, port = 5002)