import './App.css';
import  Home  from './pages/Home';
import AgentCall from './pages/agentCall';
import { NavBar } from './Componetes/nav-bar';
import {BrowserRouter as Router, Route, Routes as Switch} from "react-router-dom";

function App() {
  return (
    <div className="App">
      <Router>
      <NavBar/>
      <Switch>
        <Route path="/" exact Component={AgentCall}>
        </Route>
      </Switch>
      </Router>
    </div>
  );
}


export default App;
