import random
from flask import Flask, jsonify, request
from random import randrange
from questions import get_questions
from ml import load_process_predict, load_process_images  # Import your ML functions
from flask_cors import cross_origin  # Fix the typo in import
from features import new_features, new_questions, new_answers  # Import new features, questions, and answers

app = Flask(__name__)

#initialisation du jeu : sélection de 1024 images
@app.route('/api/init', methods=['GET'])
def get_images():
    #sélection de 1024 id au hasard
    global list_image
    nb_images_bdd = 10000
    for i in range(1024):
        list_image.add(randrange(nb_images_bdd))

    #get images de la bdd à partir de leurs id
    #renvoie les images au front
        

#première question du jeu
@app.route('/api/start/{nb_images}', methods=['GET'])
def start_game(nb_images):
    data = request.get_json()

    #déclaration et initialisation des variables globales
    global predicted_labels, nb_questions, max_questions, last_feature, proba_list, list_features, guess, nb_questions_global
    global final_img_list

    final_img_list = []
    list_features = new_features
    nb_questions = 0
    nb_questions_global = 0

    max_questions = 10
    last_feature = None
    guess = None
    proba_list = [0 for i in range(nb_images)]

    #create img list from size selected by user
    for i in range(nb_images):
        final_img_list.add(list_image[i])

    #predict labels on selected images
    predicted_labels = load_process_predict(nb_images)

    #check if some labels are useless
    for i in range(0, len(predicted_labels[0])):
        count = 0
        for j in range(0, len(predicted_labels)):
            count = count + predicted_labels[j][i]
        if count == 0:
            list_features[i] = None


    #donner la première question
    feature = get_questions(list_features, predicted_labels)
    question = new_questions[feature]

    return jsonify(
        feature=feature,
        question=question,
        answers=new_answers[feature],
    )


#update pour chaque question que l'on pose
@app.route('/api/questions/', methods=['GET'])
def get_response_and_next_question():
    #récupération de la réponse
    answers = request.json.get('answers', [])

    #actualisation des probas
    update_probabilities(answers)

    # Select a new feature to ask a question about
    if nb_questions < max_questions:
        feature = get_questions(list_features, predicted_labels)

        # Prepare the response
        question += f" {new_questions[feature]}?"
        param = f"is_{feature}"

        nb_questions +=1
        last_feature = feature

        list_features[list_features.index(feature)] = None

        return jsonify(
            feature=feature,
            param=param,
            question=question,
            answers=new_answers[feature],
        ) 
            
    else : #max amount of questions reached => try to guess !!

        guess_index = proba_list.index(max(proba_list))
        guess = final_img_list[guess_index]
        # return quoi ???
        return jsonify(
            characterMatch=guess
        ) 
    
@app.route('/api/proposition/', methods=['GET'])
def continue_next_question():
    final_img_list[final_img_list.index(guess)] = None
    nb_questions = 0

    feature = get_questions(list_features, predicted_labels)

    # Prepare the response
    question += f" {new_questions[feature]}?"
    param = f"is_{feature}"

    nb_questions +=1

    return jsonify(
        feature=feature,
        param=param,
        question=question,
        answers=new_answers[feature],
    ) 

def update_probabilities(user_answer):
    N= len(proba_list)

    # Validation de la réponse de l'utilisateur
    valid_answers = ["Yes", "No", "I don't know"]
    if user_answer in valid_answers:
        if user_answer == "Yes":
            answer = 1
        elif user_answer == "No":
            answer = 0
        else:
            answer = 0.5
        
        #update probabilities from players' answer
        index = list_features.index(last_feature)
        for i in range (0, N-1):
            proba_list[i] = proba_list[i] + predicted_labels[i][index]*answer

        response = {
            "message": f"Received answer: {user_answer}"
        }
        return jsonify(response)
    else:
        return jsonify({"error": "Invalid answer. Use 'Yes', 'No', or 'I don't know'."}), 400


if __name__ == '__main__':
    app.run(debug=True)
