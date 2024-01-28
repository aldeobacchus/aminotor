from flask import Flask, Response, jsonify, make_response, request, send_from_directory, session

from flask_cors import cross_origin  # Fix the typo in import
from features import new_features, new_questions, answers
from flask_cors import CORS
from flask_session import Session
import requests

ms_image = 'https://initimageservice.azurewebsites.net/'
ms_aminoguess = 'https://aminoguessservice.azurewebsites.net/'
ms_ariane = 'https://arianeservice.azurewebsites.net/'
origin = 'https://aminotor.azurewebsites.net' #deployment
#origin = 'http://localhost:3000' #local

app = Flask(__name__)

#app.secret_key = os.environ.get('SECRET_KEY') #KEEP THIS LINE AND ADD THE KEY ON AZURE
app.secret_key = 'you-will-never-guess' # DON'T FORGET TO DELETE THIS LINE ON DEPLOYMENT
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_COOKIE_SAMESITE'] = 'None' # change to 'None' in prod and 'Lax' with postman
app.config['SESSION_COOKIE_SECURE'] = True # change to True in prod and False with postman
app.config['SESSION_COOKIE_NAME'] = 'AminotorSession'

Session(app)
CORS(app, supports_credentials=True, origins=origin)


############################## INITIALISATION ##############################

#Racine
@app.route('/')
def hello():
    return 'Bienvenue chez orchestrateur'


#initialisation du jeu : sélection des images
@app.route('/api/init/<int:gamemod>', methods=['GET'])
def init_game(gamemod):

    if session.get('list_upload') is None:
        session['list_upload'] = []

    list_upload = session['list_upload']

    data = {
        'gamemod': gamemod,
        'nb_upload': len(list_upload)
    }

    response = requests.post(ms_image+'image/init/', json=data).json()
    session['list_image'] = response.get('list_image')

    return jsonify(
        list_upload=session['list_upload'],
        list_image=session['list_image']
        )

############################## MODE DE JEU 1 - AMINOGUESS ##############################

#première question du jeu
@app.route('/api/aminoguess/start/<int:nb_images>', methods=['GET'])
def start_game_amino(nb_images):

    session['list_features'] = new_features.copy()
    session['nb_images'] = nb_images
    data={
        'list_features': session['list_features'],
        'nb_images': session['nb_images'],
        'list_image': session['list_image'], 
        'list_upload': session['list_upload']
    }
    
    response = requests.post(ms_aminoguess+'aminoguess/start/', json=data).json()

    #initialisation et update the session variables
    session['max_questions'] = 6
    session['proba_list'] = [1]*nb_images
    session['final_img_list'] = response.get("final_img_list")
    session['last_feature'] = response.get("feature")
    session['question'] = response.get("question")
    session['nb_questions'] = 1
    session['predicted_labels'] = response.get("predicted_labels")

    return jsonify(
        feature=response.get("feature"),
        question=new_questions[response.get("feature")]
    )

#update pour chaque question que l'on pose
@app.route('/api/aminoguess/answer/<int:answer>', methods=['GET'])
def get_response_and_next_question(answer):

    data = {
        'answer': answer,
        'list_features': session['list_features'],
        'last_feature': session['last_feature'],
        'proba_list': session['proba_list'],
        'final_img_list': session['final_img_list'],
        'nb_questions': session['nb_questions'],
        'max_questions': session['max_questions'],
        'predicted_labels': session['predicted_labels']
    }
    response = requests.post(ms_aminoguess+'aminoguess/answer/', json=data).json()
    feature = response.get('feature')
    
    reel_response = {
        'character': response.get('character'),
        'fail': response.get('fail'),
        'question': None,
    }

    if response.get('proba_list'):
        session['proba_list'] = response.get('proba_list')

    session['list_features'] = response.get("list_features")

    if response['type'] == "question": # L'IA pose une nouvelle question
        session['last_feature'] = feature

        question = new_questions[feature]
        reel_response['question'] = question
        session['question'] = question

        session['nb_questions'] = session['nb_questions'] + 1

    return reel_response
    
@app.route('/api/aminoguess/proposition/', methods=['GET'])
def continue_next_question():

    data = {
        'list_features': session['list_features'],
        'proba_list': session['proba_list'],
        'final_img_list': session['final_img_list'],
        'predicted_labels': session['predicted_labels']
    }

    response = requests.post(ms_aminoguess+'aminoguess/proposition/', json=data).json()

    # update the session variables
    session['nb_questions'] = 1
    session['last_feature'] = response.get('feature')
    session['final_img_list'] = response.get('final_img_list')
    session['proba_list'] = response.get('proba_list')

    return jsonify(
        feature=response.get('feature'),
        question=new_questions[response.get('feature')],
    )

####################### MODE DE JEU 2 - ARIANE #############################

@app.route('/api/ariane/start/', methods=['GET'])
def start_game_ariane():

    session['list_features_asked'] = new_features.copy()
    
    data={
        'list_features': session['list_features_asked'],
        'list_image': session['list_image'], 
        'list_upload': session['list_upload']
    }
    
    response = requests.post(ms_ariane+'ariane/start/', json=data).json()

    #initialisation et update the session variables
    session['final_img_list'] = response.get("final_img_list")
    session['max_guess'] = 3
    session['nb_guess'] = 0
    session['predicted_labels'] = response.get("predicted_labels")
    session['img_choice'] = response.get("img_choice")
    print(session['img_choice'])

    return jsonify(
        features=session['list_features_asked'] 
    )

@app.route('/api/ariane/feature/',  methods=['POST'])
def get_feature():
    #get post 
    data = request.get_json()
    session['last_feature'] = data.get('feature')
    session['list_answers'] = answers.copy()

    data = {
        'feature': session['last_feature'],
        'img_choice': session['img_choice'],
        'list_features': session['list_features_asked'],
        'predicted_labels': session['predicted_labels'],
        'list_answers': session['list_answers'] 
    }

    response = requests.post(ms_ariane+'ariane/feature/', json=data).json()

    #update the session variables
    session['list_features_asked'] = response.get('list_features')

    return jsonify(
        list_features=session['list_features_asked'],
        answer=response.get('answer')
    )

@app.route('/api/ariane/guess/<int:guess>', methods=['GET'])
def answer_proposition(guess):

    data = {
        'guess': guess,
        'img_choice': session['img_choice'],
        'nb_guess': session['nb_guess'],
        'max_guess': session['max_guess']
    }

    response = requests.post(ms_ariane+'ariane/guess/', json=data).json()

    #update the session variables
    session['nb_guess'] = response.get('nb_guess')

    return jsonify(
        result=response.get('result')
    )

############################## MODE DE JEU 3 - THESEUS ##############################

# It's the mix between the two previous games, the user have to guess and the AI have to guess
@app.route('/api/theseus/start/', methods=['GET'])
def start_game_theseus():
    
        session['list_features'] = new_features.copy()
        session['list_features_asked'] = new_features.copy()
        
        data={
            'list_features': session['list_features'],
            'list_image': session['list_image'], 
            'list_upload': session['list_upload']
        }
        
        response = requests.post(ms_ariane+'ariane/start/', json=data).json()

        #initialisation et update the session variables
        session['predicted_labels'] = response.get("predicted_labels")
        session['final_img_list'] = response.get("final_img_list")

        session['img_choice'] = response.get("img_choice")

        session['max_guess'] = 3
        session['nb_guess'] = 0
        
        session['proba_list'] = [1]*len(session['final_img_list'])
        session['type'] = None

        session['max_questions'] = 10
        session['nb_questions'] = 0

        return jsonify(
            features=session['list_features_asked']
        )

# the user ask for a feature
@app.route('/api/theseus/feature/',  methods=['POST'])
def get_feature_and_ask_question():
    data = request.get_json()
    session['last_feature'] = data.get('feature')
    session['list_answers'] = answers.copy()

    data_ariane = {
        'feature': session['last_feature'],
        'img_choice': session['img_choice'],
        'list_features': session['list_features_asked'],
        'predicted_labels': session['predicted_labels'],
        'max_questions': session['max_questions'],
        'nb_questions': session['nb_questions'],
        'list_answers': session['list_answers'] 
    }

    response_ariane = requests.post(ms_ariane+'ariane/feature/', json=data_ariane).json()

    session['list_features_asked'] = response_ariane.get('list_features')
    answer = response_ariane.get('answer')

    response = ask_question(answer)

    # GIVE THE ANSWER TO THE USER AND ASK HIM A QUESTION
    return response

# the user make a guess
@app.route('/api/theseus/guess/<int:guess>', methods=['GET'])
def answer_proposition_and_ask_question(guess):

    data_ariane = {
        'guess': guess,
        'img_choice': session['img_choice'],
        'nb_guess': session['nb_guess'],
        'max_guess': session['max_guess']
    }

    response_ariane = requests.post(ms_image+'ariane/guess/', json=data_ariane).json()

    #update the session variables
    session['nb_guess'] = response_ariane.get('nb_guess')

    result = response_ariane.get('result')

    if result == 1: # the user didn't found, we can continue the game
        response = ask_question(result)
    else : # the user found or loose, we can stop the game
        response = jsonify(answer=result)

    return response
    
# ASK QUESTION TO THE USER
def ask_question(answer):

    response = {
        'answer': answer,
        'character': None,
        'fail': False,
        'question': None,
    }

    data_amino= {
        'labels': session['list_features'],
        'predicted_labels': session['predicted_labels']
    }

    if session['type'] == None : # 1st question
        response_amino = requests.post(ms_aminoguess+'aminoguess/get_question/', json=data_amino).json()
        session['last_feature'] = response_amino.get('feature')
        response['question'] = new_questions[response_amino.get('feature')]
        session['nb_questions'] = session['nb_questions'] + 1
    elif session['type'] == "question":
        response['question'] = new_questions[session['question']]
        session['last_feature'] = session['question']
        session['nb_questions'] = session['nb_questions'] + 1
    elif session['type'] == "character":
        response['character'] = session['character']
    elif session['type'] == "fail":
        response['fail'] = True

    return response

# the user answer to the question
@app.route('/api/theseus/answer/<int:answer>', methods=['GET'])
def get_response_and_give_labels(answer):

    data_amino = {
        'answer': answer,
        'list_features': session['list_features'],
        'last_feature': session['last_feature'],
        'proba_list': session['proba_list'],
        'final_img_list': session['final_img_list'],
        'nb_questions': session['nb_questions'],
        'max_questions': session['max_questions'],
        'predicted_labels': session['predicted_labels']
    }
    response = requests.post(ms_aminoguess+'aminoguess/answer/', json=data_amino).json()
    feature = response.get('feature')

    if response.get('proba_list'):
        session['proba_list'] = response.get('proba_list')

    session['list_features'] = response.get("list_features")
    
    response_type = response.get('type')
    session['type'] = response_type

    if (response_type == "question"): # L'IA posera une nouvelle question
        session['question'] = feature # on garde la feature pour sauvegarder last_feature
    
    elif (response_type == "character"): # L'IA proposera un personnage
        session['character'] = response.get('character')

    # RETURN THE LABELS AVAILABLE FOR THE USER
    return jsonify(
        list_features=session['list_features_asked']
    )

# the user answer the AI guess
@app.route('/api/theseus/proposition/', methods=['GET'])
def wrong_proposition_and_give_labels():
    
        data_amino = {
            'list_features': session['list_features'],
            'proba_list': session['proba_list'],
            'final_img_list': session['final_img_list'],
            'predicted_labels': session['predicted_labels']
        }
    
        response_amino = requests.post(ms_aminoguess+'aminoguess/proposition/', json=data_amino).json()
    
        # update the session variables
        session['nb_questions'] = 0
        session['final_img_list'] = response_amino.get('final_img_list')
        session['proba_list'] = response_amino.get('proba_list')
        # the newt interaction will be a question
        session['type'] = "question"
        session['question'] = response_amino.get('feature')
    
        # RETURN THE LABELS AVAILABLE FOR THE USER
        return jsonify(
            list_features=session['list_features_asked']
        )



############################## IMAGES UPLOAD AND FLUSH COOKIES ##############################

@app.route('/api/upload/', methods=['POST'])
def upload_img():

    # check if image is uploaded
    if 'image' not in request.files:
        return jsonify(
            success=False
        )
    
    file = request.files['image']
    data = {
        'image': file
    }

    response = requests.post(ms_image+'image/upload', files=data).json()

    if session.get('list_upload') is None:
        session['list_upload'] = []


    list_upload = session['list_upload']

    list_upload.append(response.get('random_name'))

    return jsonify(
        success=True
    )   

@app.route('/api/flush_session/', methods=['GET'])
def flush():
    flush_upload()
    session.clear()
    return jsonify(
        success=True
    )

@app.route('/api/flush_upload/', methods=['GET'])
def flush_upload():

    if session.get('list_upload') is not None:
        list_upload = session['list_upload']

    data = {'list_upload': list_upload}

    response = requests.post(ms_image+'image/delete', json=data).json()

    session['list_upload'] = []

    response = make_response(jsonify(success=True))
    response.delete_cookie('AminotorSession')

    return response

@app.route('/api/get_img/<int:img>', methods=['GET'])
def get_img(img):
    print(img)
    response = requests.get(ms_image+'image/get/{}'.format(img))

    
    return Response(response.content, content_type='image/jpeg')


############################## MAIN ##############################

if __name__ == '__main__':
    app.run(debug=True, port = 5000)
