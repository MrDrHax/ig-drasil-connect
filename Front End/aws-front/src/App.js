import './App.css';
import  Home  from './pages/Home';
import Login from './pages/Login';
import  Dashboard  from './pages/admin';
import AgentCall from './pages/agentCall';
import { NavBar } from './Componetes/nav-bar';
import {BrowserRouter as Router, Route, Routes as Switch} from "react-router-dom";

function App() {
  return (
    <div className="App">
      <Router>
      <Switch>
        <Route path="/" exact Component={AgentCall}>
        </Route>
      </Switch>
      <Switch>
        <Route path="/dashboard" exact Component={Dashboard}>
        </Route>
      </Switch>
      <Switch>
        <Route path="/login" exact Component={Login}>
        </Route>
      </Switch>
      </Router>
    </div>
  );
}

export default App;
