import './App.css';
import React from "react";
import StartPage from './Components/StartPage'
import EncryptPage from './Components/EncryptPage'
import DecryptPage from "./Components/DecryptPage";
import {
    BrowserRouter as Router,
    Switch,
    Route
} from "react-router-dom";

import { library } from '@fortawesome/fontawesome-svg-core'
import { faEye, faEyeSlash } from '@fortawesome/free-solid-svg-icons'

library.add(faEye, faEyeSlash)

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
