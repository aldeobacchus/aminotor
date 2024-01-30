import React, {useState} from 'react'
import axios from 'axios';
import SelectionPanel from '../SelectionPanel/SelectionPanel';
import './UserGrid.css';

axios.defaults.withCredentials = true;

function UserGrid(args) {
  const size = 24;
  const [selectedImage, setSelectedImage] = useState(null);

    React.useEffect(() => {
      fetchData();
    }, []);

    const fetchData = async () => {
      console.log("before fetch")
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/init/2');
        args.setSquares(response.data.list_image);
        console.log(response.data.image_urls)
        args.setSquaresSources(response.data.image_urls);

      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    return (
        <div className='game_userGrid'>
          {args.squares.length === 0 && (
            <div className="game_characterSelection-loading">
              <span class="loader2"></span>
              <h5>Chargement des images</h5>
            </div>
          )}
          {args.squares.length !== 0 && (
            <>
              <SelectionPanel mode="selection" size={size} squares={args.squares} squaresSources={args.squaresSources} onImageSelect={setSelectedImage}/>
              <div className="userGrid_buttons">
                <button onClick={() => {fetchData()}}>Nouvelle grille</button>
                {(selectedImage || args.mode === "ariane") && <button onClick={() => {args.setSelectionMode(false); args.setSelectedImage(selectedImage);}}>Start</button> }
              </div>
            </>
          )}
        </div>
    )
}

export default UserGrid