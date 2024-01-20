import React, { useEffect } from 'react'
import './Theseus.css'
import ArrowRightIcon from '@mui/icons-material/ArrowRight';
import ArrowDropDownIcon from '@mui/icons-material/ArrowDropDown';
import axios from 'axios';

function Theseus(args) {

  const [squaresToDisplay, setSquaresToDisplay] = React.useState(args.grid);
  const [isFoldDrawer, setIsFoldDrawer] = React.useState(true);
  const [listFeatures, setListFeatures] = React.useState([]);

  console.log("args in Theseus:", args);
  
  useEffect(() => {
    const fetchData = async () => {
      if(listFeatures.length === 0) {
        const response = await axios.get('http://127.0.0.1:5000/api2/start');
        console.log(response)
        const value = await response.data.list_features;
        console.log("value:", value);

        //remove all null values
        value.forEach((item, index) => {
          if(item === null) {
            value.splice(index, 1);
          }
        });
        console.log("value without null:", value);
        setListFeatures(value);
        console.log("listFeatures:", listFeatures);

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
      const fetchData = async () => {
        const response = await axios.get('http://127.0.0.1:api2/features');
      }
    }
  }



  return (
    
    <div className="theseus">
      
      <div className="theseus__game">
        <div key={24} className="theseus__board">
          {squaresToDisplay.map((square) => (
            <img 
              className='theseus-square-img'
              key={square} 
              src={`https://etud.insa-toulouse.fr/~alami-mejjat/${square}.jpg`}
              alt={`${square}`}
            />
          ))}
        </div>
        <div className="theseus__actions">
          <div className="theseus__questions">
            <div className="theseus__drawer" onClick={handleClickDrawer}>
              {isFoldDrawer ? <ArrowRightIcon className='theseus__arrow' /> : <ArrowDropDownIcon className='theseus__arrow' />}
              <h5 className='no-margin'>question list</h5>
            </div>
            {!isFoldDrawer && (
             <div className="theseus__list-questions">
                  {listFeatures.map((feature) => (
                    <p className="theseus__question-text" onClick={handleClickQuestion(feature)}>{feature}</p>
                  ))}
              </div>
            )}
          </div>
          <button className="theseus__button">Ask question</button>
        </div>
      </div>

    </div> 

    )
}

export default Theseus