/* eslint-disable no-unused-vars */
import React, { Component } from 'react';
import { Redirect } from 'react-router-dom';
import {
    Alert,
    Button,
    FormGroup,
    Label,
    PageHeader,
} from 'react-bootstrap';

import {
    EMAIL_WARNING,
    INVALID_INFO,
    PASSWORD_WARNING,
    UNEXPECTED_ERROR,
    USERNAME_OR_EMAIL_TAKEN,
    USERNAME_WARNING,
} from '../constants';
/* eslint-enable no-unused-vars */

class CreateAccount extends Component {
    constructor(props) {
        super(props);
        this.state = {
            fullName: '',
            username: '',
            email: '',
            password: '',
            usernameIsValid: undefined,
            emailIsValid: undefined,
            passwordIsValid: undefined,
            goToSignIn: false,
            isSignedIn: false,
            errorMsg: undefined,
        };

        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleInput = this.handleInput.bind(this);
        this.handleSignInClick = this.handleSignInClick.bind(this);
        this.signIn = this.signIn.bind(this);
    }

    /**
     * Handles the event that occurs when a user hits submit on the 'Create
     * Account' form by attempting to create the new account.
     * @param {Event} event
     */
    handleSubmit(event) {
        event.preventDefault();
        if (!this.state.usernameIsValid
            || !this.state.emailIsValid
            || !this.state.passwordIsValid) {
            // At least one of the inputs is not valid, so do nothing
            return;
        }
        this.props.client.createUser(
            this.state.fullName,
            this.state.username,
            this.state.password,
            this.state.email
        ).then(response => {
            if (response.ok) {
                // Automatically sign the user in after creating their account
                this.signIn();
            } else if (response.status === 400) {
                // The users's info is invalid
                this.setState({ errorMsg: INVALID_INFO });
            } else if (response.status === 409) {
                // The username or email is already taken
                this.setState({ errorMsg: USERNAME_OR_EMAIL_TAKEN });
            } else {
                // Some unexpected error occurred
                this.setState({ errorMsg: UNEXPECTED_ERROR });
            }
        }).catch(() => {
            // An error occurred in the browser while handling the request
            this.setState({ errorMsg: UNEXPECTED_ERROR });
        });
    }

    /**
     * Signs the user in after account creation.
     */
    signIn() {
        this.props.client.authenticate(this.state.username, this.state.password)
            .then(response => {
                if (response.ok) {
                    // Notifiy the parent component that account creation and
                    // sign-in are complete
                    this.props.onSignIn(true, this.state.username);
                    this.setState({ isSignedIn: true });
                } else {
                    // Trigger a redirect to the SignIn page if the account
                    // creation was successful but the sign-in failed
                    this.setState({ goToSignIn: true });
                }
            });
    }

    /**
     * Updates the component state when the user types in an input field.
     * @param {Event} event
     */
    handleInput(event) {
        // Make sure the value matches the requirements for its field
        const value = event.target.value;
        switch (event.target.name) {
        case 'username':
            this.setState({
                'usernameIsValid': this.validateUsername(value)
            });
            break;
        case 'email':
            this.setState({
                'emailIsValid': this.validateEmail(value)
            });
            break;
        case 'password':
            this.setState({
                'passwordIsValid': this.validatePassword(value)
            });
            break;
        }

        this.setState({
            [event.target.name]: value,
        });
    }

    /**
     * Returns true if the username is valid and false otherwise
     * @param {String} username
     */
    validateUsername(username) {
        if (username.length < 3 || username.length > 20) {
            return false;
        }
        const regexes = [
            /[A-Z]+/,
            /[a-z]+/,
            /[0-9]+/,
            /[.\-_]+/
        ];
        for (let i in regexes) {
            let match = username.match(regexes[i]);
            while (match !== null) {
                username = username.replace(match[0], '');
                match = username.match(regexes[i]);
            }
        }
        return username.length === 0;
    }

    /**
     * Returns true if the password is valid and false otherwise
     * @param {String} password
     */
    validatePassword(password) {
        if (password.length < 8) {
            return false;
        }
        const regexes = [
            /[A-Z]+/,
            /[a-z]+/,
            /[0-9]+/,
            /[.\-!@#$%^&*?_+ ]+/
        ];
        for (let i in regexes) {
            let match = password.match(regexes[i]);
            let count = 0;
            while (match !== null) {
                password = password.replace(match[0], '');
                match = password.match(regexes[i]);
                count++;
            }
            if (count === 0) {
                return false;
            }
        }
        return password.length === 0;
    }

    /**
     * Returns true if the email is valid and false otherwise
     * @param {String} email
     */
    validateEmail(email) {
        const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return re.test(email.toLowerCase());
    }

    /**
     * Triggers a redirect to the SignIn page when the user hits the
     * "Sign In" button.
     * @param {Event} event
     */
    handleSignInClick(event) {
        event.preventDefault();
        this.setState({ goToSignIn: true });
    }

    render() {
        if (this.state.isSignedIn) {
            return <Redirect to='/' />;
        } else if (this.state.goToSignIn) {
            return <Redirect to='/sign-in' />;
        }

        let errorMsg, usernameWarning, emailWarning, passwordWarning;
        let usernameClass, emailClass, passwordClass;

        // Display error message if there is one
        if (this.state.errorMsg) {
            errorMsg = <Alert bsStyle='warning'> {this.state.errorMsg} </Alert>;
        }
        // Disable submit button if input is invalid
        const submitDisabled = (
            !this.state.usernameIsValid ||
            !this.state.passwordIsValid ||
            !this.state.emailIsValid);
        // Signal the validity of each input if it's been filled in
        if (this.state.usernameIsValid !== undefined) {
            if (this.state.usernameIsValid) {
                usernameClass = 'has-success';
            } else {
                usernameClass = 'has-error';
                usernameWarning = <span>{USERNAME_WARNING}</span>;
            }
        }
        if (this.state.emailIsValid !== undefined) {
            if (this.state.emailIsValid) {
                emailClass = 'has-success';
            } else {
                emailClass = 'has-error';
                emailWarning = <span>{EMAIL_WARNING}</span>;
            }
        }
        if (this.state.passwordIsValid !== undefined) {
            if (this.state.passwordIsValid) {
                passwordClass = 'has-success';
            } else {
                passwordClass = 'has-error';
                passwordWarning = <span>{PASSWORD_WARNING}</span>;
            }
        }

        return (
            <div className='container'>

                <PageHeader>Create an Account</PageHeader>
                {errorMsg}

                <form onSubmit={this.handleSubmit}>
                    <FormGroup>
                        <Label>Name</Label>
                        <input type='text'
                            name='fullName'
                            placeholder='Name'
                            className='form-control'
                            value={this.state.fullName}
                            onChange={this.handleInput} />
                    </FormGroup>

                    <FormGroup bsClass={usernameClass}>
                        <Label>Username</Label>
                        <input type='text'
                            name='username'
                            placeholder='Username'
                            className='form-control'
                            value={this.state.username}
                            onChange={this.handleInput} />
                        {usernameWarning}
                    </FormGroup>

                    <FormGroup bsClass={emailClass}>
                        <Label>Email</Label>
                        <input type='text'
                            name='email'
                            placeholder='Email'
                            className='form-control'
                            value={this.state.email}
                            onChange={this.handleInput} />
                        {emailWarning}
                    </FormGroup>

                    <FormGroup bsClass={passwordClass}>
                        <Label>Password</Label>
                        <input type='password'
                            name='password'
                            placeholder='Password'
                            className='form-control'
                            value={this.state.password}
                            onChange={this.handleInput} />
                        {passwordWarning}
                    </FormGroup>

                    <br />
                    <Button
                        bsStyle='primary'
                        disabled={submitDisabled}
                        onClick={this.handleSubmit}
                    >
                        Create Account
                    </Button>
                    <Button
                        bsClass='btn btn-secondary'
                        onClick={this.handleSignInClick}
                    >
                        Sign In
                    </Button>
                </form>
            </div>
        );
    }
}

export default CreateAccount;
