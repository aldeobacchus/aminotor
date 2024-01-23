import React, { useState } from "react";
import axios from 'axios';

function Parameters(args) {
    const [selectedImage, setSelectedImage] = useState(null);
    const [confirmationMessage, setConfirmationMessage] = useState('');

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
            setConfirmationMessage('L\'image a été importée avec succès.');
            console.log('Réponse du serveur:', response.data);
        } catch (error) {
            console.error('Erreur lors de l\'envoi de l\'image:', error);
            setConfirmationMessage('Erreur lors de l\'envoi de l\'image.');
        }
    };

    const handleFlush = async () => {
        try {
            const response = await axios.get('http://127.0.0.1:5000/api/flush_upload/');
            setConfirmationMessage('Les données ont été supprimées avec succès.');
            console.log('Réponse du serveur:', response.data);
        } catch (error) {
            console.error('Erreur lors de la suppression des données:', error);
            setConfirmationMessage('Erreur lors de la suppression des données.');
        }
    };

    const resetConfirmationMessage = () => {
        setConfirmationMessage('');
    };

    return (
        <div className="param-menu">
            <h2>Paramètres</h2>
            <div className="param-buttons">
                <input type="file" onChange={handleImageChange} />
                <button className="button-orange white-color inika small-text" onClick={handleUpload}>Importer une image</button>
                <button className="button-red white-color inika small-text" onClick={handleFlush}>Supprimer les données</button>
                {confirmationMessage && (
                    <div className="confirmation-message">{confirmationMessage}</div>
                )}
            </div>
            <button className='button-parametres inika' onClick={() => { resetConfirmationMessage(); args.handleClickParam(); }}>Retour</button>
        </div>
    )
}

export default Parameters;
