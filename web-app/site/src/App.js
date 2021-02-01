import React, { Component } from 'react'
import {
  BrowserRouter as Router,
  Switch,
  Route,
} from 'react-router-dom'
import Map from './pages/Map/Map'
import Home from './pages/Home/Home'
import Volunteer from './pages/Volunteer/Volunteer'
import Register from './pages/Register/Register'
import About from './pages/About/About'

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

          <Route path='/register'>
            <Register />
          </Route>

          <Route path='/unsubscribe'>
            <Register />
          </Route>

          <Route path='/map'>
            <Map />
          </Route>

          <Route path='/volunteer'>
            <Volunteer />
          </Route>

          <Route path='/about'>
            <About />
          </Route>

        </Switch>
      </Router>
    )
  }
}

/**
 * A component to protect routes.
 * Shows Auth page if the user is not authenticated
 */
// const PrivateRoute = ({ component, ...options }) => {

//   const session = getSession()

//   const finalComponent = session ? Dashboard : Home
//   return <Route {...options} component={finalComponent} />
// }