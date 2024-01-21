import React, { useEffect } from 'react'
import './Theseus.css'
import ArrowRightIcon from '@mui/icons-material/ArrowRight';
import ArrowDropDownIcon from '@mui/icons-material/ArrowDropDown';
import axios from 'axios';
import UserGrid from '../UserGrid/UserGrid';
import SelectionPanel from '../SelectionPanel/SelectionPanel';

function Theseus(args) {

  const [squaresToDisplay, setSquaresToDisplay] = React.useState(args.grid);
  const [isFoldDrawer, setIsFoldDrawer] = React.useState(true);
  const [listFeatures, setListFeatures] = React.useState([]);
  const [selectedQuestion, setSelectedQuestion] = React.useState(null);
  console.log("args in Theseus:", args);
  
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
      setSelectedQuestion(feature);
    }
  }

  const handleClickSend = () => {
    console.log("selectedQuestion:", selectedQuestion);
    const fetchData = async () => {
      const response = await axios.post('http://127.0.0.1:5000/api/ariane/feature/', {
        feature: selectedQuestion
      });
      console.log("response : ", response)
    }
    fetchData();
  }



  return (
    
    <div className="theseus">
      
      <div className="theseus__game">
        <SelectionPanel size={24} squares={args.squares} squaresSources={args.squaresSources}/>
        <div className="theseus__actions">
          <div className="theseus__questions">
            <div className="theseus__drawer" onClick={handleClickDrawer}>
              {isFoldDrawer ? <ArrowRightIcon className='theseus__arrow' /> : <ArrowDropDownIcon className='theseus__arrow' />}
              <h5 className='no-margin'>question list</h5>
            </div>
            {!isFoldDrawer && (
             <div className="theseus__list-questions">
                  {listFeatures.map((feature) => (
                    <p 
                    className="theseus__question-text" 
                    key={feature}
                    onClick={handleClickQuestion(feature)}
                    style={feature === selectedQuestion ? { backgroundColor: '#EDA828' } : {}}>
                    {feature}</p>
                  ))}
              </div>
            )}
          </div>
          <button className="theseus__button" onClick={handleClickSend}>Demander</button>
        </div>
      </div>

    </div> 

    )
}

export default Theseus