import React, { Component } from "react";
import axios from 'axios'
import Form from 'react-bootstrap/Form';


export default class PromptForm extends Component {
    constructor(props) {
        super(props);
        this.state = {};
        this.state.phone = '';
        this.state.notification = 'Updates when vaccines become available in your area.';

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
    }

    async handleFormSubmit(evt) {
        evt.preventDefault()

        console.log(this.state)

        const apiBase = "https://b1n1kqglok.execute-api.us-east-1.amazonaws.com/prod" // todo: set this in process.env
        const promptEndpoint = `${apiBase}/sms/prompt`

        const results = await axios.post(promptEndpoint, {
            phone: this.state['phone'],
        });

        const phone = this.state['phone']
        const nextState = {
            "phone": "",
            "notification": `SMS sent to ${phone}`
        }
        this.setState(Object.assign(this.state, nextState))
        console.log(this.state)
    }


    /**
     * Render
     */

    render() {
        return (
            <div className='formContainer'>

                <Form inline className="subscribe-form" onSubmit={this.handleFormSubmit}>
                    <div style={{ flexDirection: "column" }}>
                        <div className='notification-container'>
                            {this.state.notification}
                        </div>
                        <div style={{ flexDirection: "row" }}>
                            <input
                                className="form-control"
                                style={{ borderRadius: '.25rem 0 0 .25rem', maxWidth: "300px", height: "auto" }}
                                value={this.state.phone}
                                type="tel"
                                placeholder="(512) 555-5555"
                                onChange={(e) => { this.handleFormInput('phone', e.target.value) }}
                            />

                            <button
                                className="btn"
                                style={{ backgroundColor: '#203375', color: 'white', borderRadius: '0 .25rem .25rem 0', borderLeft: "" }}
                            >
                                REGISTER
                        </button>
                        </div>


                    </div>

                </Form>
            </div>
        );
    }
}