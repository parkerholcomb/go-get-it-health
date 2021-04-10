import React, { Component } from 'react';
import { withRouter } from 'react-router-dom'
import Nav from '../fragments/Nav'
import PromptForm from '../fragments/PromptForm'
import vaccinateImage from '../images/vaccinate.svg'

class About extends Component {
    render() {
        return (
            <div className='container'>
                <Nav />
                <div className="hero">
                    <img src={vaccinateImage} />
                </div>

                <div className="tagline">
                    <span>Made with love by 
                        <a href="https://www.linkedin.com/in/parkerholcomb/" target="_blank"> Parker</a>,
                        <a href="https://www.linkedin.com/in/dwamian/" target="_blank"> Dwamian</a>,
                        <a href="https://www.linkedin.com/in/scott-woolley-wynd-0299072a/" target="_blank"> Scott</a>. 
                    </span>
                </div>
                {/* <PromptForm /> */}
            </div>
        )
    }

}

export default withRouter(About)