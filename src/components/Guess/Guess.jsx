import React from 'react';
import axios from 'axios';
import './guess.css';

// Set withCredentials to true globally
axios.defaults.withCredentials = true;



function Guess(args) {

    function answerYes() {
      args.setBoolFind(true);
    }

    function answerNo() {
        axios.get('https://orchestratorservice1.azurewebsites.net/api/proposition/')
          .then(response => {
            args.setQuestion(response.data.question);
            args.setGuess('');
          })
          .catch(error => {
            console.error('Erreur lors de la récupération de la question', error);
          });   
    }

  return (
    <div className="guess">
      <h2>Penses-tu à cette personne ?</h2>
      <img className="character" src={args.guess} alt="Selected" />
      <div className="answer-sol">
        <button onClick={() => answerYes()}>Oui</button>
        <button onClick={() => answerNo()}>Non</button>
      </div>
    </div>
  );
}

export default Guess;
