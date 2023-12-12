import React, { useState } from 'react';
import SizePanelBar from '../../components/SizePanelBar/SizePanelBar';
import SelectionPanel from '../../components/SelectionPanel/SelectionPanel';

function App() {
  

  return (
    <div>
      <SizePanelBar onSliderChange={handleSliderChange} />
      <SelectionPanel size={sliderValue} />
    </div>
  );
}

export default App;
