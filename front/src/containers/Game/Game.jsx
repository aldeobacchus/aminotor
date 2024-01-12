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

      {<h2>{args.gm}</h2>}
      
      {selectionMode && (
        <CharacterSelection setSelectionMode={setSelectionMode} setSelectedImage={setCharacter} setSliderValue={setSliderValue}/>
      )}

      {!selectionMode && args.gm === "Amino'Guess" && (
        <Amino character={character} sliderValue={sliderValue} setMode={args.setMode} setSelectionMode={setSelectionMode}/>
      )}

      {!selectionMode && args.gm === "Theseus Battle" && (
        <Theseus character={character} setMode={args.setMode}/>
      )}
      
    </div>
  )
}

export default Game