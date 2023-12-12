import random
from flask import Flask, jsonify, request
from ml import load_process_predict  # Import your ML functions
from flask_cors import cross_origin  # Fix the typo in import
from features import new_features, new_questions, new_answers  # Import new features, questions, and answers

app = Flask(__name__)

@app.route('/api/questions/', methods=['POST'])
@cross_origin()  # Enable Cross-Origin Resource Sharing (CORS)
def getQuestions():
    already_features = request.json.get('alreadyFeatures', [])
    params = request.json.get('params', [])
    answers = request.json.get('answers', [])

    # Use load_process_predict to get predictions based on the provided features
    characterMatch = load_process_predict(_nb_images=len(already_features))

    # Your logic to select new features here...
    availableFeatures = set(new_features) - set(already_features)

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

if __name__ == '__main__':
    app.run(debug=True)

