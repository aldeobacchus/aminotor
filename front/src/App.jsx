import './App.css';
import GameSelection from './components/GameSelection/GameSelection';
import { useState} from 'react';
import Game from './containers/Game/Game';

function App() {

  const [mode, setMode] = useState("home");

  //Callback to select the game
  const onChangeGameMode = (varMode) => {
    console.log("Game mode set to : " + varMode);
    setMode(varMode);
  }

  return (
    <div className="app">


      {mode === 'home' && (
        <>
          <h1 onClick={() => { setMode("home") }}>Aminotor</h1>

          <GameSelection callback={(e) => onChangeGameMode(e)} />
        </>
      )}

      {mode === "Amino'Guess" && (
        <>
          <h3 onClick={() => { setMode("home") }}>Aminotor</h3>
          <Game gm="Amino'Guess" setMode={setMode} />
        </>
      )}

      {mode === 'Ariane' && (
        <>
          <h3 onClick={() => { setMode("home") }}>Aminotor</h3>
          <Game gm="Ariane" setMode={setMode} />
        </>
      )}

      {mode === 'Theseus Battle' && (
        <>
          <h3 onClick={() => { setMode("home") }}>Aminotor</h3>
          <Game gm="Theseus Battle" setMode={setMode} />
        </>
      )
      }


    </div>
  );
}

export default App;