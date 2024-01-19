import React, {useState} from 'react'
import Amino from '../../components/Amino/Amino';
import Theseus from '../../components/Theseus/Theseus';
import CharacterSelection from '../../components/CharacterSelection/CharacterSelection';
import './game.css'
import UserGrid from '../../components/UserGrid/UserGrid';

function Game(args) {
  const [selectionMode, setSelectionMode] = useState(true);
  const [character, setCharacter] = useState(null);
  const [sliderValue, setSliderValue] = useState(null);
  const [characters, setCharacters] = useState([]);
  const [charactersSources, setCharactersSources] = useState([]);


  return (
    <div className='game'>
      
      {selectionMode && args.gm === "Amino'Guess" && (
        <CharacterSelection setSelectionMode={setSelectionMode} 
          setSelectedImage={setCharacter} setSliderValue={setSliderValue} 
          setSquares={setCharacters} setSquaresSources={setCharactersSources}
          squares={characters} squaresSources={charactersSources}
          />
      )}

      {!selectionMode && args.gm === "Amino'Guess" && (
        <Amino character={character} sliderValue={sliderValue} 
          setMode={args.setMode} setSelectionMode={setSelectionMode} 
          characters={characters} charactersSources={charactersSources}/>
      )}

      {selectionMode && args.gm === "Theseus Battle" && (
        <UserGrid setSelectionMode={setSelectionMode} setSelectedImage={setCharacter}
          setSquares={setCharacters} setSquaresSources={setCharactersSources}
          squares={characters} squaresSources={charactersSources}/>
      )}

      {!selectionMode && args.gm === "Theseus Battle" && (
        <Theseus character={character} setMode={args.setMode}/>
      )}
      
    </div>
  )
}

export default Game