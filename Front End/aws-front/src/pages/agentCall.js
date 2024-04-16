import React, { useState } from 'react';
import BarChart from '../Componetes/BarChartDan'; // Importa el componente BarChart desde el archivo correspondiente
import '../Styles/agentCall.css'; // Importa el archivo CSS para estilos específicos de este componente

// Definición del componente AgentCall
function AgentCall() {
    const [buttonColor, setButtonColor] = useState('orange'); // Estado para el color del botón

    // Función para manejar el clic del botón y cambiar el color
    const handleClick = () => {
        if (buttonColor === 'orange') {
            setButtonColor('green');
        } else {
            setButtonColor('orange');
        }
    };

    return (
        <div className="principal"> {/* Contenedor principal con clase 'principal' */}
            <div className="izquierda"> {/* Contenedor izquierdo */}
                <div className='user'>
                    <button id="button-user">
                        <svg height="30" viewBox="0 -2 21 21" width="80" xmlns="http://www.w3.org/2000/svg"><g fill="none" fill-rule="evenodd" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" transform="translate(2 2)"><circle cx="8.5" cy="8.5" r="8"/><path d="m14.5 13.5c-.6615287-2.2735217-3.1995581-3.0251263-6-3.0251263-2.72749327 0-5.27073171.8688092-6 3.0251263"/><path d="m8.5 2.5c1.6568542 0 3 1.34314575 3 3v2c0 1.65685425-1.3431458 3-3 3-1.65685425 0-3-1.34314575-3-3v-2c0-1.65685425 1.34314575-3 3-3z"/></g></svg><b>Name</b>
                    </button>
                </div>

                <div className="content-center">
                    {/* Botón de llamada con clase dinámica para animación y color dinámico */}
                    <button className={`pulse ${buttonColor}`} onClick={handleClick}>
                        <i className="fas fa-phone fa-2x"></i>
                    </button>
                </div>

                <div className='supervisor-button'>
                    <button className='supervisor-button-style'>Supervisor<svg height="21" viewBox="0 0 21 21" width="21" xmlns="http://www.w3.org/2000/svg"><g fill="none" fill-rule="evenodd" transform="translate(2 2)"><circle cx="8.5" cy="8.5" r="8" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"/><path d="m8.5 9.5v-1l1.41421356-1.41421356c.37507274-.37507276.58578644-.88378059.58578644-1.41421356v-.17157288c0-.61286606-.3462631-1.17313156-.89442719-1.4472136l-.21114562-.1055728c-.56305498-.2815275-1.2257994-.2815275-1.78885438 0l-.10557281.0527864c-.61286606.30643303-1 .9328289-1 1.61803399v.88196601" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"/><circle cx="8.5" cy="12.5" fill="currentColor" r="1"/></g></svg></button>
                </div>
            </div>
            <div className="derecha"> {/* Contenedor derecho */}
                <div id="nav-bar"> {/* Barra de navegación */}
                    <button className='button-nav'>Supervisor</button>
                    <button className='button-nav'>Reports</button>
                    <button className='button-nav'>Calls</button>
                </div>
                <div className="container">
                    <div>
                        {/* Icono e información */}
                        <svg height="21" viewBox="0 0 21 21" width="21" xmlns="http://www.w3.org/2000/svg"><g fill="none" fill-rule="evenodd" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" transform="translate(2 2)"><circle cx="8.5" cy="8.5" r="8"/><path d="m14.5 13.5c-.6615287-2.2735217-3.1995581-3.0251263-6-3.0251263-2.72749327 0-5.27073171.8688092-6 3.0251263"/><path d="m8.5 2.5c1.6568542 0 3 1.34314575 3 3v2c0 1.65685425-1.3431458 3-3 3-1.65685425 0-3-1.34314575-3-3v-2c0-1.65685425 1.34314575-3 3-3z"/></g></svg><b>Information</b>
                    </div>
                </div>
                <div className='container'>
                    <div>
                        {/* Icono y notas */}
                        <svg height="21" viewBox="0 0 21 21" width="21" xmlns="http://www.w3.org/2000/svg"><g fill="none" fill-rule="evenodd" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" transform="translate(4 3)"><path d="m3.5 1.5c-.42139382 0-1.08806048 0-2 0-.55228475 0-1 .44771525-1 1v11c0 .5522848.44771525 1 1 1h10c.5522847 0 1-.4477152 1-1v-11c0-.55228475-.4477153-1-1-1-.8888889 0-1.55555556 0-2 0"/><path d="m4.5.5h4c.55228475 0 1 .44771525 1 1s-.44771525 1-1 1h-4c-.55228475 0-1-.44771525-1-1s.44771525-1 1-1z"/><path d="m5.5 5.5h5"/><path d="m5.5 8.5h5"/><path d="m5.5 11.5h5"/><path d="m2.5 5.5h1"/><path d="m2.5 8.5h1"/><path d="m2.5 11.5h1"/></g></svg><b>Notes</b>
                    </div>
                </div>
                <div className='container'>
                    <div>
                        {/* Icono y métricas */}
                        <svg height="21" viewBox="0 0 21 21" width="21" xmlns="http://www.w3.org/2000/svg"><g fill="none" fill-rule="evenodd" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" transform="translate(3 3)"><path d="m.5.5v12c0 1.1045695.8954305 2 2 2h11.5"/><path d="m3.5 8.5v3"/><path d="m7.5 5.5v6"/><path d="m11.5 2.5v9"/></g></svg><b>Metrics</b>
                    </div>
                    <div className='chart-bar'>
                        {/* Gráfico de barras */}
                        <BarChart
                            data={{
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
                </div>
            </div>    
        </div>
    );
}

export default AgentCall; // Exporta el componente AgentCall
