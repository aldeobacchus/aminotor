from flask import Flask, Response, jsonify, make_response, request, send_from_directory, session


from flask_cors import CORS
from flask_session import Session
import requests


app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax' # change to 'None' in prod and 'Lax' with postman
app.config['SESSION_COOKIE_SECURE'] = True # change to True in prod and False with postman
app.config['SESSION_COOKIE_NAME'] = 'AminotorSession'
Session(app)
CORS(app)

############################## INITIALISATION ##############################

#Racine
@app.route('/')
def hello():
    return 'Bienvenue chez orchestrateur'


############################## MAIN ##############################

if __name__ == '__main__':
    app.run(debug=True, port = 8000)
