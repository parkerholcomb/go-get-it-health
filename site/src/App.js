import React, { Component } from 'react';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import Col from 'react-bootstrap/Col';
import InputGroup from 'react-bootstrap/InputGroup';
import FormControl from 'react-bootstrap/FormControl';

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

  async handleFormInput() { }

  async handleFormSubmit(evt) {
    evt.preventDefault()

    this.setState({ loading: true })

    // TODO SAVE TO DYNAMO

    // window.location.replace('/')
  }


  /**
   * Render
   */

  render() {
    return (
      <div className='container'>
        <div className='navbar'>

        </div>

        <div className='logoContainer'>
          <img className='mainLogo' src="https://vtx-public.s3.amazonaws.com/go_and_get_it.svg" />
        </div>

        <div className='formContainer'>
          <Form className="subscribe-form">
            <Form.Row className="align-items-centers">
              <Col xs="auto">
                <Form.Label htmlFor="inlineFormInput" srOnly>
                  Name
                </Form.Label>
                <Form.Control
                  className="mb-2"
                  id="inlineFormInput"
                  placeholder="+1 (512) 555-5555"
                />
              </Col>

              <Col xs="auto">
                <Button type="submit" className="mb-2" id="goGetIt-btns">
                  <img
                    className='btn-logo'
                    src='https://vtx-public.s3.amazonaws.com/vaccinate_texas.svg'
                    alt='vaccinate-texas-logo'
                  />
                  GO GET IT
                </Button>
              </Col>
            </Form.Row>
          </Form>
        </div>

      </div >

    );
  }
}
