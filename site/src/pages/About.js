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
                    Hey y'all, it's time to help our yourself and neighbors and get your vaccine! 
                    But guess what, Joe Biden is not going to show up in your driveway and give you a jab. 
                    You need to lean in, advocate for your health, and #GoGetIt.
                </div>
                <div className="tagline">
                    <span>
                        Our VaccinateTexas bot that monitors over 3,900 locations across Texas, and sends you a SMS notification 
                        whenever new COVID vaccines are available in your area. Our primary source data is from the <a href="https://tdem.maps.arcgis.com/apps/webappviewer/index.html?id=3700a84845c5470cb0dc3ddace5c376b" target="_blank">Texas Division of Emergency Management</a>.    
                    </span> 
                </div>
                <div className="tagline">
                    <span>
                        GoGetIt.Health is an <a href="https://github.com/parquar/go-get-it-health" target="_blank">open-source project</a> not affiliated with any governtment or business - just a few technologists trying to help.
                        If you'd like to get involved, send us a DM or pull request!
                    </span>
                </div>
                <div className="tagline">
                    "Open source you say? What about my data?" Great question. As healthcare engineers, we take data security very seriously.
                    While the code is open source, your data (i.e. your phone number and zip code) is stored in an encrypted S3 bucket, and is accessible only by contributing engineers (three of us currently). 
            
                </div>
                <div className="tagline">
                    
                    <span>Made with love by 
                        <a href="https://www.linkedin.com/in/parkerholcomb/" target="_blank"> Parker</a>, 
                        <a href="https://www.linkedin.com/in/dwamian/" target="_blank"> Dwamian</a>, and 
                        <a href="https://www.linkedin.com/in/scott-woolley-wynd-0299072a/" target="_blank"> Scott</a>. 
                    </span>
                </div>
                {/* <PromptForm /> */}
            </div>
        )
    }

}

export default withRouter(About)