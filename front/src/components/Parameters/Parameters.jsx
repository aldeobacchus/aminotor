import React, {useState} from "react";
import axios from 'axios';

function Parameters(args) {

    const [selectedImage, setSelectedImage] = useState(null);

    const handleImageChange = (event) => {
      setSelectedImage(event.target.files[0]);
    };

    const handleUpload = async () => {
        const formData = new FormData();
        formData.append('image', selectedImage);
    
        try {
          const response = await axios.post('http://127.0.0.1:5000/api/upload/', formData, {
            headers: {
              'Content-Type': 'multipart/form-data',
            },
          });
          console.log('Réponse du serveur:', response.data);
        } catch (error) {
          console.error('Erreur lors de l\'envoi de l\'image:', error);
        }
      };

    const handleFlush = async () => {
        try {
            const response = await axios.get('http://127.0.0.1:5000/api/flush_upload/');
            console.log('Réponse du serveur:', response.data);
        } catch (error) {
            console.error('Erreur lors de la suppression des données:', error);
        }
    };
            


    return (        
        <div className="param-menu">
            <h2>Paramètres</h2>
            <div className="param-buttons">
                <input type="file" onChange={handleImageChange}/>
                <button className="button-orange white-color inika small-text" onClick={handleUpload}>Importer une image</button>
                <button className="button-red white-color inika small-text" onClick={handleFlush}>Supprimer les données</button>
            </div>
            <button className='button-parametres inika' onClick={args.handleClickParam}>Retour</button>
        </div>
    )
}

export default Parameters;