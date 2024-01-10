import React from 'react'
import SizePanelBar from '../SizePanelBar/SizePanelBar';
import SelectionPanel from '../SelectionPanel/SelectionPanel';
import Question from '../Question/Question';
import './Amino.css';

function Amino(args) {
  const [boolFind, setBoolFind] = React.useState(false);
  
  return (

    <div className="game_amino">
          
      <h1>Amino'Guess</h1> 
      
      {!boolFind && <>
        <Question setBoolFind={setBoolFind}/>
        <img className="character" src={`https://etud.insa-toulouse.fr/~alami-mejjat/${args.character}.jpg`} alt="Selected" /> 
      </>
      }

      {boolFind && <>
        <h2>Eheh bravo qui ? Bravo bibi ! Je sais qui t'as !</h2>
        <h3>Je suis trop fort !</h3>
        <h4>Tu as : </h4>
        <img className="character" src={`https://etud.insa-toulouse.fr/~alami-mejjat/${args.character}.jpg`} alt="Selected" />
        <button onClick={() => setBoolFind(false)}>Rejouer</button>
      </>
      }


    
  </div>
  ) 
}

export default Amino