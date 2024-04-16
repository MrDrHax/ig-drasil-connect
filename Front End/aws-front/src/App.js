import './App.css';
import Home from './pages/Home'; // Importa el componente de la página de inicio
import Login from './pages/Login'; // Importa el componente de la página de inicio de sesión
import Dashboard from './pages/admin'; // Importa el componente del dashboard del administrador
import AgentCall from './pages/agentCall'; // Importa el componente del dashboard del agente
import { BrowserRouter as Router, Route, Switch } from "react-router-dom"; // Importa componentes de React Router

function App() {
  return (
    <div className="App">
      <Router> {/* Componente Router para envolver la aplicación */}
        <Switch> {/* Componente Switch para asegurar que solo se renderice una ruta a la vez */}
          <Route path="/" exact component={Home} /> {/* Ruta para la página de inicio */}
          <Route path="/adminDashboard" exact component={Dashboard} /> {/* Ruta para el dashboard del administrador */}
          <Route path="/agentDashboard" exact component={AgentCall} /> {/* Ruta para el dashboard del agente */}
          <Route path="/login" exact component={Login} /> {/* Ruta para la página de inicio de sesión */}
        </Switch>
      </Router>
    </div>
  );
}

export default App;
