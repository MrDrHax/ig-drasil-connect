import React from 'react';
import { Button, Card} from 'react-bootstrap';
import '../Styles/Login.css'; // Importa el archivo CSS para estilos específicos de este componente
import Igdrasil from '../img/ig-drasil.png'; // Importa la imagen de Igdrasil
import TicketMasterLogo from '../img/ticketmaster.svg'; // Importa el logo de TicketMaster
import Ticket from '../img/ticket.svg'; // Importa la imagen de un ticket

// Definición del componente de inicio de sesión
function LogIn() {
  return (
    <div className='Container'> {/* Contenedor principal con clase 'Container' */}
      <div>
          <Card className='leftCard'> {/* Tarjeta izquierda con clase 'leftCard' */}
            <Card.Body>
              <img className='t-logo' src={TicketMasterLogo} alt="TicketMaster Logo"/> {/* Logo de TicketMaster */}
              <img className='ticket' src={Ticket} alt='Ticketmaster Ticket'/> {/* Imagen de un ticket */}
              <Card.Text className='text'> {/* Texto de bienvenida */}
                Welcome Back!
              </Card.Text>
            </Card.Body>
         </Card>
        </div>
         <div>
         <Card className='rightCard'> {/* Tarjeta derecha con clase 'rightCard' */}
            <Card.Body> 
              <Card.Text className='awsText'> {/* Texto de inicio de sesión */}
                Log in here
              </Card.Text>
              {/* Botón de inicio de sesión con imagen */}
              <Button style={{ width:'250px'}} className='button' variant="secondary">
                <img style={{ maxWidth:'auto', height:'auto'}}  className='igdrasil' src={Igdrasil} alt="Igdrasil Logo" />
              </Button>
              <br/>
              <br/>
              <a href="http://">Forgot Password?</a> {/* Enlace para restablecer la contraseña */}
            </Card.Body>
         </Card>
        </div>
      </div>
  );
}

export default LogIn; // Exporta el componente de inicio de sesión
