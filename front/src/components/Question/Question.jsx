import React from 'react'

function Question({setBoolFind}) {
 
  return (
    <div className='question'>
        <h3>Question : ton personnage fait-il pipi au lit ?</h3>
        <button onClick={() => setBoolFind(true)}>oui</button>
        <button>non</button>
        <button>je ne sais pas trop à vrai dire</button>
    </div>
  )
}

export default Question