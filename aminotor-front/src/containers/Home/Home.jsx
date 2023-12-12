import React, { useState } from 'react';
import SizePanelBar from '../../components/SizePanelBar/SizePanelBar';
import SelectionPanel from '../../components/SelectionPanel/SelectionPanel';

function Home() {
  

  return (
    <div>
      <SizePanelBar onSliderChange={handleSliderChange} />
      <SelectionPanel size={sliderValue}  onImageSelect={setSelectedImage}/>
      {selectedImage && <p>Selected image: {selectedImage}</p>}
    </div>
  );
}

export default Home;
