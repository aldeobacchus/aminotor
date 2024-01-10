import React from 'react'
import SizePanelBar from '../SizePanelBar/SizePanelBar';
import SelectionPanel from '../SelectionPanel/SelectionPanel';

function Theseus(args) {
  return (
    
    <div className="game_theseus">
          
      <h1>Theseus</h1>
      
      <img src={`/img/200/${args.character}.jpg`} alt="Selected" /> 

    </div> 

    )
}

export default Theseus