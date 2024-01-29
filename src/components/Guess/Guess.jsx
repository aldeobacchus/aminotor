import React, { useState } from 'react';
import axios from 'axios';
import './guess.css';

// Set withCredentials to true globally
axios.defaults.withCredentials = true;


function Guess(args) {

  const [loading, setLoading] = useState(false);

  function answerYes() {
    args.setBoolFind(true);
  }

  function answerNo() {
    setLoading(true);
    axios.get('http://127.0.0.1:5000/api/aminoguess/proposition/')
      .then(response => {
        args.setQuestion(response.data.question);
        args.setGuess('');
        setLoading(false);
      })
      .catch(error => {
        console.error('Erreur lors de la récupération de la question', error);
      });
  }

  return (
    <div className="guess">
      {!loading && (
        <>
          <h2>Penses-tu à cette personne ?</h2>
          <img className="character" src={args.guess} alt="Selected" />
          <div className="answer-sol">
            <button onClick={() => answerYes()}>Oui</button>
            <button onClick={() => answerNo()}>Non</button>
          </div>
        </>
      )}
      {loading && (
        <span class="loader2"></span>
      )}
    </div>
  );
}

export default Guess;
