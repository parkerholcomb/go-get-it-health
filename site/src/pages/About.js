import React, { Component } from 'react';
import {
    Link,
    withRouter
} from 'react-router-dom'
import Nav from '../fragments/Nav'
import PromptForm from '../fragments/PromptForm'

class About extends Component {
    render() {
        return (
            <div className='container'>
                <Nav/>
                <div className='logoContainer'>
                    Test
                </div>
                <PromptForm/>
            </div>
        )
    }

}

export default withRouter(About)