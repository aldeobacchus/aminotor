
# Instructions pour la configuration de l'environnement

## Création et activation d'un environnement virtuel

1. Créez un environnement virtuel :
   ```
   python -m venv venv
   ```
2. Activez l'environnement virtuel :
   - sur macOS et Linux :
     ```
     source venv/bin/activate
     ```
   - Sur Windows :
     ```
     venv\Scripts\activate
     ```

## Installation des dépendances

- Installez les dépendances requises depuis le fichier `requirements.txt` :
  ```
  pip install -r requirements.txt
  ```

## Utilisation de l'API

- Pour démarrer l'API, exécutez le fichier `api.py` :
  ```
  python api.py
  ```
  L'API sera disponible à l'adresse `http://localhost:5000`.

- Utilisez les endpoints suivants pour interagir avec l'API :
  - `/api/start/` (GET) : Obtenir une question aléatoire pour commencer le jeu.
  - `/api/questions/` (POST) : Recevoir et traiter les réponses de l'utilisateur et poser de nouvelles questions.

