import random
from flask import Flask, jsonify, request, send_from_directory, session
from random import randrange
from questions import get_questions
from ml import load_process_predict, load_process_images  # Import your ML functions
from flask_cors import cross_origin  # Fix the typo in import
from features import new_features, new_questions, proba_features  # Import new features, questions, and answers
from flask_cors import CORS
from flask_session import Session
import os
from flask import make_response


app = Flask(__name__)
#app.secret_key = os.environ.get('SECRET_KEY') #KEEP THIS LINE AND ADD THE KEY ON AZURE
app.secret_key = 'you-will-never-guess' # DON'T FORGET TO DELETE THIS LINE ON DEPLOYMENT
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_NAME'] = 'AminotorSession'
Session(app)
CORS(app)

#initialisation du jeu : sélection de 1024 images
@app.route('/api/init/<int:gamemod>', methods=['GET'])
@cross_origin(supports_credentials=True, origins="http://localhost:3000")
def init_game(gamemod):

    if session.get('list_upload') is None:
        list_image = []
    else :
        list_image = session['list_upload'].copy()

    nb_images_bdd = 40000

    if gamemod == 1:
        grid_size = 1024
    elif gamemod == 2:
        grid_size = 28

    while len(list_image) < grid_size:
        r = randrange(0, nb_images_bdd) + 52000 # the number of the images start at 52000
        if r not in list_image:
            list_image.append(r)

    session['list_image'] = list_image

    # envoie liste d'id images
    return jsonify(list_image)


#première question du jeu
@app.route('/api/start/<int:nb_images>', methods=['GET'])
@cross_origin(supports_credentials=True, origins="http://localhost:3000")
def start_game(nb_images):
    list_image = session['list_image']    
    final_img_list = []
    
    # list_features est égal à la valeur de new_features
    list_features = new_features.copy()

    #initialisation des variables de session
    session['max_questions'] = 10
    session['last_feature'] = None
    session['proba_list'] = [1]*nb_images

    # create a list of path from the list of images
    if session.get('list_upload') is None:
        list_upload = []
    else :
        list_upload = session['list_upload']

    nb_generated_img = nb_images-len(list_upload)
    print("nb generated img", nb_generated_img)

    list_path = []
    for i in range(nb_generated_img):
        final_img_list.append(list_image[i])
        list_path.append("https://etud.insa-toulouse.fr/~alami-mejjat/0"+str(final_img_list[i])+".jpg")
        print(final_img_list[i])

    #predict labels on selected images
    predicted_labels = load_process_predict(list_path)

    #donner la première question
    feature = get_questions(list_features, predicted_labels)
    question = new_questions[feature]

    #update the session variables
    session['final_img_list'] = final_img_list
    session['last_feature'] = feature
    session['nb_questions'] = 1
    session['predicted_labels'] = predicted_labels
    session['list_features'] = list_features


    return jsonify(
        feature=feature,
        question=question
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

    return proba_list

@app.route('/api/upload/', methods=['POST'])
@cross_origin(supports_credentials=True, origins="http://localhost:3000")
def upload_img():
    random_name = random.randint(1, 50000)
    print(random_name)
    file = request.files['image']

    # add mkdir if not exist
    folder_path = "./temp/"
    file.save(os.path.join(folder_path, f"{random_name}.jpg"))

    if session.get('list_upload') is None:
        list_upload = []
    else :
        list_upload = session['list_upload']

    list_upload.append(random_name)

    return jsonify(
        success=True
    )

@app.route('/api/flush_session/', methods=['GET'])
@cross_origin(supports_credentials=True, origins="http://localhost:3000")
def flush():
    flush_upload()
    session.clear()
    return jsonify(
        success=True
    )

@app.route('/api/flush_upload/', methods=['GET'])
@cross_origin(supports_credentials=True, origins="http://localhost:3000")
def flush_upload():
    if session.get('list_upload') is None:
        list_upload = []
    else :
        list_upload = session['list_upload']
        session['list_upload'] = []

    #delete the images from the temp folder
    folder_path = "./temp/"
    for img in list_upload:
        print(img)
        file = os.path.join(folder_path, f"{img}.jpg")
        if os.path.exists(file):
            os.remove(file)
    
    response = make_response(jsonify(success=True))
    response.delete_cookie('AminotorSession')
    
    return response

@app.route('/api/get_img/<int:img>', methods=['GET'])
@cross_origin(supports_credentials=True, origins="http://localhost:3000")
def get_img(img):
    img_folder = os.path.join(app.root_path, 'temp')
    return send_from_directory(img_folder, img)
            

if __name__ == '__main__':
    app.run(debug=True)