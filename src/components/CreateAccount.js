/* eslint-disable no-unused-vars */
import React, { Component } from 'react';
import '../css/CreateAccount.css';
/* eslint-enable no-unused-vars */

// Error messages to display to the user
const invalidInfoMsg = 'Your information meets the specified requirements.';
const usernameOrEmailTaken = 'We\'re sorry, that username or email is already taken';
const createAccountFailureMsg = 'Oops, something went wrong creating your account. ' +
    'Please try again later';

class CreateAccount extends Component {
    constructor(props) {
        super(props);
        this.state = {
            fullName: '',
            username: '',
            email: '',
            password: '',
            errorMsg: undefined,
        };

        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleInputChange = this.handleInputChange.bind(this);
    }

    /**
     * Handles the event that occurs when a user hits submit on the "Create
     * Account" form by attempting to create the new account.
     * @param {Event} event
     */
    handleSubmit(event) {
        event.preventDefault();
        this.props.client.createUser(
            this.state.fullName,
            this.state.username,
            this.state.password,
            this.state.email
        ).then(response => {
            if (response.ok) {
                // Trigger authentication on the parent component so the user
                // is signed in and can use the app
                this.props.onCreateAccount(this.state.username, this.state.password);
            } else if (response.status === 400) {
                // The users's info is invalid
                this.setState({ errorMsg: invalidInfoMsg });
            } else if (response.status === 409) {
                // The username or email is already taken
                this.setState({ errorMsg: usernameOrEmailTaken });
            } else {
                // Some unexpected error occurred
                this.setState({ errorMsg: createAccountFailureMsg });
            }
        }).catch(() => {
            // An error occurred in the browser while handling the request
            this.setState({ errorMsg: createAccountFailureMsg });
        });
    }

    /**
     * Updates the component state when the user types in an input field.
     * @param {Event} event
     */
    handleInputChange(event) {
        this.setState({
            [event.target.name]: event.target.value
        });
    }

    render() {
        let errorMsg;
        if (this.state.errorMsg) {
            errorMsg = <p> {this.state.errorMsg} </p>;
        }

        return (
            <div className="CreateAccountForm">
                <form onSubmit={this.handleSubmit}>
                    <h1 className="formInput">Create an account</h1>

                    {errorMsg}

                    <label className="inputLabel formInput">Your Name</label>
                    <input type="text" name="fullName"
                        className="formInput"
                        id="fullName"
                        value={this.state.fullName}
                        onChange={this.handleInputChange} />

                    <label className="inputLabel formInput">Your username</label>
                    <input type="text" name="username"
                        className="formInput"
                        id="username"
                        value={this.state.username}
                        onChange={this.handleInputChange} />

                    <label className="inputLabel formInput">Your Email</label>
                    <input type="text" name="email"
                        className="formInput"
                        id="email"
                        value={this.state.email}
                        onChange={this.handleInputChange} />

                    <label className="inputLabel formInput">Your Password</label>
                    <input type="password" name="password"
                        className="formInput"
                        id="password"
                        value={this.state.password}
                        onChange={this.handleInputChange} />

                    <button>Create Account</button>

                </form>
            </div>
        );
    }
}

export default CreateAccount;
