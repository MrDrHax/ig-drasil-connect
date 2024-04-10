import React from 'react';
import { Button, Card} from 'react-bootstrap';
import '../Styles/Login.css';
import AmazonLogo from '../img/aws.svg';
import TicketMasterLogo from '../img/ticketmaster.svg';
import Ticket from '../img/ticket.svg';


function LogIn() {
  return (
    <div className='Container'>
      <div>
          <Card className='leftCard'>
            <Card.Header>
            <img className='t-logo' src={TicketMasterLogo} alt="TicketMaster Logo"/>
            </Card.Header>
            <Card.Body>
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
                Sign in with
              </Card.Text>
              <Button variant="secondary"><img className='awsLogo' src={AmazonLogo} alt="Amazon Logo" /></Button>
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