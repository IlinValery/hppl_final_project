import './App.css';
import StartPage from './Components/StartPage'
import EncryptPage from './Components/EncryptPage'
import DecryptPage from "./Components/DecryptPage";
import {
    BrowserRouter as Router,
    Switch,
    Route
} from "react-router-dom";

import React from "react";


function App() {
  return (
    <div className="App">
        <Router>
            <Switch>
                <Route exact path="/">
                    <StartPage text="Try our encrypting!"/>
                </Route>
                <Route exact path="/encrypt">
                    <EncryptPage text="Encrypt your text into the image!" />
                </Route>
                <Route exact path="/decrypt">
                    <DecryptPage text="Decrypt the text from the image!"/>
                </Route>
            </Switch>
        </Router>
    </div>
  );
}

export default App;
