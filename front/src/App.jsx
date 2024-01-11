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


      {mode === 'home' && (
        <>
          <h1 onClick={() => {setMode("home")}}>Aminotor</h1>

          <GameSelection callback={(e) => onChangeGameMode(e)} />
        </>
      )}

      {mode === 'Amino' && (
        <>
          <h3 onClick={() => {setMode("home")}}>Aminotor</h3>
          <Game gm="Amino" setMode={setMode}/>
        </>
      )}

      {mode === 'Theseus' && (
        <>
          <h3 onClick={() => {setMode("home")}}>Aminotor</h3>
          <Game gm="Theseus"/>
        </>
      )}

      
    </div>
  );
}

export default App;