import React, { useState } from 'react'
import SizePanelBar from '../SizePanelBar/SizePanelBar';
import SelectionPanel from '../SelectionPanel/SelectionPanel';
import './characterSelection.css';
import axios from 'axios';

// Set withCredentials to true globally
axios.defaults.withCredentials = true;

function CharacterSelection(args) {
    const [sliderValue, setSliderValue] = useState(2);
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
        const response = await axios.get('http://127.0.0.1:5000/api/init/1');
        args.setSquares(response.data.list_image);
        console.log(response.data.image_urls)
        args.setSquaresSources(response.data.image_urls);
        
        /*const uploadValue = response.data.list_upload;
        let imageUrls = [];
        console.log("before upload value")
        if (uploadValue.length !== 0) {
          // Load images in parallel
          const imagePromises = uploadValue.map((imageName) => {
            return fetch(`http://localhost:5000/api/get_img/${imageName}`)
              .then(response => response.blob())
              .then(blob => URL.createObjectURL(blob))
              .catch(error => {
                console.error(`Error loading image ${imageName}:`, error);
                return null; // Return null for failed requests
              });
          });
  
          const resolvedImages = await Promise.allSettled(imagePromises);
  
          // Filter out successful responses
          imageUrls = resolvedImages
            .filter(result => result.status === 'fulfilled')
            .map(result => result.value);
        }
        console.log("after upload value");
        const listImage = response.data.list_image;

        const newSquares = listImage.map((_, i) => {
          const padded = `https://etud.insa-toulouse.fr/~alami-mejjat/${listImage[i].toString().padStart(6, '0')}.jpg`;
          return padded;
        }); 

        console.log("after list image")
        // Combine the arrays and set the state
        args.setSquares([...uploadValue,...listImage]);
        args.setSquaresSources([...imageUrls,...newSquares]);
        console.log("end of fetch")*/

      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };
  
  return (
    <div className='game_characterSelection'>
        <SizePanelBar onSliderChange={handleSliderChange} />
        <SelectionPanel mode="selection" size={2**(sliderValue*2)} squares={args.squares} squaresSources={args.squaresSources} onImageSelect={setSelectedImage}/>
        {selectedImage && <button onClick={() => {args.setSelectionMode(false); args.setSelectedImage(selectedImage); args.setSliderValue(sliderValue)}}>Start</button> }
    </div>
  )
}

export default CharacterSelection