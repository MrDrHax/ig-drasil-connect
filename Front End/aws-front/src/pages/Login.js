import React from 'react';
import { Button, Form, Card} from 'react-bootstrap';
import '../Styles/Login.css';
import AmazonLogo from '../img/aws.svg';
import TicketMasterLogo from '../img/ticketmaster.svg';


function LogIn() {
  return (
    <div className='Container'>
      <div>
          <Card className='leftCard'>
            <Card.Body>
              <img src={TicketMasterLogo} alt="TicketMaster Logo"/>
              <Card.Text className='text'>
                Welcome Back!
              </Card.Text>
            </Card.Body>
         </Card>
        </div>
         <div>
         <Card className='rightCard'>
            <Card.Body> 
              <Card.Text className='text'>
                Welcome Back!
              </Card.Text>
              <Button variant="primary"><img src={AmazonLogo} alt="Amazon Logo" /></Button>
              <br/>
              <a href="http://">Forgot Password?</a>
            </Card.Body>
         </Card>
        </div>
      </div>
  );
}

export default LogIn;