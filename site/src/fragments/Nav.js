import React from "react";
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';

import twitterIcon from '../images/twitter.svg'
import githubIcon from '../images/github.svg'
import vaccinateTexasLogo from '../images/vaccinate-texas.svg'


export default function Menu() {
    return (
        <div className='navbar'>
            <Navbar bg="white">
                <Navbar.Brand href="/">
                    <img
                        src={vaccinateTexasLogo}
                        width="70"
                        height="70"
                        className="brand-img"
                        alt="vaccinate-texas-logo"
                    />
                </Navbar.Brand>
                <Navbar.Toggle />
                <Navbar.Collapse>
                    <Nav style={{ alignSelf: 'flex-end' }}>
                        <Nav.Link href="https://tdem.maps.arcgis.com/apps/webappviewer/index.html?id=3700a84845c5470cb0dc3ddace5c376b" target="_blank">MAP</Nav.Link>
                        <Nav.Link href='/about'>ABOUT</Nav.Link>
                        {/* <Nav.Link href='/q'>SEARCH</Nav.Link> */}
                        <a href='https://twitter.com/vaccinatetexas' target='_blank'>
                                <img src={twitterIcon} className='menuIcon' />
                            </a>
                        <a href='https://github.com/parquar/go-get-it-health' target='_blank'>
                            <img src={githubIcon} className='menuIcon' />
                        </a>
                    </Nav>
                </Navbar.Collapse>
            </Navbar>
        </div>
    )
}
