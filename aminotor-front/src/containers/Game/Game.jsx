import React from 'react'
import SizePanelBar from '../../components/SizePanelBar/SizePanelBar';
import SelectionPanel from '../../components/SelectionPanel/SelectionPanel';
import { useState } from 'react';
import Amino from '../../components/Amino/Amino';
import Theseus from '../../components/Theseus/Theseus';

function Game(args) {
  const [sliderValue, setSliderValue] = useState(2);

  const handleSliderChange = (value) => {
    setSliderValue(value);
  };

  return (
    <div className='game'>
      
      {args.gm === 'Amino' && (
        <Amino sliderValue={sliderValue} handleSliderChange={handleSliderChange} />
        
      )}

      {args.gm === 'Thesus' && (
        <Theseus sliderValue={sliderValue} handleSliderChange={handleSliderChange} />
      )}
      
    </div>
  )
}

export default Game