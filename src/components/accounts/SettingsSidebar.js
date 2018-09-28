/* eslint-disable no-unused-vars */
import React, { Component } from 'react';
import '../../css/Settings.css';
/* eslint-enable no-unused-vars */

class SettingsSidebar extends Component {
    constructor(props) {
        super(props);
        this.state = {
            currentSelected: '',
        };
    }

    render() {
        return (
            <div className='settings-sidebar'>
                <ul>
                    <li><a>Account Settings</a></li>
                    <li><a>Privacy</a></li>
                </ul>
            </div>
        );
    }
}

export default SettingsSidebar;
