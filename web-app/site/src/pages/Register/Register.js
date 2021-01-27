import React, { Component } from 'react'
import {
  Link,
  withRouter,
} from 'react-router-dom'
import styles from './Register.module.css'

class Register extends Component {

  constructor(props) {
    super(props)

    this.state = {}
    this.state.loading = true
    this.state.error = null
    this.state.formPhone = ''
    this.state.formZip = ''

    // Bindings
    this.handleFormInput = this.handleFormInput.bind(this)
    this.handleFormSubmit = this.handleFormSubmit.bind(this)
    this.handleFormTypeChange = this.handleFormTypeChange.bind(this)
  }

  /**
   * Component did mount
   */
  componentDidMount() {
    this.setState({
      loading: false
    })

    // Clear query params
    const url = document.location.href
    window.history.pushState({}, '', url.split('?')[0])
  }

  /**
   * Handles a form change
   */
  handleFormTypeChange(type) {
    this.setState({ state: type },
      () => {
        this.props.history.push(`/${type}`)
      })
  }

  /**
   * Handle text changes within form fields
   */
  handleFormInput(field, value) {
    value = value.trim()

    const nextState = {}
    nextState[field] = value

    this.setState(Object.assign(this.state, nextState))
  }

  /**
   * Handles form submission
   * @param {object} evt 
   */
  async handleFormSubmit(evt) {
    evt.preventDefault()

    this.setState({ loading: true })

    // TODO SAVE TO DYNAMO

    // window.location.replace('/')
  }

  render() {

    return (
      <div className={`${styles.container} animateFadeIn`}>
        <div className={styles.containerInner}>

          <div className='menuLogoContainer'>
            <a href='/'>
              <img
                className='menuLogo'
                src={'./vaccinate_texas.svg'}
                alt='vaccinate-texas-logo'
              />
            </a>

          </div>
          <div className='menuContainer'>
            <Link to='/register' className='menuLink menuLinkActive'>Register</Link>
            <Link to='/map' className='menuLink'>Map</Link>
            <Link to='/volunteer' className='menuLink'>Volunteer</Link>
            <Link to='/about' className='menuLink'>About</Link>
            <a href='https://twitter.com/vaccinatetexas' target='_blank'>
              <img src={'./twitter-icon.svg'} className='menuIcon' />
            </a>
            <a href='https://github.com/parquar/vaccinate-texas-org' target='_blank'>
              <img src={'./github-icon.svg'} className='menuIcon' />
            </a>
          </div>

          { /* Description Here */}

          <div className={`${styles.heroDescription}`}>
            Get daily SMS notifications with local COVID inventory. 
            Please remember that
            <a href='https://www.dshs.state.tx.us/coronavirus/immunize/vaccine.aspx' target="_blank"> eligibility restritions apply.</a>
          </div>
          
          { /* Form */}

          {!this.state.loading && (
            <div className={styles.containerRegister}>

              <form className={styles.form} onSubmit={this.handleFormSubmit}>
                <div className={styles.formField}>
                  <label className={styles.formLabel}>phone</label>
                  <input
                    type='text'
                    placeholder='512-555-5555'
                    className={styles.formInput}
                    value={this.state.formPhone}
                    onChange={(e) => { this.handleFormInput('formPhone', e.target.value) }}
                  />
                </div>
                <div className={styles.formField}>
                  <label className={styles.formLabel}>password</label>
                  <input
                    placeholder='Zip Code'
                    className={styles.formInput}
                    value={this.state.formZip}
                    onChange={(e) => { this.handleFormInput('formZip', e.target.value) }}
                  />
                </div>

                {this.state.formError && (
                  <div className={styles.formError}>{this.state.formError}</div>
                )}

                <input
                  className={`buttonPrimaryLarge ${styles.formButton}`}
                  type='submit'
                  value='Register'
                />

              </form>
            </div>
          )}
        </div>
      </div>
    )
  }
}

export default withRouter(Register)