import React from "react";
import "./header.css";
import { Link } from "react-router-dom";

function Header() {
    return (
        <header className="header">
            <div className="nav-container">
                <Link to="/" className="logo">
                    doazhu<span>.pro</span>
                </Link>
                <nav>
                    <ul className="nav-list">
                        <li><Link to="/" className="link">Home</Link></li>
                        <li><Link to="/about" className="link">About</Link></li>
                        <li><Link to="/work" className="link">Work</Link></li>
                        <li><Link to="/contact" className="link">Contact</Link></li>
                    </ul>
                </nav>
            </div>
        </header>
    );
}

export default Header;
