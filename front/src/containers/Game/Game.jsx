import React, {useState} from 'react'
import SizePanelBar from '../../components/SizePanelBar/SizePanelBar';
import SelectionPanel from '../../components/SelectionPanel/SelectionPanel';
import Amino from '../../components/Amino/Amino';
import Theseus from '../../components/Theseus/Theseus';
import CharacterSelection from '../../components/CharacterSelection/CharacterSelection';

function Game(args) {
  const [selectionMode, setSelectionMode] = useState(true);
  const [character, setCharacter] = useState(null);
  const [sliderValue, setSliderValue] = useState(null);


  return (
    <div className='game'>
      
      {selectionMode && (
        <CharacterSelection setSelectionMode={setSelectionMode} setSelectedImage={setCharacter} setSliderValue={setSliderValue}/>
      )}

      {!selectionMode && args.gm === 'Amino' && (
        <Amino character={character} sliderValue={sliderValue} setMode={args.setMode} setSelectionMode={setSelectionMode}/>
      )}

      {!selectionMode && args.gm === 'Theseus' && (
        <Theseus character={character}/>
      )}
      
    </div>
  )
}

export default Game