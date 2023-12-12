import React from 'react'
import SizePanelBar from '../SizePanelBar/SizePanelBar';
import SelectionPanel from '../SelectionPanel/SelectionPanel';
import Question from '../Question/Question';
import './Amino.css';

function Amino(args) {
  return (

    <div className="game_amino">
          
      <h1>Amino's Guess</h1> 
      
      <Question />  

      <img className="character" src={`/img/200/${args.character}.jpg`} alt="Selected" /> 
    
  </div>
  )
}

export default Amino