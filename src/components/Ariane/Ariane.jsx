import React, { useEffect } from 'react'
import './Ariane.css'
import ArrowRightIcon from '@mui/icons-material/ArrowRight';
import ArrowDropDownIcon from '@mui/icons-material/ArrowDropDown';
import axios from 'axios';
import UserGrid from '../UserGrid/UserGrid';
import SelectionPanel from '../SelectionPanel/SelectionPanel';

function Ariane(args) {

  const [isFoldDrawer, setIsFoldDrawer] = React.useState(true);
  const [listFeatures, setListFeatures] = React.useState([]);

  const [selectedQuestion, setSelectedQuestion] = React.useState(null);
  const [selectedImage, setSelectedImage] = React.useState(null);

  const [trouve, setTrouve] = React.useState(1);
  const [attempt, setAttempt] = React.useState(2);
  const [askStyle, setAskStyle] = React.useState("ariane__ask_disabled");

  const [answer, setAnswer] = React.useState("");
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
        const response = await axios.get('http://127.0.0.1:5000/api/ariane/start/');
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

  const handleClickSend = () => {
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
    if (selectedQuestion){
      const fetchData = async () => {
        const response = await axios.post('http://127.0.0.1:5000/api/ariane/feature/', {
          feature: selectedQuestion
        });
        const data = await response.data;
        setAnswer(data.answer);
        setListFeatures(removeNull(data.list_features));
      }
      fetchData();
    }
    if (selectedImage){
      console.log("image (from ariane):", selectedImage);
      const fetchData = async () => {
        const url = 'http://127.0.0.1:5000/api/ariane/guess/'+selectedImage;
        const response = await axios.get(url);
        console.log("response : ", response);
        const value = await response.data;
        console.log("value:", value);
        if (value.result === "0"){
          setTrouve(0);
          answer("Bravo vous avez trouvé !");
        } else if(value.result === "2"){
          setAttempt(0);
          setAnswer("Perdu, 3 essais ratés")
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
    
    <div className="ariane">
      
      <div className="ariane__game">
        <div className="ariane__board">
          <SelectionPanel mode="ariane" size={24} selectedImage={selectedImage} maskedList={maskedImages} squares={args.squares} squaresSources={args.squaresSources} onImageGuess={onImageGuess} />
          <button className="ariane__button" onClick={handleMask}>Masquer</button>
        </div>
        <div className="ariane__actions">
          <div className="ariane__questions">
            <div className="ariane__drawer" onClick={handleClickDrawer}>
              {isFoldDrawer ? <ArrowRightIcon className='ariane__arrow' /> : <ArrowDropDownIcon className='ariane__arrow' />}
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
        
          {answer && (
            <div className="ariane__answer">
              <p className="ariane__answer-text">{answer}</p>
            </div>
          )}
        </div>
      </div>

    </div> 

    )
}

export default Ariane