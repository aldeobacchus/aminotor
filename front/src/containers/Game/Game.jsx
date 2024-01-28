import React, {useState} from 'react'
import Amino from '../../components/Amino/Amino';
import Ariane from '../../components/Ariane/Ariane';
import CharacterSelection from '../../components/CharacterSelection/CharacterSelection';
import './game.css'
import UserGrid from '../../components/UserGrid/UserGrid';
import Theseus from '../../components/Theseus/Theseus';

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

      {selectionMode && args.gm === "Ariane" && (
        <UserGrid mode="ariane" setSelectionMode={setSelectionMode} setSelectedImage={setCharacter}
          setSquares={setCharacters} setSquaresSources={setCharactersSources}
          squares={characters} squaresSources={charactersSources}/>
      )}

      {!selectionMode && args.gm === "Ariane" && (
        <Ariane character={character} squares={characters} setSelectionMode={setSelectionMode} squaresSources={charactersSources} setMode={args.setMode}/>
      )}
      

      {selectionMode && args.gm === "Theseus Battle" && (
        <UserGrid mode="theseus" setSelectionMode={setSelectionMode} setSelectedImage={setCharacter}
          setSquares={setCharacters} setSquaresSources={setCharactersSources}
          squares={characters} squaresSources={charactersSources}/>
      )}

      {!selectionMode && args.gm === "Theseus Battle" && (
        <Theseus character={character} squares={characters} setSelectionMode={setSelectionMode} squaresSources={charactersSources} setMode={args.setMode}/>
      )}
    </div>
  )
}

export default Game