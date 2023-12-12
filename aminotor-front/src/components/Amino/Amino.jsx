import React from 'react'
import SizePanelBar from '../SizePanelBar/SizePanelBar';
import SelectionPanel from '../SelectionPanel/SelectionPanel';

function Amino(args) {
  return (
    <div className="game_amino">
          
    <h1>Amino's Guess</h1>  
  
    <SizePanelBar onSliderChange={args.handleSliderChange} />
    <SelectionPanel size={args.sliderValue} />
  </div>
  )
}

export default Amino