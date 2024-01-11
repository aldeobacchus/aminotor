import React, {useState} from 'react';
import SizePanelBar from '../SizePanelBar/SizePanelBar';
import SelectionPanel from '../SelectionPanel/SelectionPanel';
import Question from '../Question/Question';
import Guess from '../Guess/Guess';
import './Amino.css';

function Amino(args) {
  const [guess, setGuess] = useState('');
  const [boolFind, setBoolFind] = useState(false);
  const [question, setQuestion] = useState('');

  return (

    <div className="game_amino">

      {guess === '' && !boolFind && <>
        <Question setGuess={setGuess} question={question} sliderValue={args.sliderValue} setQuestion={setQuestion}/>
        <img className="character" src={`https://etud.insa-toulouse.fr/~alami-mejjat/${args.character}.jpg`} alt="Selected" /> 
      </>
      }

      {guess !== '' && !boolFind && <>
        <Guess guess={guess} setGuess={setGuess} setBoolFind={setBoolFind} setQuestion={setQuestion}/>
        <img className="character" src={`https://etud.insa-toulouse.fr/~alami-mejjat/${args.character}.jpg`} alt="Selected" />
      </>
      }

      {boolFind && (
        <div className="win">
          <h3>Excellent choix !</h3>
          <img className="character" src={`https://etud.insa-toulouse.fr/~alami-mejjat/${guess}.jpg`} alt="Selected" />
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