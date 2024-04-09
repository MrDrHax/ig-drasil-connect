import React from 'react';
import { Button, Form, Card} from 'react-bootstrap';
import '../Styles/LogIn.css';
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
              <Button variant="primary">Go somewhere</Button>
            </Card.Body>
         </Card>
        </div>
         <div>
          <Form className='rightForm'>
            <img src={AmazonLogo} alt="Amazon Logo" />
            <Form.Group className="mb-3" controlId="formBasicEmail">
              <Form.Label>Email address</Form.Label>
              <Form.Control type="email" placeholder="Enter email" style={{padding:"2px"}} />
              <Form.Text className="text-muted">
                We'll never share your email with anyone else.
              </Form.Text>
            </Form.Group>
            <Form.Group className="mb-3" controlId="formBasicPassword">
              <Form.Label>Password</Form.Label>
              <Form.Control size='sm' type="password" placeholder="Password" />
            </Form.Group>
            <Button variant="primary" type="submit">
              Sign In
            </Button>
          </Form>
        </div>
      </div>
  );
}

export default LogIn;