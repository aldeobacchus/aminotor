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
@app.route('/ariane/start/', methods=['POST'])
def start_game():
    data = request.json
    
    nb_images = data['nb_images']
    image_list = data['image_list']
    image_urls = data['image_urls']

    # create a list of path from the list of images from the initial server
    list_path_init = []  
    final_img_list = []
    for i in range(nb_images):
        list_path_init.append(image_urls[i])
        final_img_list.append(image_list[i])
    
    random = randrange(0, nb_images-1)
    img_choice = final_img_list[random]
    print(img_choice)

    #predict labels on selected images
    data = {
            'list_path_init':list_path_init
            }
    response = requests.post('http://localhost:5003/ml/predict/', json=data).json()

    predicted_labels = response.get('predicted_labels')

    return jsonify(
        final_img_list=final_img_list,
        predicted_labels=predicted_labels,
        img_choice=img_choice
    )

#MS du mode de jeu 2
#get la feature/question que le joueur a choisi et répondre
@app.route('/ariane/feature/', methods=['POST'])
def get_feature():

    data = request.json
    feature = data['feature']
    img_choice = data['img_choice']
    list_features = data['list_features']
    predicted_labels = data['predicted_labels']
    list_answers = data['list_answers']
    image_list = data['image_list']

    if all(f is None for f in list_features):
        return jsonify(
            list_features = list_features, 
            answer="Il n'y a plus de questions possibles.."
        )

    else:
        #get AI answer from predicted labels
        index_image = image_list.index(img_choice)
        nb_feature = list_features.index(feature)
        answer = predicted_labels[index_image][nb_feature]

        result = list_answers[list_features[nb_feature]][int(answer)]
        
        #update list of features so the player can't ask the same question twice
        list_features[nb_feature] = None


        return jsonify(
            list_features = list_features, 
            answer=result
        )
     
    
#MS du mode de jeu 2
@app.route('/ariane/guess/', methods=['POST'])
def answer_proposition():
    data = request.json
    player_guess = data['guess']
    img_choice = data['img_choice']
    nb_guess = data['nb_guess']
    max_guess = data['max_guess']

    nb_guess = nb_guess + 1
    
    if img_choice == player_guess:
        result = 0 #image trouvée
    elif nb_guess == max_guess:
        result = 2 #fin du jeu car trop d'essais
    else: 
        result = 1 #pas trouvé, on continue de jouer

    return jsonify(
        result = result,
        nb_guess = nb_guess
    ) 


if __name__ == '__main__':
    app.run(debug=True, port = 5004)