import React from "react";
import "../Styles/nav-bar.css";
import { Link } from "react-router-dom";



export default function NavBar() {
    return (
        <div className="navbar">
            <div className="leftside">
            </div>
            <div className="rightside">
            <Link to="/">Home</Link>
            <Link to="/Dashboard">Dashboard</Link>
            <Link to="/LogIn">Log In</Link>
            <Link to="/Contact">Contact</Link>
            </div>
        </div>   
    );
}