import React, {useEffect} from 'react';
import axios from 'axios';
import './Question.css';

// Set withCredentials to true globally
axios.defaults.withCredentials = true;

function Question(args) {
  const [question, setQuestion] = React.useState(args.question);

  useEffect(() => {
    const fetchData = async () => {
      if (question === '') {
        console.log(question);
        const grid_size = 2**(args.sliderValue*2);
        const response = await axios.get(`http://127.0.0.1:5000/api/start/${grid_size}`, { withCredentials: true })
        setQuestion(response.data.question);
        console.log(question);
        return question;
      }
    }
    fetchData();
  }, []); 

  function answerYes() {
    axios.get('http://127.0.0.1:5000/api/answer/1')
      .then(response => {
        if (response.data.character) {
          const paddedCharacter = response.data.character.toString().padStart(6, '0');
          args.setGuess(paddedCharacter);
        }
        else if (response.data.fail === true) {
          args.setGuess("fail");
        }
        setQuestion(response.data.question);
      })
      .catch(error => {
        console.error('Erreur lors de la récupération de la question', error);
      });
    }

    function answerNo() {
      axios.get('http://127.0.0.1:5000/api/answer/0')
        .then(response => {
          if (response.data.character) {
            const paddedCharacter = response.data.character.toString().padStart(6, '0');
            args.setGuess(paddedCharacter);
          }
          else if (response.data.fail) {
            args.setGuess("fail");
          }
          setQuestion(response.data.question);
        })
        .catch(error => {
          console.error('Erreur lors de la récupération de la question', error);
        });
    }

    function answerDontKnow() {
      axios.get('http://127.0.0.1:5000/api/answer/2')
        .then(response => {
          if (response.data.character) {
            const paddedCharacter = response.data.character.toString().padStart(6, '0');
            args.setGuess(paddedCharacter);
          }
          else if (response.data.fail) {
            args.setGuess("fail");
          }
          setQuestion(response.data.question);
        })
        .catch(error => {
          console.error('Erreur lors de la récupération de la question', error);
        });
    }

  if (question !== '') {
      return (
          <div className='question'>
              <h4>Question : {question}</h4>
              <div className='answer'>
                <button onClick={() => answerYes()}>Oui</button>
                <button onClick={() => answerNo()}>Non</button>
                <button onClick={() => answerDontKnow()}>Je ne sais pas</button>
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