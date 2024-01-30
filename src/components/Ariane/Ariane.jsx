import React, { useEffect, useState } from 'react'
import './Ariane.css'
import axios from 'axios';
import SelectionPanel from '../SelectionPanel/SelectionPanel';

function Ariane(args) {

  const [listFeatures, setListFeatures] = useState([]);

  const [selectedQuestion, setSelectedQuestion] = useState(null);
  const [selectedImage, setSelectedImage] = useState(null);

  const [trouve, setTrouve] = useState(1);
  const [attempt, setAttempt] = useState(2);
  const [askStyle, setAskStyle] = useState("ariane__ask_disabled");

  const [answer, setAnswer] = useState("");
  const [maskedImages, setMaskedImages] = useState([]);

  const [loadingAsk, setLoadingAsk] = useState(false);
  const [maskingMode, setMaskingMode] = useState(false);


  useEffect(() => {
    const fetchData = async () => {
      if (listFeatures.length === 0) {
        const response = await axios.get('https://orchestratorservice1.azurewebsites.net/api/ariane/start/');
        const value = await response.data.features;
        //remove all null values
        setListFeatures(removeNull(value));
        return listFeatures;
      }
    }
    fetchData();

  }, []);


  const handleClickQuestion = (feature) => {
    return () => {
      console.log("feature:", feature);
      setAskStyle("ariane__ask_enabled");
      setSelectedImage(null);
      setSelectedQuestion(feature);
    }
  }
  const onImageGuess = (image) => {
    console.log("image:", image);
    setAskStyle("ariane__ask_enabled");
    setSelectedQuestion(null);
    setSelectedImage(image);
  }

  const removeNull = (value) => {
    if (value) {
      console.log("value before removing null:", value);
      value = value.filter((item) => item !== null);
    }
    console.log("value after removing null:", value);
    return value;
  }

  const handleClickSend = () => {
    console.log("Masked images:", maskedImages);
    console.log("======ASKING QUESTION======");
    console.log("   selectedQuestion:", selectedQuestion);
    console.log("   selectedImage:", selectedImage);

    if (selectedImage === null && selectedQuestion === null) {
      console.log("no image selected or question selected");
      return;
    }
    if (selectedImage && selectedQuestion) {
      console.log("image and question selected");
      return;
    }
    setLoadingAsk(true);
    if (selectedQuestion) {
      const fetchData = async () => {
        const response = await axios.post('https://orchestratorservice1.azurewebsites.net/api/ariane/feature/', {
          feature: selectedQuestion
        });
        console.log("response:", response);
        const data = await response.data;
        setAnswer(data.answer);
        setListFeatures(removeNull(data.list_features));
        setLoadingAsk(false);
      }
      fetchData();
    }
    if (selectedImage) {
      console.log("image (from ariane):", selectedImage);
      const fetchData = async () => {
        const url = 'https://orchestratorservice1.azurewebsites.net/api/ariane/guess/' + selectedImage;
        const response = await axios.get(url);
        console.log("response : ", response);
        const value = await response.data;
        console.log("value:", value);
        console.log("result:", value.result);
        if (value.result === 0) {
          setTrouve(0);
          answer("Bravo vous avez trouvé !");
        } else if (value.result === 2) {
          setAttempt(0);
          setTrouve(2);
          setAnswer("Perdu, 3 essais ratés");
        } else {
          setLoadingAsk(false);
          setAttempt(attempt - 1);
          setAnswer("Raté, il vous reste " + attempt + " essais");
        }
      }
      fetchData();
    }
  }

  const handleMask = () => {
    console.log("MASKING IMAGE");
    if (!maskingMode) {
      setMaskingMode(true);
    } else {
      setMaskingMode(false);
    }
  }



  return (

    <div className="ariane">

      {trouve === 1 && (<div className="ariane__game">
        <div className="ariane__board">
          <SelectionPanel mode="ariane" size={24} maskingMode={maskingMode} setMaskedImages={setMaskedImages} maskedImages={maskedImages} selectedImage={selectedImage} squares={args.squares} squaresSources={args.squaresSources} onImageGuess={onImageGuess} />
          <button className="ariane__button" onClick={handleMask}>{maskingMode ? "Mode normal" : "mode masque"}</button>
        </div>

        <div className="ariane__actions">
          {!loadingAsk && (
            <>
              {
                listFeatures.length === 0 && (
                  <div className="ariane__loading">
                    <div className="ariane__questions">
                      <h5 className="ariane__loading-text">Chargement des questions</h5>
                    </div>
                    <span class="loader"></span>
                  </div>
                )
              }

              {listFeatures.length !== 0 && (
                <>
                  <div className="ariane__questions">
                    <div className="ariane__drawer">
                      <h5 className='no-margin'>question list</h5>
                    </div>
                    <div className="ariane__list-questions">
                      {listFeatures.map((feature) => (
                        <p
                          className="ariane__question-text"
                          key={feature}
                          onClick={handleClickQuestion(feature)}
                          style={feature === selectedQuestion ? { backgroundColor: '#EDA828' } : {}}>
                          {feature}</p>
                      ))}
                    </div>

                  </div>

                  <button className={askStyle} onClick={askStyle === "ariane__ask_enabled" ? handleClickSend : () => { }}>Demander</button>

                </>
              )}

              {answer && (
                <div className="ariane__answer">
                  <p className="ariane__answer-text">{answer}</p>
                </div>
              )}
            </>
          )}
          {loadingAsk && (
            <span class="loader-circle"></span>
          )}
        </div>


      </div>

      )}

      {trouve === 0 && (
        <div className="ariane__win">
          <h2 className="ariane__win-text">Bravo vous avez trouvé !</h2>
        </div>
      )}

      {trouve === 2 && (
        <div className="ariane__lose">
          <div className="ariane__lose-text">
            <h2 className="ariane__lose-text">Perdu, 3 essais ratés</h2>
            <button className="ariane__lose-button" onClick={() => args.setSelectionMode(true)}>Recommencer</button>
            <button onClick={() => args.setMode("home")}>Changer de mode de jeux</button>
          </div>

          <img className="ariane__lose-img" src="img/minotors/NORMAL.png" alt="lose" />
        </div>
      )}
    </div>

  )
}

export default Ariane