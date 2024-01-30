import React, { useEffect, useState } from 'react'
import './theseus.css'
import axios from 'axios';
import SelectionPanel from '../SelectionPanel/SelectionPanel';

const Theseus = (args) => {
  const [listFeatures, setListFeatures] = useState([]);

  const [selectedQuestion, setSelectedQuestion] = useState(null);
  const [selectedImage, setSelectedImage] = useState(null);

  //turn = 0 -> player turn; turn = 1 -> theseus turn
  const [turn, setTurn] = useState(0);

  //trouve = 0 -> player win; trouve = 1 -> game in progress; trouve = 2 -> player lose
  const [trouve, setTrouve] = useState(1);
  //trouveIA = 0 -> theseus win; trouveIA = 1 -> game in progress; trouveIA = 2 -> theseus lose
  const [trouveIA, setTrouveIA] = useState(1);
  const [attempt, setAttempt] = useState(2);

  const [answer, setAnswer] = useState("");
  const [question, setQuestion] = useState("");
  const [guessCharacter, setGuessCharacter] = useState(null);

  const [maskingMode, setMaskingMode] = useState(false);
  //UI states
  const [maskedImages, setMaskedImages] = useState([]);
  const [isFocused, setIsFocused] = useState(false);
  const [askStyle, setAskStyle] = useState("ariane__ask_disabled");
  const [loadingAsk, setLoadingAsk] = useState(false);



  useEffect(() => {
    const fetchData = async () => {
      if (listFeatures.length === 0) {
        const response = await axios.get('http://127.0.0.1:5000/api/theseus/start/');
        const value = await response.data.features;
        //remove all null values
        setListFeatures(removeNull(value));
        return listFeatures;
      }
    }
    fetchData();
  }
    , []);


  const removeNull = (value) => {
    if (value) {
      console.log("value before removing null:", value);
      value = value.filter((item) => item !== null);
    }
    console.log("value after removing null:", value);
    return value;
  }


  //========= UI FUNCTION =========

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

  const handleMask = () => {
    console.log("MASKING IMAGE");
    if (!maskingMode) {
      setMaskingMode(true);
    } else {
      setMaskingMode(false);
    }
  }

  const handleClickFocus = event => {
    setIsFocused(current => !current);
  };

  //========= ARIANE FUNCTIONS, HANDLE CLICK SEND QUESTION OR GUESS IMAGE =========
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
    console.log("loading on");
    setLoadingAsk(true);
    //========= HANDLE CLICK SEND QUESTION =========
    if (selectedQuestion) {
      const fetchData = async () => {
        const response = await axios.post('http://127.0.0.1:5000/api/theseus/feature/', {
          feature: selectedQuestion
        });
        console.log("response:", response);
        const data = await response.data;
        setAnswer(data.answer);
        //set next question or guess or lose if theseus has no question or guess
        if (data.fail) {
          setTrouveIA(2);
        }
        if (data.character) {
          setGuessCharacter(data.character);
        }
        else {
          console.log("loading off");
          setLoadingAsk(false);
          setQuestion(data.question);
        }
      }
      fetchData();
    }

    //========= HANDLE CLICK SEND GUESS IMAGE =========
    if (selectedImage) {
      console.log("image (from theseus):", selectedImage);

      const fetchData = async () => {
        const url = 'http://127.0.0.1:5000/api/theseus/guess/' + selectedImage;
        const response = await axios.get(url);

        console.log("response : ", response);
        const data = await response.data;
        console.log("data:", data);

        if (data.answer === 0) {
          setTrouve(0);
          setAnswer("Bravo vous avez trouvé !");
        } else if (data.answer === 2) {
          setAttempt(0);
          setTrouve(2);
          setAnswer("Perdu, 3 essais ratés");
        } else {
          setAttempt(attempt - 1);
          setAnswer("Raté, il vous reste " + attempt + " essais");
          if (data.fail) {
            setTrouveIA(2);
          }
          if (data.character) {
            setGuessCharacter(data.character);
          }
          else {
            console.log("loading off");
            setLoadingAsk(false);
            setQuestion(data.question);
          }
        }
      }
      fetchData();
    }


    setTurn(1);

  }

  //========= THESEUS FUNCTIONS, HANDLE CLICK SEND ANSWER =========
  const handleAnswer = (arg) => {
    setLoadingAsk(true);
    console.log("answering question with : ", arg);
    const fetchData = async () => {
      const response = await axios.get('http://127.0.0.1:5000/api/theseus/answer/' + arg);
      console.log("response:", response);
      const data = await response.data;
      console.log("list features:", data.list_features);
      setListFeatures(removeNull(data.list_features));
      setQuestion(null);
      setTurn(0);
      setLoadingAsk(false);
    }
    fetchData();
  }






  return (

    <div className="theseus">

      {trouve === 1 && trouveIA === 1 && (
        <div className="ariane__game">
          <div className="ariane__board">
            <SelectionPanel mode="ariane" maskingMode={maskingMode} setMaskedImages={setMaskedImages} maskedImages={maskedImages} size={24} selectedImage={selectedImage} squares={args.squares} squaresSources={args.squaresSources} onImageGuess={onImageGuess} />
            <button className="ariane__button" onClick={handleMask}>{maskingMode ? "Mode normal" : "mode masque"}</button>
          </div>


          <div className="ariane__actions">

            {/*Tour du joueur*/}
            {turn === 0 && (
              <>
                {listFeatures.length !== 0 && (
                  <div className="ariane__questions">
                    <div className="ariane__drawer">
                      <h5 className='no-margin'>liste des question</h5>
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
                )}
                {listFeatures.length === 0 && (
                  <div className="ariane__loading">
                    <div className="ariane__questions">
                      <h5 className="ariane__loading-text">Chargement des questions</h5>
                    </div>
                    <span class="loader"></span>
                  </div>
                )}

                <button className={askStyle} onClick={askStyle === "ariane__ask_enabled" ? handleClickSend : () => { }}>Demander</button>

              </>
            )}

            {/*Tour de Thésée*/}
            {turn === 1 && (
              <>

                {answer && !guessCharacter && !loadingAsk && (
                  <div className="theseus__answer">
                    <p className="theseus__answer-text">{answer}</p>
                  </div>
                )}

                {question && !loadingAsk && (
                  <div className="theseus__questions">
                    <p className="theseus__answer-text">{question}</p>
                    <div className='theseus__question-wrapper'>
                      <button className='ariane__button button-blue' onClick={() => handleAnswer(1)}>Oui</button>
                      <button className='ariane__button button-orange' onClick={() => handleAnswer(0)}>Non</button>
                    </div>
                    <button className='ariane__button theseus__button-idk' onClick={() => handleAnswer(2)}>Je ne sais pas</button>
                  </div>
                )}

                {question && !loadingAsk && (
                  <img className={isFocused ? "characterFocus" : "theseus__mycharacter"} onClick={handleClickFocus} src={args.character} alt="Selected" />
                )}

                {loadingAsk && (
                  <span class="loader-circle"></span>
                )}

                {guessCharacter && (
                  <div className="theseus__guess">
                    <p className="theseus__guess-text">Je pense que c'est cette personne :</p>
                    <img className="theseus__guess-img" src={"https://etud.insa-toulouse.fr/~alami-mejjat/" + guessCharacter.toString().padStart(6, '0')} alt="guess" />
                    <div className="theseus__guess-buttons">
                      <button className='ariane__button' onClick={() => setTrouveIA(0)}>Oui</button>
                      <button className='ariane__button' onClick={() => setTurn(0)}>Non</button>
                    </div>
                  </div>
                )}


              </>
            )}


          </div>
        </div>
      )}


      {trouve === 0 && (
        <div className="ariane__lose">
          <div className="ariane__lose-text">
            <h2 className="ariane__lose-text">Bravo vous avez trouvé !</h2>
            <img className="theseus__guess-img" src={"https://etud.insa-toulouse.fr/~alami-mejjat/" + selectedImage.toString().padStart(6, '0')} />
            <button className="ariane__lose-button" onClick={() => args.setSelectionMode(true)}>Recommencer</button>
            <button onClick={() => args.setMode("home")}>Changer de mode de jeux</button>
          </div>

          <img className="ariane__lose-img" src="img/minotors/LAMP.png" alt="win" />
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

      {trouveIA === 0 && (
        <div className="ariane__lose">
          <div className="ariane__lose-text">
            <h2 className="ariane__lose-text">Thésée a trouvé !</h2>
            <img className="theseus__guess-img" src={"https://etud.insa-toulouse.fr/~alami-mejjat/" + guessCharacter.toString().padStart(6, '0')} alt="guess" />
            <button className="ariane__lose-button" onClick={() => args.setSelectionMode(true)}>Recommencer</button>
            <button onClick={() => args.setMode("home")}>Changer de mode de jeux</button>
          </div>

          <img className="ariane__lose-img" src="img/minotors/NORMAL.png" alt="lose" />
        </div>
      )

      }

    </div>

  )
}


export default Theseus