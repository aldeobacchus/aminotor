import logo from './logo.svg';
import './App.css';
import GameSelection from './components/gameSelection/GameSelection';
import { useState } from 'react';
import Game from './containers/Game/Game';

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

      {mode === 'home' && (
        <GameSelection callback={(e) => onChangeGameMode(e)}/>
      )}

      {mode === 'Amino' && (
        <Game gm="Amino"/>
      )}

      {mode === 'Thesus' && (
        <Game gm="Thesus"/>
      )}


    </div>
  );
}

export default App;
