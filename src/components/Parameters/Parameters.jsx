import React, { useState } from "react";
import axios from 'axios';
import './parametres.css';
function Parameters(args) {
    const [selectedImage, setSelectedImage] = useState(null);
    const [confirmationMessage, setConfirmationMessage] = useState('');

    const [loadingAdd, setLoadingAdd] = useState(false);
    const [loadingFlush, setLoadingFlush] = useState(false);

    const handleImageChange = (event) => {
        console.log('Image sélectionnée:', event.target.files[0]);
        setSelectedImage(event.target.files[0]);
    };

    const handleUpload = async () => {
        setLoadingAdd(true);
        const formData = new FormData();
        formData.append('image', selectedImage);

        try {
            const response = await axios.post('https://orchestratorservice1.azurewebsites.net/api/upload/', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            setLoadingAdd(false);
            setConfirmationMessage('L\'image a été importée avec succès.');
            console.log('Réponse du serveur:', response.data);
        } catch (error) {
            setLoadingAdd(false);
            console.error('Erreur lors de l\'envoi de l\'image:', error);
            setConfirmationMessage('Erreur lors de l\'envoi de l\'image.');
        }
    };

    const handleFlush = async () => {
        setLoadingFlush(true);
        try {
            const response = await axios.get('https://orchestratorservice1.azurewebsites.net/api/flush_upload/');
            setLoadingFlush(false);
            setConfirmationMessage('Les données ont été supprimées avec succès.');
            console.log('Réponse du serveur:', response.data);
        } catch (error) {
            setLoadingFlush(false);
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
                <div className="param-import">
                    <input type="file" id="inputfile" onChange={handleImageChange} className="input-file" />
                    {!selectedImage && (
                        <label htmlFor="inputfile" className="label-input-file">Choisir une image...</label>
                    )}
                    {selectedImage && (
                        <>
                            <label htmlFor="inputfile" className="label-input-file">{selectedImage.name}</label>
                            {!loadingAdd ? (
                                <button className="button-orange inika button-parametres white-color" onClick={handleUpload}>Importer</button>
                            ) : (
                                <span className="loader-circle"></span>
                            )}
                        </>
                    )}

                </div>
                {!loadingFlush ? (
                    <button className="button-red white-color inika button-parametres" onClick={handleFlush}>Supprimer mes données</button>
                ) : (
                    <span className="loader-circle"></span>
                )}
                {confirmationMessage && (
                    <div className="confirmation-message">{confirmationMessage}</div>
                )}
            </div>
            <button className='button-parametres inika' onClick={() => { resetConfirmationMessage(); args.handleClickParam(); }}>Retour</button>
        </div>
    )
}

export default Parameters;
