import logo from './logo.svg';
import './App.css';
import StartPage from './Components/StartPage'
import EncryptPage from './Components/EncryptPage'
import DecryptPage from "./Components/DecryptPage";
import EncryptedImage from "./Components/EncryptedImage";
import DecryptedText from "./Components/DecryptedText";
import {
    BrowserRouter as Router,
    Switch,
    Route,
    Link
} from "react-router-dom";

import React from "react";


function App() {
  return (
    <div className="App">
        <Router>
            <Switch>
                <Route path="/">
                    <StartPage text="Try our encrypting!"/>
                </Route>
                <Route path="/encrypt">
                    <EncryptPage text="Encrypt your text into the image!" />
                </Route>
                <Route path="/decrypt">
                    <DecryptPage text="Decrypt the text from the image!"/>
                </Route>
                <Route path="/text">
                    <DecryptedText text="Here is the encrypted text!"/>
                </Route>
                <Route path="/image">
                    <EncryptedImage text="Here is the encrypted image!"/>
                </Route>
            </Switch>
        </Router>
    </div>
  );
}

export default App;
