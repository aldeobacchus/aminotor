import React from 'react'
import SizePanelBar from '../SizePanelBar/SizePanelBar';
import SelectionPanel from '../SelectionPanel/SelectionPanel';
import { useState } from 'react';

function CharacterSelection(args) {
    const [squares, setSquares] = useState([]);
    const [sliderValue, setSliderValue] = useState(2);
    const [selectedImage, setSelectedImage] = useState(null);
  
    const handleSliderChange = (value) => {
      setSliderValue(value);
    };

    React.useEffect(() => {
        const newSquares = [];
        for (let i = 0; i < 1024; i++) {
          const random = Math.floor(Math.random() * 200) + 1;
          const padded = random.toString().padStart(6, '0');
          newSquares.push(padded);
        }
        setSquares(newSquares);
      }, []);

  return (
    <div className='game_characterSelection'>
        <SizePanelBar onSliderChange={handleSliderChange} />
        <SelectionPanel size={sliderValue} squares={squares} onImageSelect={setSelectedImage}/>
        {selectedImage && <button onClick={() => {args.setSelectionMode(false); args.setSelectedImage(selectedImage)}}>Start</button> }
    </div>
  )
}

export default CharacterSelection