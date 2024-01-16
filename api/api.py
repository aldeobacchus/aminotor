from flask import Flask, Response, jsonify, make_response, request, send_from_directory, session
from flask_cors import cross_origin  # Fix the typo in import
from features import new_features, new_questions, proba_features  # Import new features, questions, and answers
from flask_cors import CORS
from flask_session import Session
import requests


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
@cross_origin(supports_credentials=True, origins="http://localhost:3000" )
def init_game(gamemod):

    if session.get('list_upload') is None:
        session['list_upload'] = []

    list_upload = session['list_upload']

    data = {
        'gamemod': gamemod,
        'nb_upload': len(list_upload)
    }

    response = requests.post('http://localhost:5001/image/init', json=data).json()
    session['list_image'] = response.get('list_image')

    return jsonify(
        list_upload=session['list_upload'],
        list_image=session['list_image']
        )


#première question du jeu
@app.route('/api/start/<int:nb_images>', methods=['GET'])
@cross_origin(supports_credentials=True, origins="http://localhost:3000")
def start_game(nb_images):

    session['list_features'] = new_features.copy()
    session['nb_images'] = nb_images
    data={
        'list_features': session['list_features'],
        'nb_images': session['nb_images'],
        'list_image': session['list_image'], 
        'list_upload': session['list_upload']
    }
    
    response = requests.post('http://localhost:5002/aminoguess/start', json=data).json()

    #initialisation et update the session variables
    session['max_questions'] = 10
    session['proba_list'] = [1]*nb_images
    session['final_img_list'] = response.get("final_img_list")
    session['last_feature'] = response.get("feature")
    session['question'] = response.get("question")
    session['nb_questions'] = 1
    session['predicted_labels'] = response.get("predicted_labels")

    return jsonify(
        feature=response.get("feature"),
        question=response.get("question")
    )


#update pour chaque question que l'on pose
@app.route('/api/answer/<int:answer>', methods=['GET'])
@cross_origin(supports_credentials=True, origins="http://localhost:3000")
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
    response = requests.post('http://localhost:5002/aminoguess/answer', json=data).json()
    feature = response.get('feature')
    question = response.get('question')

    if response.get('proba_list'):
        session['proba_list'] = response.get('proba_list')

    session['list_features'] = response.get("list_features")

    if question: # L'IA pose une nouvelle fonction
        session['last_feature'] = feature
        session['question'] = question
        session['nb_questions'] = session['nb_questions'] + 1

    return response
    
@app.route('/api/proposition/', methods=['GET'])
@cross_origin(supports_credentials=True, origins="http://localhost:3000")
def continue_next_question():

    data = {
        'list_features': session['list_features'],
        'proba_list': session['proba_list'],
        'final_img_list': session['final_img_list'],
        'predicted_labels': session['predicted_labels']
    }

    response = requests.post('http://localhost:5002/aminoguess/proposition', json=data).json()

    # update the session variables
    session['nb_questions'] = 1
    session['last_feature'] = response.get('feature')
    session['final_img_list'] = response.get('final_img_list')
    session['proba_list'] = response.get('proba_list')

    return jsonify(
        feature=response.get('feature'),
        question=response.get('question'),
    )

@app.route('/api/upload/', methods=['POST'])
@cross_origin(supports_credentials=True, origins="http://localhost:3000")
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

    response = requests.post('http://localhost:5001/image/upload', files=data).json()

    if session.get('list_upload') is None:
        session['list_upload'] = []

    list_upload = session['list_upload']

    list_upload.append(response.get('random_name'))

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

    if session.get('list_upload') is not None:
        list_upload = session['list_upload']

    data = {'list_upload': list_upload}

    response = requests.post('http://localhost:5001/image/delete', json=data).json()

    session['list_upload'] = []

    response = make_response(jsonify(success=True))
    response.delete_cookie('AminotorSession')

    return response

@app.route('/api/get_img/<int:img>', methods=['GET'])
@cross_origin(supports_credentials=True, origins="http://localhost:3000")
def get_img(img):
    print(img)
    response = requests.get('http://localhost:5001/image/get/{}'.format(img))
    
    return Response(response.content, content_type='image/jpeg')


    

if __name__ == '__main__':
    app.run(debug=True, port = 5000)