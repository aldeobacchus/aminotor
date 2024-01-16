import React from 'react'
import './Theseus.css'

function Theseus(args) {

  console.log("args in Theseus:", args);
  return (
    
    <div className="game_theseus">
      <h2> This content is unavailable for now</h2>
      <h2> Please come back later</h2>
      <div className="button">
        <button onClick={() => args.setMode("home")}>Menu principal</button>
      </div>
    </div> 

    )
}

export default Theseus