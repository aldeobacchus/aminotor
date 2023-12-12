import React from 'react'
import SizePanelBar from '../../components/SizePanelBar/SizePanelBar';
import SelectionPanel from '../../components/SelectionPanel/SelectionPanel';
import { useState } from 'react';
import Amino from '../../components/Amino/Amino';
import Theseus from '../../components/Theseus/Theseus';
import CharacterSelection from '../../components/CharacterSelection/CharacterSelection';

function Game(args) {
  const [selectionMode, setSelectionMode] = useState(true);

  return (
    <div className='game'>
      
      {selectionMode && (
        <CharacterSelection setSelectionMode={setSelectionMode}/>
      )}

      {!selectionMode && args.gm === 'Amino' && (
        <div className="game_amino">
          
          <h1>Amino's Guess</h1>  
        </div>
        
      )}

      {!selectionMode && args.gm === 'Thesus' && (
        <div className="game_thesus">
          
        <h1>Thesus battle</h1>  
 
      </div> 
      )}
      
    </div>
  )
}

export default Game