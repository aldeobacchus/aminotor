import requests
import json

app_url = 'http://127.0.0.1:5000/'

# Endpoint pour /api/questions/
questions_endpoint = 'api/questions/'

# Endpoint pour /api/answer/
answer_endpoint = 'api/answer/'

# Exemple de requête GET à /api/questions/
response_questions = requests.get(app_url + questions_endpoint)
if response_questions.status_code == 200:
    print("Requête pour /api/questions/ réussie ! Voici la réponse :")
    print(json.dumps(response_questions.json(), indent=4))
else:
    print("La requête pour /api/questions/ a échoué. Statut :", response_questions.status_code)

# Exemple de requête POST à /api/answer/ avec une réponse valide pour une caractéristique spécifique
valid_response = {
    "answer": "Yes",  # Remplacez par 'No' ou 'I don't know' selon votre besoin
    "feature": "Eyeglasses"  # Remplacez par une caractéristique existante parmi les nouvelles caractéristiques
}

response_answer = requests.post(app_url + answer_endpoint, json=valid_response)
if response_answer.status_code == 200:
    print("\nRequête pour /api/answer/ réussie ! Voici la réponse :")
    print(json.dumps(response_answer.json(), indent=4))
else:
    print("La requête pour /api/answer/ a échoué. Statut :", response_answer.status_code)

