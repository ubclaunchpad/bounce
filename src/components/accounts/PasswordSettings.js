/* eslint-disable no-unused-vars */
import React, { Component } from 'react';
import { Button, Label, FormGroup } from 'react-bootstrap';

import { validatePassword } from '../utils';
import {
    PASSWORD_WARNING,
    VERIFY_PASSWORD_ERROR,
    INCORRECT_PASSWORD_WARNING,
    PASSWORD_CHANGE_ERROR,
    PASSWORD_CHANGE_UNSUCCESSFUL,
    PASSWORD_CHANGE_SUCCESSFUL
} from '../../constants';
import '../../css/Settings.css';
/* eslint-enable no-unused-vars */

class PasswordSettings extends Component {
    constructor(props) {
        super(props);
        this.state = {
            currentPassword: '',
            newPassword: '',
            newPasswordReentry: '',
            currentPasswordIsValid: undefined,
            newPasswordIsValid: undefined,
            newPasswordReentryIsValid: undefined,
            isPasswordChangeSuccessful: undefined,
            passwordChangeMessage: undefined
        };

        this.validatePasswordReentry = this.validatePasswordReentry.bind(this);
        this.handleInputChange = this.handleInputChange.bind(this);
        this.validateCurrentPassword = this.validateCurrentPassword.bind(this);
        this.handlePasswordChangeSubmit = this.handlePasswordChangeSubmit.bind(this);
        this.updatePassword = this.updatePassword.bind(this);
    }

    /**
     * If password reentry is not empty string,
     * check if password reentry is same as new password.
     * Else, return false
     */
    validatePasswordReentry(passwordReentryInput, passwordInput) {
        let newPassword = passwordInput || this.state.newPassword;
        if (passwordReentryInput.length > 0) {
            return passwordReentryInput === newPassword;
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

        let isNewPasswordValid = this.state.newPasswordIsValid;
        let isNewPasswordReentryValid = this.state.newPasswordReentryIsValid;

        switch (event.target.name) {
        case 'newPassword':
            isNewPasswordValid = validatePassword(value);
            isNewPasswordReentryValid = this.validatePasswordReentry(this.state.newPasswordReentry, value);
            break;
        case 'newPasswordReentry':
            isNewPasswordReentryValid = this.validatePasswordReentry(value);
            break;
        default:
            break;
        }

        this.setState({
            [event.target.name]: value,
            newPasswordIsValid: isNewPasswordValid,
            newPasswordReentryIsValid: isNewPasswordReentryValid
        });
    }

    /**
     * Return true if user input current password correctly
     */
    validateCurrentPassword(password) {
        return this.props.client.authenticate(
            this.props.client.getUsername(),
            password
        ).then(response => {
            if (response.ok) {
                return true;
            } else if (response.status === 401) {
                return false;
            } else {
                return undefined;
            }
        }).catch(() => {
            return undefined;
        });
    }

    /**
     * Update user password and return whether process was successful
     */
    updatePassword() {
        // Stub
        return true;
    }

    /**
     * Revalidate password inputs.
     * If there is undefined or false states, set password inputs to empty.
     * @param {Event} event
     */
    handlePasswordChangeSubmit(event) {
        event.preventDefault();

        let isPasswordValid;
        const isNewPasswordValid = this.handlePasswordValidation(this.state.newPassword);
        let isNewPasswordReentryValid = this.validatePasswordReentry(this.state.newPasswordReentry);
        let isPasswordChangeSuccessful;
        let passwordChangeMessage;

        if (isNewPasswordValid && isNewPasswordReentryValid) {
            this.validateCurrentPassword(this.state.currentPassword)
                .then(isVerify => {
                    if (isVerify === true) {
                        isPasswordValid = true;
                        return this.updatePassword();
                    } else if (isVerify === false) {
                        isPasswordValid = false;
                        passwordChangeMessage = PASSWORD_CHANGE_UNSUCCESSFUL;
                        return false;
                    } else {
                        isPasswordValid = undefined;
                        passwordChangeMessage = VERIFY_PASSWORD_ERROR;
                        return false;
                    }
                })
                .then(isUpdated => {
                    if (isUpdated === true) {
                        passwordChangeMessage = PASSWORD_CHANGE_SUCCESSFUL;
                        isPasswordChangeSuccessful = true;
                    } else {
                        if (!passwordChangeMessage) {
                            passwordChangeMessage = PASSWORD_CHANGE_ERROR;
                        }
                        isPasswordChangeSuccessful = false;
                    }
                })
                .then(() => {
                    this.setState({
                        'currentPasswordIsValid': isPasswordValid,
                        'newPasswordIsValid': isNewPasswordValid,
                        'newPasswordReentryIsValid': isNewPasswordReentryValid,
                        'currentPassword': '',
                        'newPassword': '',
                        'newPasswordReentry': '',
                        'isPasswordChangeSuccessful': isPasswordChangeSuccessful,
                        'passwordChangeMessage': passwordChangeMessage
                    });
                });
        } else {
            isPasswordValid = undefined;
            isPasswordChangeSuccessful = false;
            passwordChangeMessage = PASSWORD_CHANGE_UNSUCCESSFUL;
            if (isNewPasswordValid === false) {
                isNewPasswordReentryValid = undefined;
            }

            this.setState({
                'currentPasswordIsValid': isPasswordValid,
                'newPasswordIsValid': isNewPasswordValid,
                'newPasswordReentryIsValid': isNewPasswordReentryValid,
                'currentPassword': '',
                'newPassword': '',
                'newPasswordReentry': '',
                'isPasswordChangeSuccessful': isPasswordChangeSuccessful,
                'passwordChangeMessage': passwordChangeMessage
            });
        }
    }

    render() {
        let newPasswordWarning, passwordConfirmationWarning;
        let passwordConfirmationClass, newPasswordClass;

        if (this.state.newPasswordIsValid !== undefined) {
            if (this.state.newPasswordIsValid) {
                newPasswordClass = 'has-success';
            } else {
                newPasswordClass = 'has-error';
                newPasswordWarning = <span>{PASSWORD_WARNING}</span>;
            }
        }

        if (this.state.newPasswordReentryIsValid !== undefined) {
            if (this.state.newPasswordReentryIsValid) {
                passwordConfirmationClass = 'has-success';
            } else {
                passwordConfirmationClass = 'has-error';
                passwordConfirmationWarning = <span>{'Retyped password does not match new password'}</span>;
            }
        }

        return (
            <div>
                <form onSubmit={this.handlePasswordChangeSubmit}>
                    <FormGroup>
                        <Label>Current Password</Label>
                        <input type='password'
                            name='currentPassword'
                            className='form-control'
                            placeholder='Current password'
                            value={this.state.currentPassword}
                            onChange={this.handleInputChange} />
                    </FormGroup>

                    <FormGroup bsClass={newPasswordClass}>
                        <Label>New Password</Label>
                        <input type='password'
                            name='newPassword'
                            className='form-control'
                            placeholder='New password'
                            value={this.state.newPassword}
                            onChange={this.handleInputChange} />
                        {newPasswordWarning}
                    </FormGroup>

                    <Label>Confirm New Password</Label>
                    <FormGroup bsClass={passwordConfirmationClass}>
                        <input type='password'
                            name='newPasswordReentry'
                            className='form-control'
                            placeholder='Retype new password'
                            value={this.state.newPasswordReentry}
                            onChange={this.handleInputChange} />
                        {passwordConfirmationWarning}
                    </FormGroup>

                    <Button bsStyle='primary'>Submit</Button>
                </form>
            </div>
        );
    }
}

export default PasswordSettings;
