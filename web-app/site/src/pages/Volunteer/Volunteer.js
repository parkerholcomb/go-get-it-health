import React, { Component } from 'react'
import {
  Link,
  withRouter
} from 'react-router-dom'
import styles from './Volunteer.module.css'

class Volunteer extends Component {

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
            <Link to='/map' className='menuLink'>Map</Link>
            <Link to='/volunteer' className='menuLink menuLinkActive'>Volunteer</Link>
          </div>


          { /* Put the volunteer form here */}
          <iframe className={`${styles.iframeContent}`} src="https://airtable.com/embed/shrXQTHXF90RYhiLG?backgroundColor=blue"></iframe>

          
          
        </div>
      </div>
    )
  }
}

export default withRouter(Volunteer)