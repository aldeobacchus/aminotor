import random
from flask import Flask, jsonify, request
from random import randrange
from questions import get_questions
from ml import load_process_predict, load_process_images  # Import your ML functions
from flask_cors import cross_origin  # Fix the typo in import
from features import new_features, new_questions, proba_features  # Import new features, questions, and answers
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Ajouter option guess si il est sur de lui
# Ajouter option l'IA se déclare perdante (proba trop faible)

#initialisation du jeu : sélection de 1024 images
@app.route('/api/init', methods=['GET'])
def init_game():
    #sélection de 1024 id au hasard
    global list_image
    list_image = []
    nb_images_bdd = 40000
    while len(list_image) < 1024:
        r = randrange(0, nb_images_bdd) + 52000 #the number of the images start at 52000
        if r not in list_image:
            list_image.append(r)

    # envoie liste d'id images
    return jsonify(list_image)

#première question du jeu
@app.route('/api/start/<int:nb_images>', methods=['GET'])
def start_game(nb_images):
    print("nb_images", nb_images)

    #déclaration et initialisation des variables globales
    global predicted_labels, nb_questions, max_questions, last_feature, proba_list, list_features
    global final_img_list # good

    final_img_list = []
    # list_features est égal à la valeur de new_features
    list_features = new_features.copy()
    nb_questions = 0
    max_questions = 5
    last_feature = None
    proba_list = [1]*nb_images

    #create img list from size selected by user
    for i in range(nb_images):
        final_img_list.append(list_image[i])

    # create a list of path from the list of images
    list_path = []  
    for i in range(nb_images):
        list_path.append("https://etud.insa-toulouse.fr/~alami-mejjat/0"+str(final_img_list[i])+".jpg")

    #predict labels on selected images
    predicted_labels = load_process_predict(list_path)

    #donner la première question
    feature = get_questions(list_features, predicted_labels)
    question = new_questions[feature]
    last_feature = feature
    nb_questions +=1

    return jsonify(
        feature=feature,
        question=question
    )


#update pour chaque question que l'on pose
@app.route('/api/answer/<int:answer>', methods=['GET'])
def get_response_and_next_question(answer):
    global nb_questions, list_features, last_feature, proba_list, final_img_list
    #actualisation des probas
    if answer != 2:
        update_probabilities(answer)

    list_features[list_features.index(last_feature)] = None

    # Select a new feature to ask a question about
    if nb_questions < max_questions:
        feature = get_questions(list_features, predicted_labels)

        # Prepare the response
        question = new_questions[feature]

        nb_questions +=1
        last_feature = feature

        return jsonify(
            feature=feature,
            question=question,
        ) 
            
    else : #max amount of questions reached => try to guess !!

        guess_index = proba_list.index(max(proba_list))
        guess = final_img_list[guess_index]
        # return quoi ???
        return jsonify(
            character=guess
        ) 
    
@app.route('/api/proposition/', methods=['GET'])
def continue_next_question():
    global nb_questions, list_features, last_feature, proba_list, final_img_list, question

    guess_index = proba_list.index(max(proba_list))
    guess = final_img_list[guess_index]
    
    final_img_list[final_img_list.index(guess)] = None
    proba_list[guess_index] = 0

    nb_questions = 0

    feature = get_questions(list_features, predicted_labels)

    # Prepare the response
    question = new_questions[feature]
    last_feature = feature
    nb_questions +=1
    

    return jsonify(
        feature=feature,
        question=question,
    ) 


# Update the probabilities based on the user's answer
def update_probabilities(user_answer):

    #update probabilities from players' answer
    index = list_features.index(last_feature)
    for i in range(len(final_img_list)):
        if user_answer == predicted_labels[i][index]:
            proba_list[i] *= proba_features[index]
        else:
            proba_list[i] *=  (1-proba_features[index])


if __name__ == '__main__':
    app.run(debug=True)