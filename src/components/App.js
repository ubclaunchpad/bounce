/* eslint-disable no-unused-vars */
import React, { Component } from 'react';
import SignIn from './SignIn';
import Clubs from './Clubs';
import Home from './Home';
import {
    BrowserRouter,
    Switch,
    Route
} from 'react-router-dom';
import '../css/App.css';
import CreateAccount from './CreateAccount';
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
        this.getSignInPage = this.getSignInPage.bind(this);
        this.getCreateAccountPage = this.getCreateAccountPage.bind(this);
        this.getHomePage = this.getHomePage.bind(this);
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

    /**
     * Returns a SignIn component.
     */
    getSignInPage() {
        return <SignIn
            onSignIn={this.onSignIn}
            client={this.props.client}
        />;
    }

    /**
     * Returns a SignIn component that defaults to the CreateAccount form.
     */
    getCreateAccountPage() {
        return <CreateAccount
            onSignIn={this.onSignIn}
            client={this.props.client}
        />;
    }

    getHomePage() {
        return <Home
            isSignedIn={this.state.isSignedIn}
            username={this.state.username}
            isNewAccount={this.state.isNewAccount}
        />;
    }

    render() {
        return (
            <BrowserRouter>
                <Switch>
                    <Route exact path='/' component={this.getHomePage} />
                    <Route path='/sign-in' render={this.getSignInPage} />
                    <Route path='/create-account' render={this.getCreateAccountPage} />
                </Switch>
            </BrowserRouter>
        );
    }
}

export default App;
