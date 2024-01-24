import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Question.css';


// Set withCredentials to true globally
axios.defaults.withCredentials = true;

function Question(args) {
  const [question, setQuestion] = useState(args.question);
  const [nombreAleatoire, setNombreAleatoire] = useState(1);


  useEffect(() => {
    const fetchData = async () => {
      if (question === '') {
        console.log(question);
        const grid_size = 2**(args.sliderValue*2);
        const response = await axios.get(`http://127.0.0.1:5000/api/aminoguess/start/${grid_size}`, { withCredentials: true })
        setQuestion(response.data.question);
        console.log(question);
        return question;
      }
    }

    //fetch data
    fetchData();
  }, []); 

    function answer(arg) {
      axios.get('http://127.0.0.1:5000/api/aminoguess/answer/'+arg)
        .then(response => {
          if (response.data.character) {
            const guess = response.data.character;
            console.log(guess);
            args.setGuess(args.charactersSources[args.characters.indexOf(guess)])
          }
          else if (response.data.fail) {
            args.setGuess("fail");
          }
          setQuestion(response.data.question);
        })
        .catch(error => {
          console.error('Erreur lors de la récupération de la question', error);
        });

        // Générer un nombre aléatoire entre 1 et 2
        const nombreDecimal = 1 + Math.random();
        const nombreFinal = nombreDecimal < 0.5 ? 1 : 2;
        // Mettre à jour l'état avec le nombre aléatoire généré
        setNombreAleatoire(nombreFinal);
    }

  if (question !== '') {
      return (
          <div className='question'>
              <h4>Question : {question}</h4>
              <div className="answer-container">
                {/* TODO CHANGER DE PLACE VERS AMINO */}
                {nombreAleatoire === 1 ? <img className="minotor" src='img/minotors/NORMAL.png' alt="image1" /> : <img className="minotor" src='img/minotors/LAMP.png' alt="image2"/>}
                <div className="answer-container2">
                  <div className='answer'>
                    <button onClick={() => answer(1)}>Oui</button>
                    <button onClick={() => answer(0)}>Non</button>
                  </div>

                  <div className='answer'>
                    <button onClick={() => answer(3)}>Je pense que oui</button>
                    <button onClick={() => answer(2)}>Je ne sais pas</button>
                    <button onClick={() => answer(4)}>Je pense que non</button>
                  </div>
                </div>
                <div className='answer-container-padding'></div>
              </div>
          </div>
    )
    } else {
      return (
        <div className='wait'>
            <h3>Laissez-moi réfléchir un instant...</h3>
        </div>
      )
    }

}

export default Question