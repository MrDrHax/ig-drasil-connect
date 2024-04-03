import './App.css';
import  Home  from './pages/Home';
import { NavBar } from './Componetes/nav-bar';
import {BrowserRouter as Router, Route, Routes as Switch} from "react-router-dom";

function App() {
  return (
    <div className="App">
      <Router>
      <NavBar/>
      <Switch>
        <Route path="/" exact Component={Home}>
        </Route>
      </Switch>
      </Router>
    </div>
  );
}


export default App;
