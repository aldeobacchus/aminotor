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

  const [trouve, setTrouve] = React.useState(0);
  
  useEffect(() => {
    const fetchData = async () => {
      if(listFeatures.length === 0) {
        const response = await axios.get('http://127.0.0.1:5000/api/ariane/start/');
        console.log("response : ", response)
        const value = await response.data.features;
        console.log("value:", value);

        //remove all null values
        if (value){
          value.forEach((item, index) => {
            if(item === null) {
              value.splice(index, 1);
            }
          })
        }
        console.log("value without null:", value);
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
      setSelectedImage(null);
      setSelectedQuestion(feature);
    }
  }
  const onImageGuess = (image) => {
    console.log("image:", image);
    setSelectedQuestion(null);
    setSelectedImage(image);
  }

  const handleClickSend = () => {
    console.log("======ASKING QUESTION======");
    console.log("   selectedQuestion:", selectedQuestion);
    console.log("   selectedImage:", selectedImage);
    
    if (selectedImage === null && selectedQuestion === null){
      console.log("no image selected or question selected");
      return;
    }
    if (selectedImage && selectedQuestion){
      console.log("image and question selected");
      return
    }
    if (selectedQuestion){
      const fetchData = async () => {
        const response = await axios.post('http://127.0.0.1:5000/api/ariane/feature/', {
          feature: selectedQuestion
        });
        console.log("response : ", response)
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
        if (value.result === 2){
          setTrouve(2);
        }
      }
      fetchData();
    }
  }


  


  return (
    
    <div className="ariane">
      
      <div className="ariane__game">
        <div className="ariane__grid">
          <SelectionPanel mode="ariane" size={24} squares={args.squares} squaresSources={args.squaresSources} onImageGuess={onImageGuess} />
          <button className="ariane__button">Masquer</button>
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
          <button className="ariane__button" onClick={handleClickSend}>Demander</button>
        </div>
      </div>

    </div> 

    )
}

export default Ariane