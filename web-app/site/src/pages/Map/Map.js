import React, { Component } from 'react'
import {
  Link,
  withRouter
} from 'react-router-dom'
import styles from './Map.module.css'

class Map extends Component {

  constructor(props) {
    super(props)
    this.state = {}
  }

  async componentDidMount() { }

  render() {

    return (
      <div className={`${styles.container} animateFadeIn`}>
        <div className={styles.containerInner}>
          { /* Main Navigation */}
          <div className='menuLogoContainer'>
            <img
              className='menuLogo'
              src={'./vaccinate_texas.svg'}
              alt='vaccinate-texas-logo'
            />
          </div>
          <div className='menuContainer'>
            <Link to='/' className='menuLink'>Home</Link>
            <Link to='/register' className='menuLink'>Register</Link>
            <Link to='/map' className='menuLink menuLinkActive'>Map</Link>
            <Link to='/volunteer' className='menuLink'>Volunteer</Link>
          </div>


          { /* Put the map here */}
          <iframe 
            className={`${styles.iframeContent}`} 
            src="https://tdem.maps.arcgis.com/apps/webappviewer/index.html?id=3700a84845c5470cb0dc3ddace5c376b"
          />
          
          <a
            href="https://genesis.soc.texas.gov/files/accessibility/vaccineprovideraccessibilitydata.csv" 
            style={{marginTop:'10px'}}
          >
            Download Raw Data
          </a>

        </div>
      </div>
    )
  }
}

export default withRouter(Map)