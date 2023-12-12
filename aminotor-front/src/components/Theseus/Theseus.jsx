import React from 'react'
import SizePanelBar from '../SizePanelBar/SizePanelBar';
import SelectionPanel from '../SelectionPanel/SelectionPanel';

function Theseus(args) {
  return (
    
    <div className="game_thesus">
          
      <h1>Theseus</h1>

      <SizePanelBar onSliderChange={args.handleSliderChange} />
      <SelectionPanel size={args.sliderValue} />
    </div> 

    )
}

export default Theseus