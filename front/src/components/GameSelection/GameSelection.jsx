import React from 'react'
import './gameSelection.css'
import Parameters from '../Parameters/Parameters'

function GameSelection(args) {  
  const [isSelectedParameters, setIsSelectedParameters] = React.useState(true);

  const handleClickParam = event => {
    setIsSelectedParameters(current => !current);
  }

  return (
    
    <div>
        {isSelectedParameters && (
          <div className='gs'>
            <h2>Select a game mode</h2>

            <div className='gs_buttons'>
              <button className='button-orange' onClick={() => args.callback("Amino'Guess")}>Amino'Guess</button>
              <button className='button-blue' onClick={() => args.callback("Theseus Battle")}>Theseus Battle</button>
            </div>

            <button className='button-parametres' onClick={handleClickParam}>Paramètres</button>
          </div>
        )}

        {!isSelectedParameters && (
          <Parameters handleClickParam={handleClickParam}/>
        )
        }
    </div>
  )
}

export default GameSelection