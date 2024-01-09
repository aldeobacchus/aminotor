import random
from flask import Flask, jsonify, request
from random import randrange
from questions import get_questions
from ml import load_process_predict, load_process_images  # Import your ML functions
from flask_cors import cross_origin  # Fix the typo in import
from features import new_features, new_questions, new_answers  # Import new features, questions, and answers

app = Flask(__name__)

@app.route('/api/init', methods=['GET'])
def init_game():
    #sélection de 1024 images au hasard
    global list_image
    nb_images_bdd = 10000
    for i in range(1024):
        list_image.add(randrange(nb_images_bdd))

    #get images de la bdd à partir de leurs id
        
    #renvoie les images au front


@app.route('/api/start/{nb_images}', methods=['GET'])
def start_game(nb_images):
    data = request.get_json()

    global final_img_list 
    global images, model, predicted_labels, nb_questions, max_questions, last_feature, proba_list
    
    #create img list from size selected by user
    for i in range(nb_images):
        final_img_list.add(list_image[i])

    #predict labels on selected images
    predicted_labels = load_process_predict(nb_images)

    nb_questions = 0
    max_questions = 10

    last_feature = None

    proba_list = [0 for i in range(nb_images)]

    #donner la première question
    feature = get_questions(new_features, predicted_labels)
    question = new_questions[feature]

    return jsonify(
        feature=feature,
        #param=param,
        question=question,
        answers=new_answers[feature],
        #characterMatch=characterMatch
    )




@app.route('/api/questions/', methods=['GET'])
def get_questions():
    already_features = request.json.get('alreadyFeatures', [])
    params = request.json.get('params', [])
    answers = request.json.get('answers', [])

    # Use load_process_predict to get predictions based on the provided features
    #characterMatch = load_process_predict(_nb_images=len(already_features))

    availableFeatures = set(new_features) - set(already_features)

    #do the same for the labels

    if not availableFeatures:
        return jsonify(characterMatch=characterMatch)  # Return the character if all features have been processed

    # Select a random new feature to ask a question about
    #feature = random.choice(list(availableFeatures))
    feature = get_questions(availableFeatures, )
    question = new_questions[feature]
    param = feature

    # Prepare the response
    if feature in already_features:
        question += f" {characterMatch[feature]}?"
        param = f"is_{characterMatch[feature]}"

    nb_questions +=1
    last_feature = param

    return jsonify(
        feature=feature,
        param=param,
        question=question,
        answers=new_answers[feature],
        characterMatch=characterMatch
    )


@app.route('/api/answer/', methods=['POST'])
def receive_answer():
    data = request.get_json()
    user_answer = data.get('answer')
    if nb_questions < max_questions:

        # Validation de la réponse de l'utilisateur
        valid_answers = ["Yes", "No", "I don't know"]
        if user_answer in valid_answers:
            
            #update probabilities from players' answer
            index = new_features.index(last_feature)
            for i in range (0, N-1):
                proba_list[i] = proba_list[i] + predicted_labels[i][index]

            response = {
                "message": f"Received answer: {user_answer}"
            }
            return jsonify(response)
        else:
            return jsonify({"error": "Invalid answer. Use 'Yes', 'No', or 'I don't know'."}), 400
        
    else : #max amount of questions reached => try to guess !!

        guess_index = proba_list.index(max(proba_list))
        guess = new_features[guess_index]
        # return quoi ???

if __name__ == '__main__':
    app.run(debug=True)
