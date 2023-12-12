import React from 'react'

function GameSelection(args) {  

  return (
    <div className='gs'>
        
        <h1>Select a game mode</h1>

        <div className='gs__buttons'>
            <button className='gs__button' onClick={() => args.callback("Amino")}>Amino's Guess</button>
            <button className='gs__button' onClick={() => args.callback("Theseus")}>Theseus Battle</button>
        </div>
    </div>
  )
}

export default GameSelection