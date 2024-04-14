import React, { useState } from 'react';
import '../Styles/NavBar.css'; // Archivo de estilos para la barra de navegación
import BarChart from '../Componetes/BarChart';  
import PieChart from '../Componetes/PieChart';

export default function NavBar() {
  // Estado para almacenar qué pestaña está activa
  const [activeTab, setActiveTab] = useState('Name');

  // Función para cambiar la pestaña activa cuando se hace clic en un elemento de la barra de navegación
  const handleTabClick = (tabName) => {
    setActiveTab(tabName);
  };

  return (
    <div>
      {/* Barra de navegación */}
      <div className="navbarAdmin">
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


        {activeTab === 'Messages' && <div>Contenido de la pestaña Messages</div>}
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