import random
from flask import Flask, jsonify, request
from ml import load_process_predict  # Import your ML functions
from flask_cors import cross_origin  # Fix the typo in import
from features import new_features, new_questions, new_answers  # Import new features, questions, and answers
import numpy as np

app = Flask(__name__)



@app.route('/api/start/', methods=['GET'])
@cross_origin()
def start():
    # Randomly select a question from the dictionary
    question = random.choice(list(new_questions.values()))

    # Return the question text as a simple string
    return jsonify(question=question)


@app.route('/api/questions/', methods=['POST'])
@cross_origin()
def getQuestions():
    # Récupération de la question précédente et de la réponse de l'utilisateur
    previous_question = request.json.get('previous_question')
    user_answer = request.json.get('user_answer')  # 'oui' ou 'non'

    # Traitement de la réponse et mise à jour des caractéristiques déjà traitées
    already_features = request.json.get('alreadyFeatures', [])
    if previous_question:
        feature_of_previous_question = [feature for feature, question in new_questions.items() if question == previous_question][0]
        if user_answer.lower() == 'oui':
            already_features.append(feature_of_previous_question)

    # Utiliser load_process_predict pour obtenir des prédictions basées sur les caractéristiques fournies
    # Votre logique de traitement basée sur les réponses, ajustez selon le besoin
    load_process_predict(_nb_images=len(already_features))

    # Sélection d'une nouvelle caractéristique à demander
    availableFeatures = set(new_features) - set(already_features)
    if not availableFeatures:
        # Vous pouvez choisir de gérer différemment la fin du jeu ici
        return jsonify(new_question="Game Over or Character Found")

    new_feature = random.choice(list(availableFeatures))
    new_question = new_questions[new_feature]

    # Retourne uniquement la nouvelle question
    return jsonify(new_question=new_question)

if __name__ == '__main__':
    app.run(debug=True)
