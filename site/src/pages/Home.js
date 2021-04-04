import React, { Component } from 'react';
import {
    Link,
    withRouter
} from 'react-router-dom'
import Nav from '../fragments/Nav'
import PromptForm from '../fragments/PromptForm';

class Home extends Component {

  render() {
    return (
      <div className='container'>
        <Nav/>
        <div className='logoContainer'>
          <img className='mainLogo' src="https://vtx-public.s3.amazonaws.com/go_and_get_it.svg" />
        </div>
        <PromptForm/>
      </div >

    );
  }
}

export default withRouter(Home)