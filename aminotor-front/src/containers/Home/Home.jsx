import React, { useState } from 'react';
import SizePanelBar from '../../components/SizePanelBar/SizePanelBar';
import SelectionPanel from '../../components/SelectionPanel/SelectionPanel';

function App() {
  const [sliderValue, setSliderValue] = useState(2);
  const [selectedImage, setSelectedImage] = useState(null);

  const handleSliderChange = (value) => {
    setSliderValue(value);
  };

  return (
    <div>
      <SizePanelBar onSliderChange={handleSliderChange} />
      <SelectionPanel size={sliderValue}  onImageSelect={setSelectedImage}/>
      {selectedImage && <p>Selected image: {selectedImage}</p>}
    </div>
  );
}

export default App;
