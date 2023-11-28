from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/api/questions/', methods=['POST'])
def get_questions():
    # Votre logique pour générer les questions
    # ...

    # Exemple de réponse pour /api/questions/
    response = {
        "answers": ["Yes", "No"],
        "feature": "facial_hair",
        "param": "facial_hair",
        "question": "Does the character have facial hair? "
    }
    return jsonify(response)

@app.route('/api/answer/', methods=['POST'])
def receive_answer():
    data = request.get_json()
    user_answer = data.get('answer')

    # Validation de la réponse de l'utilisateur
    valid_answers = ["Yes", "No", "I don't know"]
    if user_answer in valid_answers:
        # Si la réponse est valide, traitez-la comme requis
        # ...

        # Exemple de réponse pour /api/answer/
        response = {
            "message": f"Received answer: {user_answer}"
        }
        return jsonify(response)
    else:
        return jsonify({"error": "Invalid answer. Use 'Yes', 'No', or 'I don't know'."}), 400

if __name__ == '__main__':
    app.run(debug=True)

