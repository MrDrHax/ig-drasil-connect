import React from 'react';
import { Button, Card} from 'react-bootstrap';
import '../Styles/Login.css';
import AmazonLogo from '../img/aws.svg';
import Keycloak from '../img/keycloak.svg';
import TicketMasterLogo from '../img/ticketmaster.svg';
import Ticket from '../img/ticket.svg';


function LogIn() {
  return (
    <div className='Container'>
      <div>
          <Card className='leftCard'>
            <Card.Body>
              <img className='t-logo' src={TicketMasterLogo} alt="TicketMaster Logo"/>
              <img className='ticket' src={Ticket} alt='Ticketmaster Ticket'/>
              <Card.Text className='text'>
                Welcome Back!
              </Card.Text>
            </Card.Body>
         </Card>
        </div>
         <div>
         <Card className='rightCard'>
            <Card.Body> 
              <Card.Text className='awsText'>
                Log in here
              </Card.Text>
              {/* <Button className='button' variant="secondary"><img className='awsLogo' src={AmazonLogo} alt="Amazon Logo" /></Button> */}
              <Button className='button' variant="secondary"><img className='keycloak' src={Keycloak} alt="Keycloak Logo" /></Button>
              <br/>
              <br/>
              <a href="http://">Forgot Password?</a>
            </Card.Body>
         </Card>
        </div>
      </div>
  );
}

export default LogIn;