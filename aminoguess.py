import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import requests


app = Flask(__name__)
CORS(app)

#première question du jeu
@app.route('/aminoguess/start/', methods=['POST'])
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
    server_path = "https://etud.insa-toulouse.fr/~alami-mejjat/0"

    list_path_upload = []
    for img in list_upload:
        list_path_upload.append(os.path.join(os.getcwd(),folder_name, f"{img}.jpg"))

    # create a list of path from the list of images from the initial server
    list_path_init = []  
    for i in range(nb_image):
        list_path_init.append(server_path+str(final_img_list[i])+".jpg")
    
    #predict labels on selected images
    data = {'list_path_upload':list_path_upload,
            'list_path_init':list_path_init
            }
    response = requests.post('http://localhost:5003/ml/predict/', json=data).json()

    predicted_labels = response.get('predicted_labels')
    
    data_labels = {
        'labels': list_features,
        'predicted_labels': predicted_labels
    }

    #donner la première question
    feature = get_questions(data_labels)
    
    return jsonify(
        final_img_list=final_img_list,
        predicted_labels=predicted_labels,
        feature=feature
    )


#update pour chaque question que l'on pose
@app.route('/aminoguess/answer/', methods=['POST'])
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
        'type': None,
        'character': None,
        'fail': False,
        'feature': None,
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
        response['type']="character"
    # Si les probas sont trop faibles, on peut déclarer forfait
    elif max(proba_list) < 0.5 :
        response['fail']=True
        response['type']="fail"
    # Sinon on continue à jouer en posant une nouvelle question
    else :
        predicted_labels = data['predicted_labels']
        data_labels = {"labels": list_features,"predicted_labels": predicted_labels}
        feature = get_questions(data_labels)
        response['feature'] = feature
        response['type']="question"

    return response
    
@app.route('/aminoguess/proposition/', methods=['POST'])
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

    data_labels = {"labels": list_features,"predicted_labels": predicted_labels}
    feature = get_questions(data_labels)

    return jsonify(
        feature=feature,
        final_img_list=final_img_list,
        proba_list=proba_list

    )

@app.route('/aminoguess/get_question/', methods=['POST'])
def process_questions():
    data = request.json if request.json else request.get_json()
    
    if not data:
        return "Erreur : Aucune donnée reçue dans la requête.", 400
    response = get_questions(data)
    print (response)
    return jsonify(feature=response)

def get_questions(data):

    labels = data['labels']
    predicted_labels = data['predicted_labels']

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
    app.run(debug=True, port = 5002)