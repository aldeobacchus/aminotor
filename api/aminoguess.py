
import os
from flask import Flask, jsonify, request, session
from questions import get_questions
from features import new_features, new_questions, proba_features  # Import new features, questions, and answers
from flask_cors import CORS
import requests


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

    list_upload = data['list_upload']

    #add the images uploaded by the user
    i=0
    while len(final_img_list) < nb_image and i < len(list_upload):
        final_img_list.append(list_upload[i])
        i += 1
    
    #add the images from the initial server
    i = 0
    while len(final_img_list) < nb_image:
        final_img_list.append(list_image[i])
        i += 1

    #TODO: change from the local server to the azure stockage service
    folder_name = "temp"

    list_path_upload = []
    for img in list_upload:
        list_path_upload.append(os.path.join(os.getcwd(),folder_name, f"{img}.jpg"))

    # create a list of path from the list of images from the initial server
    list_path_init = []  
    for i in range(nb_image):
        list_path_init.append("https://etud.insa-toulouse.fr/~alami-mejjat/0"+str(final_img_list[i])+".jpg")
    
    #predict labels on selected images
    data = {'list_path_upload':list_path_upload,
            'list_path_init':list_path_init
            }
    response = requests.post('http://localhost:5003/ml/predict', json=data).json()

    predicted_labels = response.get('predicted_labels')
    

    #donner la première question
    feature = get_questions(list_features, predicted_labels)
    question = new_questions[feature]
    return jsonify(
        final_img_list=final_img_list,
        predicted_labels=predicted_labels,
        feature=feature,
        question=question
    )


#update pour chaque question que l'on pose
@app.route('/aminoguess/answer', methods=['POST'])
def get_response_and_next_question():
    data = request.json

    answer = data['answer']
    list_features = data['list_features']
    last_feature = data['last_feature']
    proba_list = data['proba_list']
    final_img_list = data['final_img_list']
    nb_questions = data['nb_questions']
    max_questions = data['max_questions']
    data['nb_images'] = len(final_img_list)

    response = {
        'character': None,
        'fail': False,
        'feature': None,
        'question': None,
        'list_features': None,
        'proba_list': None
    }

    #actualisation des probas
    if answer != 2:
        proba_list = update_probabilities(data)
        response['proba_list'] = proba_list


    list_features[list_features.index(last_feature)] = None
    response['list_features'] = list_features


    # Si le max est 2 fois plus grand que le deuxième max, on peut proposer une réponse
    if max(proba_list) > 1.3*sorted(proba_list)[-2] or nb_questions == max_questions :
        guess_index = proba_list.index(max(proba_list))
        guess = final_img_list[guess_index]
        response['character']=guess
    # Si les probas sont trop faibles, on peut déclarer forfait
    elif max(proba_list) < 0.5 :
        response['fail']=True
    # Sinon on continue à jouer en posant une nouvelle question
    else :
        predicted_labels = data['predicted_labels']
        feature = get_questions(list_features, predicted_labels)

        # Prepare the response
        question = new_questions[feature]

        response['feature'] = feature
        response['question'] = question

    return response
    
@app.route('/aminoguess/proposition', methods=['POST'])
def continue_next_question():
    data = request.json

    proba_list = data['proba_list']
    final_img_list = data['final_img_list']
    list_features = data['list_features']
    predicted_labels = data['predicted_labels']

    guess_index = proba_list.index(max(proba_list))
    guess = final_img_list[guess_index]

    final_img_list[final_img_list.index(guess)] = None
    proba_list[guess_index] = 0

    feature = get_questions(list_features, predicted_labels)

    # Prepare the response
    question = new_questions[feature]
    

    return jsonify(
        feature=feature,
        question=question,
        final_img_list=final_img_list,
        proba_list=proba_list

    )


# Update the probabilities based on the user's answer
def update_probabilities(data):
    user_answer = data['answer']
    list_features = data['list_features']
    last_feature = data['last_feature']
    nb_images = data['nb_images']
    predicted_labels = data['predicted_labels']
    proba_list = data['proba_list']
    
    #update probabilities from players' answer
    index = list_features.index(last_feature)
    for i in range(nb_images):

        if user_answer == predicted_labels[i][index]:
            proba_list[i] *=  1 #proba_features[index]

        elif user_answer == 3:
            if predicted_labels[i][index] == 1:
                proba_list[i] *= 0.95
            else :
                proba_list[i] *= 0.90

            

        elif user_answer == 4:
            if predicted_labels[i][index] == 0:
                proba_list[i] *= 0.95
            else :
                proba_list[i] *= 0.90

            
        else:
            proba_list[i] *=  0.8

    return proba_list
    

if __name__ == '__main__':
    app.run(debug=True, port = 5002)