import React, { useState } from 'react';
import './SelectionPanel.css';

const SelectionPanel = ({ size, squares, onImageSelect}) => {
  const [selectedImage, setSelectedImage] = useState(null);

  // display only the first 'size' elements of the 'squares' list
  const squaresToDisplay = squares.slice(0, 2**(size*2));

  const handleImageSelect = (image) => {
    setSelectedImage(image);
    onImageSelect(image);
  };

  return (
    <div key={size} className="selection-panel">
      {squaresToDisplay.map((square) => (
        <img 
          className='square-img'
          key={square} 
          src={`https://etud.insa-toulouse.fr/~alami-mejjat/${square}.jpg`}
          alt={`${square}`}
          onClick={() => handleImageSelect(square)}
          style={square === selectedImage ? { boxShadow: '0 0 3px 5px #EDA828' } : {}}
        />
      ))}
    </div>
  );
};

export default SelectionPanel;