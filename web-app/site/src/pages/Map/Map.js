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
          <div className={`${styles.mapMenuContainer}`}>
            <div className='menuLogoContainer'>
              <a href='/'>
                <img
                  className='menuLogo'
                  src={'./vaccinate_texas.svg'}
                  alt='vaccinate-texas-logo'
                />
              </a>
            </div>
            <div className='menuContainer'>
              <Link to='/register' className='menuLink'>Register</Link>
              <Link to='/map' className='menuLink menuLinkActive'>Map</Link>
              <Link to='/volunteer' className='menuLink'>Volunteer</Link>
              <Link to='/about' className='menuLink'>About</Link>
              <a href='https://twitter.com/vaccinatetexas' target='_blank'>
              <img src={'./twitter-icon.svg'} className='menuIcon' />
            </a>
            <a href='https://github.com/parquar/vaccinate-texas-org' target='_blank'>
              <img src={'./github-icon.svg'} className='menuIcon' />
            </a>
            </div>
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