import React, { Component } from 'react';


export default class App extends Component {
  constructor(props) {
    super(props);
    this.state = {};
    this.state.loading = false;
  }

  /**
   * Component Did Mount
   */

  async componentDidMount() { }

  /**
   * Render
   */

  render() {
    return (
      <div>

        {/* menu container */}
        <div className='menuContainer'>
          <img
            className='menuLogo'
            src='https://vtx-public.s3.amazonaws.com/vaccinate_texas.svg'
            alt='vaccinate-texas-logo'
          />
          <div className='menuLinkContainer'>

            <a href='/map' className='menuLink'>Map</a>
            <a href='/volunteer' className='menuLink'>Volunteer</a>
            <a href='/about' className='menuLink'>About</a>
            <a href='https://twitter.com/vaccinatetexas' target='_blank'>
              {/* <img src={'./twitter-icon.svg'} className='menuIcon' /> */}
            </a>
            <a href='https://github.com/parquar/vaccinate-texas-org' target='_blank'>
              <img
                src='https://vtx-public.s3.amazonaws.com/github-icon.svg'
                className='menuIcon'
              />
            </a>
          </div>
        </div>


        {/* home container */}
        <div className="container" id="home">
          <div className="hero">
            <img src="https://vtx-public.s3.amazonaws.com/go_and_get_it.svg" />
          </div>

          <div className="tagline">
            Text your zip code to +15124886383 to get push notifications
          </div>
        </div>

        {/* map container */}
        <div className="containerFull" id="map">
          <iframe
            className="iframeContent"
            src="https://tdem.maps.arcgis.com/apps/webappviewer/index.html?id=3700a84845c5470cb0dc3ddace5c376b"
          />
        </div>

        {/* about container */}
      </div >

    );
  }
}
