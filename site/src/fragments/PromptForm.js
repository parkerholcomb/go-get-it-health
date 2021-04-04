import React, { Component } from "react";
import axios from 'axios'
import Form from 'react-bootstrap/Form';


export default class PromptForm extends Component {
    constructor(props) {
        super(props);
        this.state = {};
        this.state.phone = '';
        this.state.notification = '';

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

        const results = await axios.post('https://p6ccqa7dik.execute-api.us-east-1.amazonaws.com/dev/sms/prompt', {
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
                <div className='notification-container'>
                    {this.state.notification}
                </div>
                <Form inline className="subscribe-form" onSubmit={this.handleFormSubmit}>
                    <div style={{ flexDirection: "row" }}>
                        <div style={{ border: "1px solid #ced4da", borderRight: "", borderRadius: ".25rem 0 0 .25rem", width: "60px", alignContent: 'center' }}>
                            <img
                                style={{ padding: "15px 10px 10px 10px", height: "50px", filter: "opacity(50%)" }}
                                src="https://vtx-public.s3.amazonaws.com/comment-alt.svg"
                            />
                        </div>

                        <input
                            className="form-control"
                            style={{ borderRadius: '0', maxWidth: "240px", height: "auto" }}
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

                </Form>
            </div>
        );
    }
}