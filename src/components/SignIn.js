/* eslint-disable no-unused-vars */
import React, { Component } from 'react';
import { UNAUTHORIZED, SIGNIN_ERROR } from '../constants';
import CreateAccount from './CreateAccount';
import { Redirect } from 'react-router-dom';
/* eslint-enable no-unused-vars */

class SignIn extends Component {
    constructor(props) {
        super(props);
        this.state = {
            isSignedIn: false,
            username: '',
            password: '',
            goToCreateAccount: false,
            errorMsg: undefined,
        };

        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleInput = this.handleInput.bind(this);
        this.handleCreateAccountClick = this.handleCreateAccountClick.bind(this);
    }

    /**
     * Handle the event that occurs when a user clicks the "Sign In" button
     * by authenticating them with the backend.
     * @param {Event} event
     */
    handleSubmit(event) {
        event.preventDefault();
        this.props.client.authenticate(
            this.state.username,
            this.state.password
        ).then(response => {
            // Check if authentication was successful
            if (response.ok) {
                // Trigger a page transition in the parent component
                this.props.onSignIn(false, this.state.username);
                this.setState({ isSignedIn: true });
            } else if (response.status === 401) {
                // The users's credentials are invalid
                this.setState({ errorMsg: UNAUTHORIZED });
            } else {
                // Some unexpected error occurred
                this.setState({ errorMsg: SIGNIN_ERROR });
            }
        }).catch(() => {
            // An error occurred in the browser while handling the request
            this.setState({ errorMsg: SIGNIN_ERROR });
        });
    }

    /**
     * Update this component's state when the user enters his/her credentials.
     * @param {Event} event
     */
    handleInput(event) {
        this.setState({
            [event.target.name]: event.target.value
        });
    }

    /**
     * Triggers a redirect to the CreateAccount page when the user hits the
     * "Create Account" button.
     * @param {Event} event
     */
    handleCreateAccountClick(event) {
        event.preventDefault();
        this.setState({ goToCreateAccount: true });
    }

    render() {
        let buttonClass = 'btn btn-primary';
        if (this.state.isSignedIn) {
            return <Redirect to='/' />;
        } else if (this.state.goToCreateAccount) {
            return <Redirect to='create-account' />;
        } else if (this.state.password === '' && this.state.username === '') {
            buttonClass += ' disabled';
        }
        const error = this.state.errorMsg ? <p>{this.state.errorMsg}</p> : undefined;

        return (
            <div className='container'>
                <form onSubmit={this.handleSubmit}>
                    <h1>Sign In</h1>

                    {error}

                    <div className='form-group'>
                        <label>Username</label>
                        <input type='text'
                            name='username'
                            placeholder='Username'
                            className='form-control'
                            value={this.state.username}
                            onChange={this.handleInput} />
                    </div>

                    <div className='form-group'>
                        <label>Password</label>
                        <input type='password'
                            name='password'
                            placeholder='Password'
                            className='form-control'
                            value={this.state.password}
                            onChange={this.handleInput} />
                    </div>

                    <button className={buttonClass}>Sign In</button>
                    <button
                        onClick={this.handleCreateAccountClick}
                        className='btn btn-secondary'>
                        Create Account
                    </button>
                </form>
            </div>
        );
    }
}

export default SignIn;
