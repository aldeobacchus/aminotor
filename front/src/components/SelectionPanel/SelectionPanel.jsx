import React, { useEffect, useState } from 'react';
import './SelectionPanel.css';

const SelectionPanel = (args) => {
  const [selectedImage, setSelectedImage] = useState(null);

  // display only the first 'size' elements of the 'squares' list
  const squaresToDisplay = args.squares.slice(0, args.size);
  const squaresSourcesToDisplay = args.squaresSources.slice(0, args.size);

  const handleImageSelect = (image) => {
    setSelectedImage(image);
    args.onImageSelect(squaresSourcesToDisplay[squaresToDisplay.indexOf(image)]);
  };

  return (
    <div key={args.size} className="selection-panel">
      {squaresToDisplay.map((square) => (
        <img 
          className='square-img'
          key={square} 
          src={squaresSourcesToDisplay[squaresToDisplay.indexOf(square)]}
          alt={`${square}`}
          onClick={() => handleImageSelect(square)}
          style={square === selectedImage ? { boxShadow: '0 0 3px 5px #EDA828' } : {}}
        />
      ))}
    </div>
  );
};

export default SelectionPanel;