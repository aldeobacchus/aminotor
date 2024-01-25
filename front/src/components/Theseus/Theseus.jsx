import React, { useEffect } from 'react'
import './theseus.css'
import axios from 'axios';
import SelectionPanel from '../SelectionPanel/SelectionPanel';

const Theseus = (args) => {
    const [isFoldDrawer, setIsFoldDrawer] = React.useState(true);
    const [listFeatures, setListFeatures] = React.useState([]);
  
    const [selectedQuestion, setSelectedQuestion] = React.useState(null);
    const [selectedImage, setSelectedImage] = React.useState(null);
  
    //turn = 0 -> player turn; turn = 1 -> theseus turn
    const [turn , setTurn] = React.useState(0);

    //trouve = 0 -> player win; trouve = 1 -> game in progress; trouve = 2 -> player lose
    const [trouve, setTrouve] = React.useState(1);
    //trouveIA = 0 -> theseus win; trouveIA = 1 -> game in progress; trouveIA = 2 -> theseus lose
    const [trouveIA, setTrouveIA] = React.useState(1);
    const [attempt, setAttempt] = React.useState(2);
    const [askStyle, setAskStyle] = React.useState("ariane__ask_disabled");
  
    const [answer, setAnswer] = React.useState("");
    const [question, setQuestion] = React.useState("");
    const [guessCharacter, setGuessCharacter] = React.useState(null);
    
    const [maskedImages, setMaskedImages] = React.useState([]);
    

    const removeNull = (value) => {
      if (value){
        value.forEach((item, index) => {
          if(item === null) {
            value.splice(index, 1);
          }
        }
      )}
      return value;
    }
  
    useEffect(() => {
      const fetchData = async () => {
        if(listFeatures.length === 0) {
          const response = await axios.get('http://127.0.0.1:5000/api/theseus/start/');
          const value = await response.data.features;
          //remove all null values
          removeNull(value);
          setListFeatures(value);
          return listFeatures;
        }
      }
      fetchData();
      
    }
    , []);
  
    const handleClickDrawer = () => {
      setIsFoldDrawer(!isFoldDrawer);
      console.log("listFeatures2 :", listFeatures);
    }
  
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

    //========= HANDLE CLICK SEND QUESTION OR GUESS IMAGE =========

    const handleClickSend = () => {
      setTurn(1);
      console.log("Masked images:", maskedImages);
      console.log("======ASKING QUESTION======");
      console.log("   selectedQuestion:", selectedQuestion);
      console.log("   selectedImage:", selectedImage);
      
      if (selectedImage === null && selectedQuestion === null){
        console.log("no image selected or question selected");
        return;
      }
      if (selectedImage && selectedQuestion){
        console.log("image and question selected");
        return;
      }
      //========= HANDLE CLICK SEND QUESTION =========
      if (selectedQuestion){
        const fetchData = async () => {
          const response = await axios.post('http://127.0.0.1:5000/api/theseus/feature/', {
            feature: selectedQuestion
          });
          console.log("response:", response);
          const data = await response.data;
          setAnswer(data.answer);
          //set next question or guess or lose if theseus has no question or guess
          if(data.fail){
            setTrouveIA(2);
          }
          if(data.character){
            setGuessCharacter(data.character);
          }
          else{
            setQuestion(data.question);
          }
          setQuestion(data.question);
          setListFeatures(removeNull(data.list_features));
        }
        fetchData();
      }

      //========= HANDLE CLICK SEND GUESS IMAGE =========
      if (selectedImage){
        console.log("image (from theseus):", selectedImage);
        const fetchData = async () => {
          const url = 'http://127.0.0.1:5000/api/theseus/guess/'+selectedImage;
          const response = await axios.get(url);
          console.log("response : ", response);
          const value = await response.data;
          console.log("value:", value);
          console.log("result:", value.result);
          if (value.result === 0){
            setTrouve(0);
            answer("Bravo vous avez trouvé !");
          } else if(value.result === 2){
            setAttempt(0);
            setTrouve(2);
            setAnswer("Perdu, 3 essais ratés");
          } else {
            setAttempt(attempt-1);
            setAnswer("Raté, il vous reste "+attempt+" essais");
          }
        }
        fetchData();
      }
    }
  
    const handleMask = () => {
      console.log("MASKING IMAGE", selectedImage);
      {/*if selected image is not in maskedimages, put it in, else remove it*/}
      if (!maskedImages.includes(selectedImage)){
        setMaskedImages([...maskedImages, selectedImage]);
      } else {
        setMaskedImages(maskedImages.filter((item) => item !== selectedImage));
      }
    }
    
  
  

    return (
      
    <div className="theseus">
    
        { trouve===1 && (
            <div className="ariane__game">
                <div className="ariane__board">
                    <SelectionPanel mode="ariane" size={24} selectedImage={selectedImage} maskedList={maskedImages} squares={args.squares} squaresSources={args.squaresSources} onImageGuess={onImageGuess} />
                    <button className="ariane__button" onClick={handleMask}>Masquer</button>
                </div>
        
            
                <div className="ariane__actions">
                    
                    {/*Tour du joueur*/}
                    {turn === 0 && (
                    <>
                        <div className="ariane__questions">
                            <div className="ariane__drawer" onClick={handleClickDrawer}>
                                <h5 className='no-margin'>question list</h5>
                            </div>
                            {!isFoldDrawer && (
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
                            )}
                        </div>
                
                        <button className={askStyle} onClick={askStyle==="ariane__ask_enabled" ? handleClickSend : ()=>{} }>Demander</button>
            
                        
                    </>
                    )}

                    {/*Tour de Thésée*/}
                    {turn === 1 && (
                    <>
                        
                        {answer && (
                            <div className="theseus__answer">
                                <p className="theseus__answer-text">{answer}</p>
                            </div>
                        )}

                        <p className="theseus__text">C'est au tour de Thésée</p>

                        {question && (
                            <div className="theseus__answer">
                                <p className="theseus__answer-text">{question}</p>
                            </div>
                        )}

                        {guessCharacter && (
                            <div className="theseus__answer">
                                <p className="theseus__answer-text">Je pense que c'est {guessCharacter}</p>
                            </div>
                        )}

                        
                    </>   
                    )}
                </div>
            </div>
        )}
    

        { trouve===0 && (
        <div className="ariane__win">
            <h2 className="ariane__win-text">Bravo vous avez trouvé !</h2>
        </div>
        )}

        { trouve===2 && (
        <div className="ariane__lose">
            <div className="ariane__lose-text">
            <h2 className="ariane__lose-text">Perdu, 3 essais ratés</h2>
            <button className="ariane__lose-button" onClick={() => args.setSelectionMode(true)}>Recommencer</button>
            <button onClick={() => args.setMode("home")}>Changer de mode de jeux</button> 
            </div>
            
            <img className="ariane__lose-img" src="img/minotors/NORMAL.png" alt="lose"/>
        </div>
        )}

    </div> 
      
    )
}


export default Theseus