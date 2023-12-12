import React, { useState } from 'react';
import SizePanelBar from '../../components/SizePanelBar/SizePanelBar';
import SelectionPanel from '../../components/SelectionPanel/SelectionPanel';

function App() {
  const [sliderValue, setSliderValue] = useState(2);

  const handleSliderChange = (value) => {
    setSliderValue(value);
  };

  return (
    <div>
      <SizePanelBar onSliderChange={handleSliderChange} />
      <SelectionPanel size={sliderValue} />
    </div>
  );
}

export default App;
