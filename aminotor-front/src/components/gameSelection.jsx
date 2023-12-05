import React from 'react'

function GameSelection() {
  return (
    <div className='gs'>
        <h1>Aminotor</h1>
        <h1>Select a game mode</h1>

        <div className='gs__buttons'>
            <button className='gs__button'>Amino's Guess</button>
            <button className='gs__button'>Thesus Battle</button>
        </div>
    </div>
  )
}

export default GameSelection