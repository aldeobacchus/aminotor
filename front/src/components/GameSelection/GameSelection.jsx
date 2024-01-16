import React from 'react'
import './gameSelection.css'

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
          <div className="param-menu">
            <h2>Paramètres</h2>
            <div className="param-buttons">
              <button className="button-orange white-color inika small-text">Importer une image</button>
              <button className="button-red white-color inika small-text">Supprimer les données</button>
            </div>
            <button className='button-parametres inika' onClick={handleClickParam}>Retour</button>
          </div>
        )
        }
    </div>
  )
}

export default GameSelection