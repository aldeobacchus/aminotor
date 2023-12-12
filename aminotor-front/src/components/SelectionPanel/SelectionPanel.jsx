import React from 'react';
import './SelectionPanel.css';

const SelectionPanel = ({ size }) => {

  // generate a list of 1024  random numbers between 000001 and 000200
  const squares = [];
  for (let i = 0; i < 1024; i++) {
    const random = Math.floor(Math.random() * 200) + 1;
    const padded = random.toString().padStart(6, '0');
    squares.push(padded);
  }

  // affiche uniquement les size premiers éléments de la liste squares
  const squaresToDisplay = squares.slice(0, 2**(size*2));

  return (
    <div key={size} className="selection-panel">
      {squaresToDisplay.map((squaresToDisplay) => (
        <img 
          key={squaresToDisplay} 
          src={`/img/200/${squaresToDisplay}.jpg`}
          alt={`${squaresToDisplay}`}
        />
      ))}
    </div>
  );
};

export default SelectionPanel;