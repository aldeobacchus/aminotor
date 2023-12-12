import React from 'react'
import SizePanelBar from '../../components/SizePanelBar/SizePanelBar';
import SelectionPanel from '../../components/SelectionPanel/SelectionPanel';
import { useState } from 'react';
import Amino from '../../components/Amino/Amino';
import Theseus from '../../components/Theseus/Theseus';

function Game(args) {
  const [sliderValue, setSliderValue] = useState(2);
  const [selectedImage, setSelectedImage] = useState(null);
  const [squares, setSquares] = useState([]);

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
    <div className='game'>
      
      {args.gm === 'Amino' && (
        <div className="game_amino">
          
          <h1>Amino's Guess</h1>  
        
          <SizePanelBar onSliderChange={handleSliderChange} />
          <SelectionPanel size={sliderValue} squares={squares} onImageSelect={setSelectedImage}/>
          <br/>
          {selectedImage && <img src={`/img/200/${selectedImage}.jpg`} alt="Selected" />}     
        </div>
        
      )}

      {args.gm === 'Thesus' && (
        <div className="game_thesus">
          
        <h1>Amino's Guess</h1>  
      
        <SizePanelBar onSliderChange={handleSliderChange} />
        <SelectionPanel size={sliderValue} squares={squares} onImageSelect={setSelectedImage}/>
        <br/>
        {selectedImage && <img src={`/img/200/${selectedImage}.jpg`} alt="Selected" />}  
      </div> 
      )}
      
    </div>
  )
}

export default Game