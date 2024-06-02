import React from "react";
import {Link} from "react-router-dom";

export function Navbar(){
    return (
        <nav className="navbar navbar-expand-lg bg-white border-buttom box-shadow py-3 mb-3 ">
            <div className="container">
                <Link className="navbar-brand" to="/">World of Football</Link>
                <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                <span className="navbar-toggler-icon"></span>
                </button>
                <div className="collapse navbar-collapse" id="navbarSupportedContent">
                <ul className="navbar-nav me-auto mb-2 mb-lg-0">
                    {/* <li className="nav-item">
                    <Link className="nav-link text-dark" aria-current="page" to="/">Home</Link>
                    </li> */}
                    <li className="nav-item">
                    <Link className="nav-link text-dark" to="/player">Players</Link>
                    </li>
                    <li className="nav-item">
                    <Link className="nav-link text-dark" to="/team">Teams</Link>
                    </li>
                    <li className="nav-item">
                    <Link className="nav-link text-dark" to="/chart">Chart</Link>
                    </li>
                </ul>
                </div>
            </div>
        </nav>
    );
}

export function Footer(){
    return (
        <footer className="fixed-bottom bg-body-tertiary text-center text-lg-start mt-auto">
            <div className="text-center p-3" style={{backgroundColor: 'rgba(0, 0, 0, 0.05)'}}>
                © 2024 Copyright: Eduard Eftimie
            </div>
        </footer>
    );
}