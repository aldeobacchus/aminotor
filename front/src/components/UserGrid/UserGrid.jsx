import React, {useState} from 'react'
import axios from 'axios';
import SelectionPanel from '../SelectionPanel/SelectionPanel';
import './UserGrid.css';

axios.defaults.withCredentials = true;

function UserGrid(args) {
  const [squares, setSquares] = React.useState([]);
  const size = 24;
  const [selectedImage, setSelectedImage] = useState(null);

    React.useEffect(() => {
      fetchData();
    }, []);

    const fetchData = async () => {
      const response = await axios.get('http://127.0.0.1:5000/api2/init/2');
      const value = response.data;
      const newSquares = Array(size).fill('000000').map((_, i) => {
        const padded = value[i].toString().padStart(6, '0');
        return padded;
      });
      setSquares(newSquares);
    }

    return (
        <div className='game_userGrid'>
            <SelectionPanel size={size} squares={squares} onImageSelect={setSelectedImage}/>
            <button onClick={() => {fetchData()}}>Nouvelle grille</button>
            {selectedImage && <button onClick={() => {args.setSelectionMode(false); args.setSelectedImage(selectedImage); args.setGrid(squares)}}>Start</button> }
        </div>
    )
}

export default UserGrid
            

