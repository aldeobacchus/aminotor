import React from 'react'
import SizePanelBar from '../../components/SizePanelBar/SizePanelBar';
import SelectionPanel from '../../components/SelectionPanel/SelectionPanel';
import { useState } from 'react';

function Game(args) {
  const [sliderValue, setSliderValue] = useState(2);

  const handleSliderChange = (value) => {
    setSliderValue(value);
  };

  return (
    <div className='game'>
      
      {args.gm === 'Amino' && (
        <div className="game_amino">
          
          <h1>Amino's Guess</h1>  
        
          <SizePanelBar onSliderChange={handleSliderChange} />
          <SelectionPanel size={sliderValue} />
        </div>
        
      )}

      {args.gm === 'Thesus' && (
        <div className="game_thesus">
          
        <h1>Amino's Guess</h1>  
      
        <SizePanelBar onSliderChange={handleSliderChange} />
        <SelectionPanel size={sliderValue} />
      </div> 
      )}
      
    </div>
  )
}

export default Game