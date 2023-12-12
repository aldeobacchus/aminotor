import React, { useState } from 'react';  
import SizePanelBar from '../../components/SizePanelBar/SizePanelBar';
import SelectionPanel from '../../components/SelectionPanel/SelectionPanel';

function Test() {
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
    <div>
      <SizePanelBar onSliderChange={handleSliderChange} />
      <SelectionPanel size={sliderValue} squares={squares} onImageSelect={setSelectedImage}/>
      {selectedImage && <img src={`/img/200/${selectedImage}.jpg`} alt="Selected" />}
    </div>
  );
    <div>Test</div>
    
  )
}

export default Test