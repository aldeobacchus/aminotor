import random
from flask import Flask, jsonify, request
from ml import load_process_predict  # Import your ML functions
from flask_cors import cross_origin  # Fix the typo in import
from features import new_features, new_questions, new_answers  # Import new features, questions, and answers

app = Flask(__name__)

@app.route('/api/questions/', methods=['POST'])
<<<<<<< HEAD
@cross_origin()  # Enable Cross-Origin Resource Sharing (CORS)
def getQuestions():
    already_features = request.json.get('alreadyFeatures', [])
    params = request.json.get('params', [])
    answers = request.json.get('answers', [])
=======
def get_questions():
    # Votre logique pour générer les questions
    #get set of features
    label= ["id", "brown_hair", "blue_eyes", "browneyes"],
    grid = [[5, 1,0,1],[6, 0,0,1],[7, 0,1,0], [8, 1,0,1]]
    #initialize grid with pics : id and then value for labels

    nb_rows = len(grid) #number of elements in the grid
    print("nb rows", nb_rows)
    nb_col = len(grid[0]) #number of features

    #compute positive rate for each feature
    rate = []
    for i in range (0,nb_col): #we don't start at 0 since 0 is id and not a label
        count = 0
        for j in range (1, nb_rows):
            count = count + grid[i][j]
        print("count=", count)
        rate.append(count/nb_rows) #to do check that =/ 0
    
    #choose feature (the one with positive rate closest to 0.5)
    closest_rate = min(rate, key=lambda x: abs(x - 0.5))
    closest_index = rate.index(0.5)
    chosen_label=label[closest_index]

    print("chosen label", chosen_label)

    print("Closest rate to 0.5:", closest_rate)
    print("corresponding label:", chosen_label)

    #ask corresponding question
>>>>>>> 1a789febeb0d9331c6c2fde160b7372e2ef18a5a

    # Use load_process_predict to get predictions based on the provided features
    characterMatch = load_process_predict(_nb_images=len(already_features))

    # Your logic to select new features here...
    availableFeatures = set(new_features) - set(already_features)

<<<<<<< HEAD
    if not availableFeatures:
        return jsonify(characterMatch=characterMatch)  # Return the character if all features have been processed

    # Select a random new feature to ask a question about
    feature = random.choice(list(availableFeatures))
    question = new_questions[feature]
    param = feature

    # Prepare the response
    if feature in already_features:
        question += f" {characterMatch[feature]}?"
        param = f"is_{characterMatch[feature]}"

    return jsonify(
        feature=feature,
        param=param,
        question=question,
        answers=new_answers[feature],
        characterMatch=characterMatch
    )
=======
    # Validation de la réponse de l'utilisateur
    valid_answers = ["Yes", "No", "I don't know"]
    if user_answer in valid_answers:
        # Si la réponse est valide, traitez-la comme requis
        # update grid
        
        # Exemple de réponse pour /api/answer/
        response = {
            "message": f"Received answer: {user_answer}"
        }
        return jsonify(response)
    else:
        return jsonify({"error": "Invalid answer. Use 'Yes', 'No', or 'I don't know'."}), 400
>>>>>>> 1a789febeb0d9331c6c2fde160b7372e2ef18a5a

if __name__ == '__main__':
    app.run(debug=True)

