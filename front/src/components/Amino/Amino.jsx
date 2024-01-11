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
          
      <h1>Amino'Guess</h1> 
      
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

      {boolFind && <>
        <h2>Bravo !</h2>
        <img className="character" src={`https://etud.insa-toulouse.fr/~alami-mejjat/${guess}.jpg`} alt="Selected" />
        <button onClick={() => args.setSelectionMode(true)}>Rejouer</button>
        <button onClick={() => args.setMode("home")}>Changer de mode de jeux</button>
      </>
      }


    
  </div>
  ) 
}

export default Amino