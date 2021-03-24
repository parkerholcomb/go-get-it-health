import React, { Component } from 'react';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import FormControl from 'react-bootstrap/FormControl';
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
              <Nav className="mr-auto vtx-navbar">
                <Nav.Link href="#todo">ABOUT</Nav.Link>
                <Nav.Link href="#todo">BLOG</Nav.Link>
              </Nav>
              
              
            </Navbar.Collapse>
          </Navbar>
        </div>

        <div className='logoContainer'>
          <img className='mainLogo' src="https://vtx-public.s3.amazonaws.com/go_and_get_it.svg" />
        </div>

        <div className='formContainer'>
          <Form inline className="subscribe-form" onSubmit={this.handleFormSubmit}>
            <FormControl
              type="text"
              placeholder="Mobile Number"
              className=" mr-sm-2"
              onChange={(e) => { this.handleFormInput('phone', e.target.value) }}
            />
            <Button type="submit" id="goGetIt-btn">
              GO GET IT
              </Button>
          </Form>
        </div>

      </div >

    );
  }
}
