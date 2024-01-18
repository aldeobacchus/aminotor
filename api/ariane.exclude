import random
from flask import Flask, jsonify, request, session
from random import randrange
from questions import get_questions
from ml import load_process_predict, load_process_images  # Import your ML functions
from flask_cors import cross_origin  # Fix the typo in import
from features import new_features, new_questions, answers  # Import new features, questions, and answers
from flask_cors import CORS



app = Flask(__name__)
CORS(app)


#MS du mode de jeu 2 : start
#PENSEZ à RECUP la nouvelle version de FEATURES.PY
#début du jeu (choix de l'image et initialisation de la liste de questions)
@app.route('/ariane/start', methods=['GET'])
def start_game():


    list_image = session['list_image']

    nb_images = len(list_image)
    #choix de l'image
    img_choice = randrange(0, nb_images)

    # list_features est égal à la valeur de new_features
    list_features = new_features.copy()
    list_answers = answers.copy()


    # create a list of path from the list of images
    list_path = []  
    for i in range(nb_images):
        list_path.append("https://etud.insa-toulouse.fr/~alami-mejjat/0"+str(list_image[i])+".jpg")

    #predict labels on selected images
    predicted_labels = load_process_predict(list_path)

    #eliminate irrelevant features from list
    nb_rows = len(predicted_labels) #number of elements in the grid
    nb_col = len(predicted_labels[0]) #number of features
    for i in range(0,nb_col):
        if list_features[i]!= None:
            count = 0
            for j in range(0, nb_rows):
                if predicted_labels[j][i] is not None :
                    count = count + predicted_labels[j][i]
            if count == 0 : #to do : vérifier qu'on garde bien cette partie
                list_features[i] == None

    #update the session variables
    session['img_choice'] = img_choice
    session['predicted_labels'] = predicted_labels
    session['list_features'] = list_features
    session['list_answers'] = list_answers


    return jsonify(
        list_features=list_features,
    )

#MS du mode de jeu 2
#get la feature/question que le joueur a choisi et répondre
@app.route('/api2/feature/<string:feature>', methods=['GET'])
@cross_origin(supports_credentials=True, origins="http://localhost:3000")
def get_feature(feature):

    img_choice = session['img_choice']
    list_features = session['list_features']
    predicted_labels = session['predicted_labels']
    max_questions = session['max_questions']
    nb_questions = session['nb_questions']
    list_answers = session['list_answers'] 


    if nb_questions < max_questions :
        #get AI answer from predicted labels
        nb_feature = list_features.index(nb_feature)
        answer = predicted_labels[img_choice][nb_feature]
        print(int(answer))

        result = list_answers[list_features[nb_feature]][int(answer)]
        
        #update list of features so the player can't ask the same question twice
        list_features[nb_feature] = None


        #update the session variables
        session['last_feature'] = feature
        session['list_features'] = list_features


        return jsonify(
            list_features = list_features, 
            answer=result
        )
     
    
#MS du mode de jeu 2
@app.route('/api2/proposition/<int:guess>', methods=['GET'])
@cross_origin(supports_credentials=True, origins="http://localhost:3000")
def answer_proposition(guess):
    player_guess = guess
    img_choice = session['img_choice']
    nb_guess = session['nb_guess']
    max_guess = session['max_guess']

    nb_guess = nb_guess + 1
    
    if img_choice == player_guess:
        result = 0 #image trouvée
    elif nb_guess == max_guess:
        result = 2 #fin du jeu car trop d'essais
    else: 
        result = 1 #pas trouvé, on continue de jouer


    session['nb_guess']= nb_guess 
    #update the session variables    

    return jsonify(
        result = result,
        guess = guess
    ) 


if __name__ == '__main__':
    app.run(debug=True, port = 5004)