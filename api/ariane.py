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
    final_img_list = []
    
    list_image = data['list_image']
    nb_images = len(list_image)
    list_upload = data['list_upload']

    img_choice = randrange(0, nb_images)
    print(img_choice)

    #add the images uploaded by the user
    i=0
    while len(final_img_list) < nb_images and i < len(list_upload):
        final_img_list.append(list_upload[i])
        i += 1
    
    #add the images from the initial server
    i = 0
    while len(final_img_list) < nb_images:
        final_img_list.append(list_image[i])
        i += 1

    #TODO: change from the local server to the azure stockage service
    folder_name = "temp"
    server_path = "https://etud.insa-toulouse.fr/~alami-mejjat/0"

    list_path_upload = []
    for img in list_upload:
        list_path_upload.append(os.path.join(os.getcwd(),folder_name, f"{img}.jpg"))

    # create a list of path from the list of images from the initial server
    list_path_init = []  
    for i in range(nb_images):
        list_path_init.append(server_path+str(final_img_list[i])+".jpg")
    
    #predict labels on selected images
    data = {'list_path_upload':list_path_upload,
            'list_path_init':list_path_init,
            'nb_images': nb_images
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

    if all(f is None for f in list_features):
        return jsonify(
            list_features = list_features, 
            answer="Il n'y a plus de questions possibles.."
        )

    else:
        #get AI answer from predicted labels
        nb_feature = list_features.index(feature)
        answer = predicted_labels[img_choice][nb_feature]

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