/* eslint-disable no-unused-vars */
import React, { Component } from 'react';
/* eslint-enable no-unused-vars */

class Clubs extends Component {
    constructor(props) {
        super(props);
        // TODO: fetch and display clubs the user might be intersted in
    }

    render() {
        let welcomeMsg;
        if (this.props.newAccount) {
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
