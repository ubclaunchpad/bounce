/* eslint-disable no-unused-vars */
import React, { Component } from 'react';
import '../css/App.css';
import SignIn from './SignIn';
import Clubs from './Clubs';
/* eslint-enable no-unused-vars */

class App extends Component {
    constructor(props) {
        super(props);
        this.state = {
            signedIn: false,
            newAccount: false,
            username: undefined,
        };

        this.onSignIn = this.onSignIn.bind(this);
    }

    /**
     * Updates the state to indicate that the user is signed in.
     * @param {Boolean} newAccount whether or not this account was just created
     * @param {String} username
     */
    onSignIn(newAccount, username) {
        this.setState({
            signedIn: true,
            newAccount: newAccount,
            username: username,
        });
    }

    render() {
        if (this.state.signedIn) {
            return <Clubs
                client={this.props.client}
                newAccount={this.state.newAccount}
                username={this.state.username}
            />;
        }
        return <SignIn onSignIn={this.onSignIn} client={this.props.client} />;
    }
}

export default App;
