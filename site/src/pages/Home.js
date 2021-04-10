import React, { Component } from 'react';
import {withRouter} from 'react-router-dom'
import Nav from '../fragments/Nav'
import PromptForm from '../fragments/PromptForm';
import go_and_get_it from '../images/go_and_get_it.svg'

class Home extends Component {

  render() {
    return (
      <div className='container'>
        <Nav/>
        <div className='logoContainer'>
          <img className='mainLogo' src={go_and_get_it} />
        </div>
        <PromptForm/>
      </div >

    );
  }
}

export default withRouter(Home)