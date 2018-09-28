/* eslint-disable no-unused-vars */
import React, { Component } from 'react';
import { Alert, Button, FormGroup, Label } from 'react-bootstrap';

import {
    EMAIL_WARNING, UNEXPECTED_ERROR, USER_UPDATED
} from '../../constants';
import { validateEmail } from '../utils';
import '../../css/Settings.css';
/* eslint-enable no-unused-vars */

class EmailSettings extends Component {
    constructor(props) {
        super(props);
        this.state = {
            newEmail: '',
            newEmailIsValid: undefined,
            failed: undefined
        };

        this.handleInputChange = this.handleInputChange.bind(this);
        this.handleEmailChangeSubmit = this.handleEmailChangeSubmit.bind(this);
        this.updateEmail = this.updateEmail.bind(this);
    }

    /**
     * If new email is not empty string, validate format of email.
     * Else, return undefined
     * @param {string} newEmail
     */
    handleEmailValidation(newEmail) {
        if (newEmail.length > 0) {
            return validateEmail(newEmail);
        } else {
            return undefined;
        }
    }

    /**
     * Updates the component state when the user types in an input field.
     * @param {Event} event
     */
    handleInputChange(event) {
        const value = event.target.value;
        this.setState({
            [event.target.name]: value,
            newEmailIsValid: this.handleEmailValidation(value),
        });
    }

    /**
     * Update user email and return whether process was successful
     */
    updateEmail() {
        return this.props.client.updateUser(
            this.props.client.getUsername(),
            undefined,
            this.state.newEmail
        ).then(response => {
            if (response.ok) {
                return true;
            } else {
                return false;
            }
        }).catch(() => {
            return false;
        });
    }

    /**
     * Check new email format then update user email address.
     * @param {Event} event
     */
    handleEmailChangeSubmit(event) {
        event.preventDefault();

        const isNewEmailValid = this.handleEmailValidation(this.state.newEmail);
        if (isNewEmailValid) {
            this.updateEmail()
                .then(isUpdated => {
                    this.setState({ failed: !isUpdated });
                });
        } else {
            this.setState({newEmailIsValid: false});
        }
    }

    render() {
        let newEmailWarning, newEmailClass;
        if (this.state.newEmailIsValid !== undefined) {
            if (this.state.newEmailIsValid) {
                newEmailClass = 'has-success';
            } else {
                newEmailClass = 'has-error';
                newEmailWarning = <span>{EMAIL_WARNING}</span>;
            }
        }

        return (
            <div>
                <form onSubmit={this.handleEmailChangeSubmit}>
                    {this.state.failed === true &&
                        <Alert bsStyle='danger'>{UNEXPECTED_ERROR}</Alert>
                    }
                    {this.state.failed === false &&
                        <Alert bsStyle='success'>{USER_UPDATED}</Alert>
                    }
                    <FormGroup bsClass={newEmailClass}>
                        <Label>New Email</Label>
                        <input type='email'
                            name='newEmail'
                            className='form-control'
                            placeholder='New email'
                            value={this.state.newEmail}
                            onChange={this.handleInputChange}
                            autoComplete='new-password' />
                        {newEmailWarning}
                    </FormGroup>
                    <Button bsStyle='primary' type='submit'>Submit</Button>
                </form>
            </div>
        );
    }
}

export default EmailSettings;
