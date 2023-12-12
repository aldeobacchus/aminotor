import React from 'react'
import SizePanelBar from '../../components/SizePanelBar/SizePanelBar';
import SelectionPanel from '../../components/SelectionPanel/SelectionPanel';
import { useState } from 'react';
import Amino from '../../components/Amino/Amino';
import Theseus from '../../components/Theseus/Theseus';
import CharacterSelection from '../../components/CharacterSelection/CharacterSelection';

function Game(args) {
  const [selectionMode, setSelectionMode] = useState(true);
  const [character, setCharacter] = useState(null);
  const [question, setQuestion] = useState(null);

  return (
    <div className='game'>
      
      {selectionMode && (
        <CharacterSelection setSelectionMode={setSelectionMode} setSelectedImage={setCharacter}/>
      )}

      {!selectionMode && args.gm === 'Amino' && (
        <Amino character={character} question/>
      )}

      {!selectionMode && args.gm === 'Theseus' && (
        <Theseus character={character}/>
      )}
      
    </div>
  )
}

export default Game