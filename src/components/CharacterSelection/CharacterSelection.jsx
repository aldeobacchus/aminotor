import React, { useState } from 'react'
import SizePanelBar from '../SizePanelBar/SizePanelBar';
import SelectionPanel from '../SelectionPanel/SelectionPanel';
import './characterSelection.css';
import axios from 'axios';

// Set withCredentials to true globally
axios.defaults.withCredentials = true;

function CharacterSelection(args) {
    const [sliderValue, setSliderValue] = useState(4);
    const [selectedImage, setSelectedImage] = useState(null);
  
    const handleSliderChange = (value) => {
      setSliderValue(value);
    };

    React.useEffect(() => {
      fetchData();
    }, []);

    const fetchData = async () => {
      console.log("before fetch")
      try {
        const response = await axios.get('https://orchestratorservice1.azurewebsites.net/api/init/1');
        args.setSquares(response.data.list_image);
        console.log(response.data.image_urls)
        console.log(response.data.image_urls.length);
        args.setSquaresSources(response.data.image_urls);

      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };
  
  return (
    <div className='game_characterSelection'>
      {/**image list is empty*/}
    {args.squares.length !== 0 ? (
        <>
        <SizePanelBar onSliderChange={handleSliderChange} />
        <SelectionPanel mode="selection" size={2**(sliderValue)} squares={args.squares} squaresSources={args.squaresSources} onImageSelect={setSelectedImage}/>
        {selectedImage && <button onClick={() => {args.setSelectionMode(false); args.setSelectedImage(selectedImage); args.setSliderValue(sliderValue)}}>Start</button> }
        </>
      ) : (
        <div className='game_characterSelection-loading'>
          <span class="loader2"></span>
          <h5>Chargement des images</h5>
        </div>
      )}
    </div>
  )
}

export default CharacterSelection