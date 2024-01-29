import React, { useEffect, useState } from 'react';
import './SelectionPanel.css';

{/*args : mode : {selection,ariane}*/ }
const SelectionPanel = (args) => {
  const [selectedImage, setSelectedImage] = useState(null);

  // display only the first 'size' elements of the 'squares' list
  const squaresToDisplay = args.squares.slice(0, args.size);
  const squaresSourcesToDisplay = args.squaresSources.slice(0, args.size);

  const handleImageSelect = (image) => {
    setSelectedImage(image);
    args.onImageSelect(squaresSourcesToDisplay[squaresToDisplay.indexOf(image)]);
  };

  const handleImageGuess = (image) => {
    if (args.maskingMode) {
      args.setMaskedImages([...args.maskedImages, image]);
      if (!args.maskedImages.includes(image)) {
        args.setMaskedImages([...args.maskedImages, image]);
      } else {
        args.setMaskedImages(args.maskedImages.filter((item) => item !== image));
      }
    } else {
      setSelectedImage(image);
      args.onImageGuess(image);
    }
  };

  const handleStyle = (square) => {
    let styles = {};
    if (square === selectedImage) {
      styles = { boxShadow: '0 0 3px 5px #EDA828' };
    }
    if (args.maskedImages?.includes(square)) {
      styles = { opacity: 0.5 };
    }
    if (args.maskedImages?.includes(square) && square === selectedImage) {
      styles = { opacity: 0.5, boxShadow: '0 0 3px 5px #EDA828' };
    }

    return styles;
  }


  return (
    <div key={args.size} className="selection-panel">
      {squaresToDisplay.map((square) => (
        <img
          className={args.maskingMode ? 'square-img purple-hover' : 'square-img'}
          key={square}
          src={squaresSourcesToDisplay[squaresToDisplay.indexOf(square)]}
          alt={`${square}`}
          onClick={args.mode === "ariane" ? () => handleImageGuess(square) : () => handleImageSelect(square)}

          style={handleStyle(square)}
        />
      ))}
    </div>
  );
};

export default SelectionPanel;