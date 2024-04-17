import React, { useState } from 'react';
import '../Styles/NavBar.css'; // Archivo de estilos para la barra de navegación
import { Link } from "react-router-dom"; //Importamos Link para poder redirigir hacia las diferentes páginas
import BarChart from '../Componetes/BarChart';  
import PieChart from '../Componetes/PieChart';
import AmazonLogo from '../img/home.svg'; 

export default function NavBar() {
  // Estado para almacenar qué pestaña está activa
  const [activeTab, setActiveTab] = useState('Name');

  // Función para cambiar la pestaña activa cuando se hace clic en un elemento de la barra de navegación
  const handleTabClick = (tabName) => {
    setActiveTab(tabName);
  };

  // Estado para almacenar el agente seleccionado en los mensajes
  const [selectedAgent, setSelectedAgent] = useState(null);

  // Función para cambiar de agente cuando se hace clic
  const handleAgentClick = (agent) => {
    setSelectedAgent(agent);
  };

  return (
    <div>
      {/* Barra de navegación */}
      <div className="navbarAdmin">
      <Link //Se crea el link hacia Home desde la barra de navegación (ícono de la casa)
          to="/"
          className={`navitemAdmin ${activeTab === 'Home' ? 'active' : ''}`}
          onClick={() => handleTabClick('Home')}
        >
          {/* Icono de casa */}
          <img className='navbaricon' src={AmazonLogo} alt="Home" />
        </Link>
        <div /* Barra de navegación sección de name que se expandirá para cuando haya llamadas */
          className={`navitemAdmin ${activeTab === 'Name' ? 'active' : ''}`}
          onClick={() => handleTabClick('Name')}
        >
          Name
        </div>
        <div /* Barra de navegación de team */
          className={`nav-itemAdmin ${activeTab === 'Team' ? 'active' : ''}`}
          onClick={() => handleTabClick('Team')}
        >
          Team
        </div>
        <div /* Barra de navegación sección de mensajes (pendiente) */
          className={`navitemAdmin ${activeTab === 'Messages' ? 'active' : ''}`}
          onClick={() => handleTabClick('Messages')}
        >
          Messages
        </div>
        <div /* Barra de navegación sección de reportes*/
          className={`navitemAdmin ${activeTab === 'Reports' ? 'active' : ''}`}
          onClick={() => handleTabClick('Reports')}
        >
          Reports
        </div>
        <div /* Barra de navegación sección de llamadas */
          className={`navitemAdmin ${activeTab === 'Calls' ? 'active' : ''}`}
          onClick={() => handleTabClick('Calls')}
        >
          Calls
        </div>
      </div>

       {/* Contenido de la pestaña activa */}
       <div className="tab-contentAdmin">
        {activeTab === 'Name' && <div>Contenido de la pestaña Name</div>}
        {activeTab === 'Team' && 
  <div className="team-container" /* contenido de team, gráficas y resumen */> 
    <div className="metrics-section" /* gráficas */>
      <BarChart
       data={{ /* Cambiar cuando haya data, bar chart */
         labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
         datasets: [{
           label: 'Sales',
           data: [50, 60, 70, 80, 90, 100, 110],
           backgroundColor: 'rgba(54, 162, 235, 0.5)', // Color de fondo de las barras
           borderColor: 'rgba(54, 162, 235, 1)', // Color del borde de las barras
           borderWidth: 1,
          }]
        }}
      />

      <PieChart
       data={{ /* Cambiar cuando haya data, pie chart */
         labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
         datasets: [{
           label: 'Sales',
           data: [50, 60, 70, 80, 90, 100, 110],
           backgroundColor: 'rgba(54, 162, 235, 0.5)', // Color de fondo de las barras
           borderColor: 'rgba(54, 162, 235, 1)', // Color del borde de las barras
           borderWidth: 1,
          }]
        }}
      />
    </div>

    {/* Sección 2: Filas de texto, botones y espaciadores */}
    <div className="generalData">
      <div className="generalData-container"
      /* los botones de view more llevan a un pop-up con información de llamadas para una visualización mejor */>
        <h2>General Data</h2>
        
        <div> 
          Agents in call: 38
        </div>
        <br />
        <button>View more</button>
        <br />
        <div>
          Agents in break: 5
        </div>
        <br />
        <button>View more</button>
        <br />
        <div>
          Agents unoccupied: 7
        </div>
        <br />
        <button>View more</button>
        <br />
        <div>
          Agents that need help: 3
        </div>
        <br />
        <button>View more</button>
        <br />
      </div>
    </div>
  </div>
}


{activeTab === 'Messages' && (
  <div className="messages-container">
    {/* Agent list on the left */}
    <div className="agent-list">
      {Array.from({ length: 10 }, (_, index) => index + 1).map(agent => (
        <div key={agent} className={`agent-item ${selectedAgent === agent ? 'active' : ''}`} onClick={() => handleAgentClick(agent)}>
          Agent {agent}
        </div>
      ))}
    </div>

    {/* Chat content on the right */}
    <div className="chat-content">
      {selectedAgent ? (
        <div>
          <h3>Chat for Agent {selectedAgent}</h3>
          {/* Replace this with actual chat component */}
          <div>Chat content for Agent {selectedAgent} goes here...</div>
        </div>
      ) : (
        <div>Select an agent to start chatting</div>
      )}
    </div>
  </div>
)}

        {activeTab === 'Reports' && /* Sección de reportes data a cambiar con queries */
        
        <div className="calls-container"/*Hereda el formato y media queries de calls*/ >
    <div className="calls-table">
    <div class="table-container">
  <table>
    <tbody>
      <tr>
        <th colSpan="1">Agent</th>
        <th colSpan="1">Status</th>
        <th colSpan="1">Asked for help</th>
        <th colSpan="1">Enter call</th>
      </tr>
      <tr>
        <td colSpan="1">Agent 1</td>
        <td colSpan="1">In a call</td>
        <td colSpan="1">No</td>
        <td colSpan="1"><button>Enter call</button></td>
      </tr>
      <tr>
        <td colSpan="1">Agent 2</td>
        <td colSpan="1">In a call</td>
        <td colSpan="1">No</td>
        <td colSpan="1"><button>Enter call</button></td>
      </tr>
      <tr>
        <td colSpan="1">Agent 3</td>
        <td colSpan="1">In a call</td>
        <td colSpan="1">No</td>
        <td colSpan="1"><button>Enter call</button></td>
      </tr>
      <tr>
        <td colSpan="1">Agent 4</td>
        <td colSpan="1">In a call</td>
        <td colSpan="1">Yes</td>
        <td colSpan="1"><button>Enter call</button></td>
      </tr>
      <tr>
        <td colSpan="1">Agent 5</td>
        <td colSpan="1">In a call</td>
        <td colSpan="1">No</td>
        <td colSpan="1"><button>Enter call</button></td>
      </tr>
      <tr>
        <td colSpan="1">Agent 6</td>
        <td colSpan="1">In a call</td>
        <td colSpan="1">Yes</td>
        <td colSpan="1"><button>Enter call</button></td>
      </tr>
      <tr>
        <td colSpan="1">Agent 7</td>
        <td colSpan="1">In a call</td>
        <td colSpan="1">No</td>
        <td colSpan="1"><button>Enter call</button></td>
      </tr>
      <tr>
        <td colSpan="1">Agent 8</td>
        <td colSpan="1">In a call</td>
        <td colSpan="1">No</td>
        <td colSpan="1"><button>Enter call</button></td>
      </tr>
    </tbody>
  </table>
</div>

    </div>
  </div>}


        {activeTab === 'Calls' && /* Sección de calls que también se va a cambair con la data */
  <div className="calls-container">
    <div className="calls-table">
    <div class="table-container">
  <table>
    <tbody>
      <tr>
        <th colSpan="1">Call Status</th>
        <th colSpan="1">Day</th>
        <th colSpan="1">Week</th>
      </tr>
      <tr>
        <td colSpan="1">Completed</td>
        <td colSpan="1">10</td>
        <td colSpan="1">10</td>
      </tr>
      <tr>
        <td colSpan="1">Not Completed</td>
        <td colSpan="1">8</td>
        <td colSpan="1">10</td>
      </tr>
      <tr>
        <td colSpan="1">Supervisor intervention</td>
        <td colSpan="1">0</td>
        <td colSpan="1">10</td>
      </tr>
      <tr>
        <td colSpan="1">Client Stressed</td>
        <td colSpan="1">3</td>
        <td colSpan="1">10</td>
      </tr>
    </tbody>
  </table>
</div>

    </div>
  </div>
}

      </div>
    </div>
  );
}