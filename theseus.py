#fais moi un microservice similaire a ariane et aminoguess qui mele les fonctionnalité des deux de facon a ce que l'utilisatuer devine un personnage et que l'ordi devine un personnage
import os
import requests
from flask import Flask, jsonify, request
from random import randrange
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


#MS du mode de jeu 2 : start
#PENSEZ à RECUP la nouvelle version de FEATURES.PY
#début du jeu (choix de l'image et initialisation de la liste de questions)
@app.route('/theseus/start', methods=['POST'])
def start_game():
    data = request.json
    img_list = []
    
    list_image = data['list_image']
    nb_images = len(list_image)
    list_upload = data['list_upload']
    list_features = data['list_features']

    img_choice = randrange(0, nb_images)
    print(img_choice)

    #add the images uploaded by the user
    i=0
    while len(img_list) < nb_images and i < len(list_upload):
        img_list.append(list_upload[i])
        i += 1
    
    #add the images from the initial server
    i = 0
    while len(img_list) < nb_images:
        img_list.append(list_image[i])
        i += 1
    

    #TODO: change from the local server to the azure stockage service
    folder_name = "temp"

    list_path_upload = []
    for img in list_upload:
        list_path_upload.append(os.path.join(os.getcwd(),folder_name, f"{img}.jpg"))

    # create a list of path from the list of images from the initial server
    list_path_init = []  
    for i in range(nb_images):
        list_path_init.append("https://etud.insa-toulouse.fr/~alami-mejjat/0"+str(img_list[i])+".jpg")
    
    #predict labels on selected images
    data = {'list_path_upload':list_path_upload,
            'list_path_init':list_path_init
            }
    response = requests.post('http://localhost:5003/ml/predict', json=data).json()
    
    predicted_labels = response.get('predicted_labels')

    #donner la première question
    feature = get_questions(list_features, predicted_labels)

    return jsonify(
        img_list=img_list,
        predicted_labels=predicted_labels,
        feature=feature,
        img_choice=img_choice
    )


@app.route('/theseus/answer', methods=['POST'])
def get_response_and_next_question():
    data = request.json

    answer = data['answer']
    list_features = data['list_features']
    last_feature = data['last_feature']
    proba_list = data['proba_list']
    final_img_list = data['final_img_list']
    nb_questions = data['nb_questions']
    max_questions = data['max_questions']
    predicted_labels = data['predicted_labels']

    # Update the probabilities based on the answer
    if answer != 2:  # Assuming 2 means 'don't know' or similar
        proba_list = update_probabilities(proba_list, last_feature, answer, predicted_labels)
    
    # Update the list of features to avoid asking the same question again
    list_features.remove(last_feature)

    response = {
        'character': None,
        'fail': False,
        'feature': None,
        'list_features': list_features,
        'proba_list': proba_list
    }

    # Determine next action
    if max(proba_list) > 1.3 * sorted(proba_list)[-2] or nb_questions == max_questions:
        # Make a guess
        guess_index = proba_list.index(max(proba_list))
        guess = final_img_list[guess_index]
        response['character'] = guess
    elif max(proba_list) < 0.5:
        # Declare a fail
        response['fail'] = True
    else:
        # Continue with another question
        feature = get_questions(list_features, predicted_labels)
        response['feature'] = feature

    return jsonify(response)













def get_questions(labels, predicted_labels):

    nb_rows = len(predicted_labels) #number of elements in the grid
    print("nb rows", nb_rows)
    nb_col = len(predicted_labels[0]) #number of features
    print("nb col", nb_col)

    #init rate
    rate = []
    for i in range(0, nb_col):
        if labels[i]== None:
            rate.append(None)
        else :
            rate.append(0)

    #compute positive rate for each feature
    for i in range(0,nb_col):
        if rate[i]!= None:
            count = 0
            for j in range(0, nb_rows):
                if predicted_labels[j][i] is not None :
                    count = count + predicted_labels[j][i]
            rate[i]=(count/nb_rows)

    # There is None inside
    closest_rate = min([v for v in rate if v is not None], key=lambda x: abs(x - 0.5))
    closest_index = rate.index(closest_rate)
    chosen_label=labels[closest_index]

    print("chosen label", chosen_label)
    print("Closest rate to 0.5:", closest_rate)
    print("corresponding label:", chosen_label)
    
    return chosen_label
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
    app.run(debug=True, port = 5005)
