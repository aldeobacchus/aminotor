import React, {useState} from 'react';
import Question from '../Question/Question';
import Guess from '../Guess/Guess';
import './Amino.css';

function Amino(args) {
  const [guess, setGuess] = useState('');
  const [boolFind, setBoolFind] = useState(false);
  const [question, setQuestion] = useState('');
  const [isFocused, setIsFocused] = useState(false);

  const handleClick = event => {
    setIsFocused(current => !current);
  };
  return (

    <div className="game_amino">

      {!guess && !boolFind && <>
        <Question setGuess={setGuess} question={question} sliderValue={args.sliderValue} setQuestion={setQuestion} characters={args.characters} charactersSources={args.charactersSources}/>
        <img className={isFocused ? "characterFocus" : "character mycharacter"} onClick={handleClick} src={args.character} alt="Selected" /> 
      </>
      }

      {guess === 'fail' && !boolFind && <>
        <h3>Désolé, je n'ai pas trouvé..</h3>
        <div className="answer">
          <button onClick={() => args.setSelectionMode(true)}>Rejouer</button>
          <button onClick={() => args.setMode("home")}>Changer de mode de jeux</button>
        </div>
      </>
      }

      {guess && guess !== 'fail' && !boolFind && <>
        <Guess guess={guess} setGuess={setGuess} setBoolFind={setBoolFind} setQuestion={setQuestion}/>
        <img className={isFocused ? "characterFocus" : "character mycharacter"} onClick={handleClick} src={args.character} alt="Selected" />
      </>
      }

      {boolFind && (
        <div className="win">
          <h3>Excellent choix !</h3>
          <img className="character" src={guess} alt="Selected" />
          <div className="answer">
            <button onClick={() => args.setSelectionMode(true)}>Rejouer</button>
            <button onClick={() => args.setMode("home")}>Changer de mode de jeux</button>
          </div>
        </div>
      )}


    
  </div>
  ) 
}

export default Amino