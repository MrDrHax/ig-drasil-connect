import React from "react";
import "../Styles/nav-bar.css";
import { Link } from "react-router-dom";
// import {Nav, Navbar} from 'react-bootstrap';

export default function NavBar() {
    return (
        <div className="navbar">
            <div className="leftside">
            </div>
            <div className="rightside">
            <Link className="link" to="/">Home</Link>
            <Link className="link" to="/adminDashboard">Admin Dashboard</Link>
            <Link className="link" to="/agentDashboard">Agent Dashboard</Link>
            <Link className="link" to="/login">Log In</Link>
            <Link className="link" to="/Contact">Contact</Link>
            </div>
        </div>   
    );
}