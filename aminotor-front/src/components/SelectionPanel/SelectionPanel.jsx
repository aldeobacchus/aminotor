import React from 'react';
import './SelectionPanel.css';

const SelectionPanel = ({ size, onImageSelect }) => {
  const [selectedImage, setSelectedImage] = React.useState(null);

  // generate a list of 1024  random numbers between 000001 and 000200
  const squares = [];
  for (let i = 0; i < 1024; i++) {
    const random = Math.floor(Math.random() * 200) + 1;
    const padded = random.toString().padStart(6, '0');
    squares.push(padded);
  }

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
          key={square} 
          src={`/img/200/${square}.jpg`}
          alt={`${square}`}
          onClick={() => handleImageSelect(square)}
          style={square === selectedImage ? { boxShadow: '0 0 10px 5px red' } : {}}
        />
      ))}
    </div>
  );
};

export default SelectionPanel;