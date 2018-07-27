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
        };

        this.onSignIn = this.onSignIn.bind(this);
    }

    /**
     * Updates the state to indicate that the user is signed in.
     */
    onSignIn() {
        this.setState({ signedIn: true });
    }

    render() {
        if (this.state.signedIn) {
            return <Clubs client={this.props.client} />;
        }
        return <SignIn onSignIn={this.onSignIn} client={this.props.client} />;
    }
}

export default App;
