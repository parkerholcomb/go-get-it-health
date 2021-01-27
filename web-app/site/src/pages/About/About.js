import React, { Component } from 'react'
import {
  Link,
  withRouter
} from 'react-router-dom'
import styles from './About.module.css'

class About extends Component {

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
            <Link to='/map' className='menuLink'>Map</Link>
            <Link to='/volunteer' className='menuLink'>Volunteer</Link>
            <Link to='/about' className='menuLink menuLinkActive'>About</Link>
            <a href='https://twitter.com/vaccinatetexas' target='_blank'>
              <img src={'./twitter-icon.svg'} className='menuIcon' />
            </a>
            <a href='https://github.com/parquar/vaccinate-texas-org' target='_blank'>
              <img src={'./github-icon.svg'} className='menuIcon' />
            </a>
          </div>

          { /* About */}
          <div className={`${styles.heroArtwork}`}>
            <img
              draggable='false'
              src={'./go_and_get_it.svg'}
              alt='go-and-get-it'
            />
          </div>

          { /* Hero Description */}

          <div className={`${styles.heroDescription}`}>
            Just trying to find my Dad a vaccine.
            
          </div>



        </div>
      </div>
    )
  }
}

export default withRouter(About)