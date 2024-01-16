import React from 'react'
import './gameSelection.css'

function GameSelection(args) {  

  return (
    <div className='gs'>
        
        <h2>Select a game mode</h2>

        <div className='gs_buttons'>
            <button className='button-orange' onClick={() => args.callback("Amino'Guess")}>Amino'Guess</button>
            <button className='button-blue' onClick={() => args.callback("Theseus Battle")}>Theseus Battle</button>
        </div>
    </div>
  )
}

export default GameSelection