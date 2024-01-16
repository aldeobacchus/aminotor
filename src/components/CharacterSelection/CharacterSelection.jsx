import React, { useState } from 'react'
import SizePanelBar from '../SizePanelBar/SizePanelBar';
import SelectionPanel from '../SelectionPanel/SelectionPanel';
import './characterSelection.css';
import axios from 'axios';

// Set withCredentials to true globally
axios.defaults.withCredentials = true;

function CharacterSelection(args) {
    const [squares, setSquares] = useState([]);
    const [sliderValue, setSliderValue] = useState(2);
    const [selectedImage, setSelectedImage] = useState(null);
  
    const handleSliderChange = (value) => {
      setSliderValue(value);
    };

    React.useEffect(() => {
      const fetchData = async () => {
        const response = await axios.get('http://127.0.0.1:5000/api/init/1');
        const value = response.data;
        const newSquares = Array(1024).fill('000000').map((_, i) => {
          const padded = value[i].toString().padStart(6, '0');
          return padded;
        });
        setSquares(newSquares);
      };
      fetchData();
      }, []);
  
  return (
    <div className='game_characterSelection'>
        <SizePanelBar onSliderChange={handleSliderChange} />
        <SelectionPanel size={2**(sliderValue*2)} squares={squares} onImageSelect={setSelectedImage}/>
        {selectedImage && <button onClick={() => {args.setSelectionMode(false); args.setSelectedImage(selectedImage); args.setSliderValue(sliderValue)}}>Start</button> }
    </div>
  )
}

export default CharacterSelection