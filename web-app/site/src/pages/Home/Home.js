import React, { Component } from 'react'
import {
  Link,
  withRouter
} from 'react-router-dom'
import styles from './Home.module.css'

class Home extends Component {

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

          <div className='menuContainer'>
            <Link to='/register' className='menuLink'>Register</Link>
            <Link to='/map' className='menuLink'>Map</Link>
            <Link to='/volunteer' className='menuLink'>Volunteer</Link>
            <Link to='/about' className='menuLink'>About</Link>
            <a href='https://twitter.com/vaccinatetexas' target='_blank'>
              <img src={'./twitter-icon.svg'} className='menuIcon' />
            </a>
            <a href='https://github.com/parquar/vaccinate-texas-org' target='_blank'>
              <img src={'./github-icon.svg'} className='menuIcon' />
            </a>
          </div>
          
          { /* Hero Artwork */}
          
          <div className={`${styles.heroTitle}`}>
            <img
              draggable='false'
              src={'./vaccinate_texas.svg'}
              alt='vaccinate-texas-logo'
            />
          </div>

          { /* Hero Description */}

          <div className={`${styles.heroDescription}`}>
            Register to get SMS notifications when COVID vaccines are available in your area. 
          </div>

          { /* Call To Action */}

          <div className={`${styles.containerCta}`}>

            <Link to='/register'>
              <button className={`buttonPrimaryLarge`}>
                Register
              </button>
            </Link>

            {/* <Link to='/login' className={`${styles.linkSignIn}`}>sign-in</Link> */}
          </div>
        </div>
      </div>
    )
  }
}

export default withRouter(Home)