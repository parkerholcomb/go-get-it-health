import React, { Component } from 'react';
import Form from 'react-bootstrap/Form';
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import { sendPrompt } from './utils/api';


export default class App extends Component {
  constructor(props) {
    super(props);
    this.state = {};
    this.state.phone = '';

    this.handleFormInput = this.handleFormInput.bind(this)
    this.handleFormSubmit = this.handleFormSubmit.bind(this)
  }

  /**
   * Component Did Mount
   */

  async componentDidMount() { }

  handleFormInput(field, value) {
    value = value.trim()

    const nextState = {}
    nextState[field] = value

    this.setState(Object.assign(this.state, nextState))
    // console.log(this.state)
  }


  async handleFormSubmit(evt) {
    evt.preventDefault()

    console.log(this.state)



    resp = await sendPrompt(this.state['phone'])
    console.log(resp)
  }


  /**
   * Render
   */

  render() {
    return (
      <div className='container'>
        <div className='navbar'>
          <Navbar bg="white">
            <Navbar.Brand href="#home">
              <img
                src="https://vtx-public.s3.amazonaws.com/vaccinate_texas_border.svg"
                width="70"
                height="70"
                className="d-inline-block align-top"
                alt="vaccinate-texas-logo"
              />
            </Navbar.Brand>
            <Navbar.Toggle />
            <Navbar.Collapse className="justify-content-end">
              <Nav style={{alignSelf: 'flex-end'}}>
                <Nav.Link href="https://tdem.maps.arcgis.com/apps/webappviewer/index.html?id=3700a84845c5470cb0dc3ddace5c376b" target="_blank">MAP</Nav.Link>
                <Nav.Link href="#todo">ABOUT</Nav.Link>
              </Nav>


            </Navbar.Collapse>
          </Navbar>
        </div>

        <div className='logoContainer'>
          <img className='mainLogo' src="https://vtx-public.s3.amazonaws.com/go_and_get_it.svg" />
        </div>

        <div className='formContainer'>
          <Form inline className="subscribe-form" onSubmit={this.handleFormSubmit}>
            <div style={{flexDirection: "row"}}>
              <div style={{border: "1px solid #ced4da", borderRight: "", borderRadius: ".25rem 0 0 .25rem", width: "60px", alignContent:'center'}}>
                <img 
                  style={{padding: "15px 10px 10px 10px", height: "50px", filter: "opacity(50%)"}}
                  src="https://vtx-public.s3.amazonaws.com/comment-alt.svg" 
                />
              </div>

              <input 
                className="form-control" 
                style={{borderRadius: '0', width: "240px"}}
                placeholder="(512) 555-5555"
                onChange={(e) => { this.handleFormInput('phone', e.target.value) }}
              />

              <button 
                className="btn"
                style={{backgroundColor: '#203375', color: 'white', borderRadius: '0 .25rem .25rem 0'}}
              >
                SUBSCRIBE
              </button>

            </div>

          </Form>
        </div>

      </div >

    );
  }
}
