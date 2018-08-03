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
            isSignedIn: false,
            isNewAccount: false,
            username: undefined,
        };

        this.onSignIn = this.onSignIn.bind(this);
    }

    /**
     * Updates the state to indicate that the user is signed in.
     * @param {Boolean} isNewAccount whether or not this account was just created
     * @param {String} username
     */
    onSignIn(isNewAccount, username) {
        this.setState({
            isSignedIn: true,
            isNewAccount: isNewAccount,
            username: username,
        });
    }

    render() {
        if (this.state.isSignedIn) {
            return (
                <Clubs
                    client={this.props.client}
                    isNewAccount={this.state.isNewAccount}
                    username={this.state.username}
                />
            );
        }
        return (
            <SignIn
                onSignIn={this.onSignIn}
                client={this.props.client}
            />
        );
    }
}

export default App;
