import React from 'react'
import Question from '../../components/question/Question'

function Game(args) {
  return (
    <div className='game'>
      
      {args.gm === 'Amino' && (
        <h1>Amino's Guess</h1>  
      )}

      {args.gm === 'Thesus' && (
        <h1>Thesus Battle</h1>  
      )}
      
    </div>
  )
}

export default Game