import React, { useState } from 'react';
import "./SizePanelBar.css";

const SizePanelBar = ({onSliderChange }) => {
    const [sliderValue, setSliderValue] = useState(4);

    const handleSliderChange = (event) => {
      const sliderValue = parseInt(event.target.value, 10);
      setSliderValue(sliderValue);
      onSliderChange(sliderValue);
    };

  const renderCheckpoints = () => {
    const checkpoints = [];
    for (let i = 1; i <= 5; i++) {
      checkpoints.push(
        <div    
          key={i}
          className={`checkpoint ${i <= sliderValue ? 'active' : ''}`}
          onClick={() => setSliderValue(i)}
        ></div>
      );
    }
    return checkpoints;
  };

  return (
    <div className="slider-container">
      <input
        type="range"
        min="4"
        max="7"
        value={sliderValue}
        className="slider"
        onChange={handleSliderChange}
      />
      <div className="checkpoints-container">{renderCheckpoints()}</div>
      <div className="slider-value">{2**(sliderValue)}</div>
    </div>
  );
};

export default SizePanelBar;