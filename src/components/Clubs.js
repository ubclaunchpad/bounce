/* eslint-disable no-unused-vars */
import React, { Component } from 'react';
/* eslint-enable no-unused-vars */

class Clubs extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        let welcomeMsg;
        if (this.props.isNewAccount) {
            welcomeMsg = <p>Welcome, {this.props.username}!</p>;
        }
        return (
            <div>
                {welcomeMsg}
                <p>I'm a cool club</p>
            </div>
        );
    }
}

export default Clubs;
