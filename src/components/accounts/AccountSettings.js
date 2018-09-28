/* eslint-disable no-unused-vars */
import React, { Component } from 'react';
import { Alert, PageHeader, Col } from 'react-bootstrap';

import SettingsSidebar from './SettingsSidebar';
import PasswordSettings from './PasswordSettings';
import EmailSettings from './EmailSettings';
import { NOT_SIGNED_IN_ERROR } from '../../constants';
/* eslint-enable no-unused-vars */

class AccountSettings extends Component {
    render() {
        if (!this.props.client.isSignedIn()) {
            return (
                <Alert bsStyle='warning'>{NOT_SIGNED_IN_ERROR}</Alert>
            );
        }
        return (
            <div className='container'>
                <PageHeader>Account Settings</PageHeader>
                <Col sm={3}>
                    <SettingsSidebar />
                </Col>
                <Col>
                    <div className='container'>
                        <PasswordSettings
                            client={this.props.client} />
                        <br />
                        <EmailSettings
                            client={this.props.client} />
                    </div>
                </Col>
            </div>
        );
    }
}

export default AccountSettings;
