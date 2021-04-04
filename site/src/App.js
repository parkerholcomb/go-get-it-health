import React, { Component } from 'react'
import {
  BrowserRouter as Router,
  Switch,
  Route,
} from 'react-router-dom'
import Home from './pages/Home'
import About from './pages/About'

export default class App extends Component {

  constructor(props) {
    super(props)
    this.state = {}
  }

  async componentDidMount() {
    // console.log(getSession())
  }

  render() {
    return (
      <Router>
        <Switch>

          <Route exact path='/'>
            <Home />
          </Route>

          <Route path='/about'>
            <About />
          </Route>

        </Switch>
      </Router>
    )
  }
}