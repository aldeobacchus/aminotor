import './App.css';
import GameSelection from './components/GameSelection/GameSelection';
import { useState } from 'react';
import Game from './containers/Game/Game';
import Test from './containers/Test/Test';

function App() {
  
  const [mode, setMode] = useState("home");

  //Callback to select the game
  const onChangeGameMode = (varMode) =>{
    console.log("Game mode set to : " + varMode);
    setMode(varMode);
  }

  return (
    <div className="app">

      <button onClick={() => {setMode("home")}}>home</button>
      <h1>Aminotor</h1>

      {mode === 'home' && (
        <>
          <GameSelection callback={(e) => onChangeGameMode(e)} />
        </>
      )}

      {mode === 'Amino' && (
        <Game gm="Amino"/>
      )}

      {mode === 'Theseus' && (
        <Game gm="Theseus"/>
      )}

      
    </div>
  );
}

export default App;
