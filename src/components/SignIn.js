/* eslint-disable no-unused-vars */
import React, { Component } from 'react';
import '../css/SignIn.css';
import CreateAccount from './CreateAccount';
/* eslint-enable no-unused-vars */

// Error messages to display to the user
const unauthorizedMsg = 'Invalid username or password';
const signInErrorMsg = 'Oops! Something went wrong during sign-in. ' +
    'Please try again later.';

class SignIn extends Component {
    constructor(props) {
        super(props);
        this.state = {
            username: undefined,
            password: undefined,
            errorMsg: undefined,
            accountCreated: true,
        };

        this.handleSubmit = this.handleSubmit.bind(this);
        this.getErrorSection = this.getErrorSection.bind(this);
        this.handleInput = this.handleInput.bind(this);
        this.handleSignIn = this.handleSignIn.bind(this);
        this.onCreateAccount = this.onCreateAccount.bind(this);
        this.handleCreateAccountClick = this.handleCreateAccountClick.bind(this);
    }

    /**
     * Handle the event that occurs when a user clicks the "Sign In" button
     * by authenticating them with the backend.
     * @param {Event} event
     */
    handleSubmit(event) {
        event.preventDefault();
        this.handleSignIn();
    }

    /**
     * Authenticates the user with the back-end.
     */
    handleSignIn() {
        this.props.client.authenticate(
            this.state.username,
            this.state.password
        ).then(response => {
            // Check if authentication was successful
            if (response.ok) {
                // Trigger a page transition in the parent component
                this.props.onSignIn();
            } else if (response.status === 401) {
                // The users's credentials are invalid
                this.setState({ errorMsg: unauthorizedMsg });
            } else {
                // Some unexpected error occurred
                this.setState({ errorMsg: signInErrorMsg });
            }
        }).catch(() => {
            // An error occurred in the browser while handling the request
            this.setState({ errorMsg: signInErrorMsg });
        });
    }

    /**
     * Authenticates the user with the given credentials. Called to
     * automatically sign a user in when they create their account.
     * @param {String} username
     * @param {String} password
     */
    onCreateAccount(username, password) {
        this.setState({ username: username, password: password });
        this.handleSignIn();
    }

    /**
     * Return a section with an error message in it if the last sign-in was
     * unsuccessful, otherwise return nothing.
     */
    getErrorSection() {
        if (this.state.errorMsg) {
            return <p> {this.state.errorMsg} </p>;
        }
        return undefined;
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
     * Triggers a page re-render so the user is shown the create account page.
     * @param {Event} event
     */
    handleCreateAccountClick(event) {
        this.setState({ accountCreated: false });
    }

    render() {
        if (!this.state.accountCreated) {
            return <CreateAccount client={this.props.client} />;
        }
        return (
            <div className='UserSignIn'>
                <form onSubmit={this.handleSubmit}>
                    <h1 className='signinComponent'>Sign In</h1>
                    {this.getErrorSection()}

                    <input type='text' name='username'
                        placeholder='Username'
                        className='signinComponent'
                        value={this.state.username}
                        onChange={this.handleInput} />

                    <input type='password' name='password'
                        placeholder='Password'
                        className='signinComponent'
                        value={this.state.password}
                        onChange={this.handleInput} />

                    <button>Sign In</button>
                    <button onClick={this.handleCreateAccountClick}>Create Account</button>
                </form>
            </div>
        );
    }
}

export default SignIn;
