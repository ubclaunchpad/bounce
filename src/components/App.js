/* eslint-disable no-unused-vars */
import React, { Component } from 'react';
import {
    BrowserRouter,
    Switch,
    Route
} from 'react-router-dom';

import SignIn from './SignIn';
import Clubs from './Clubs';
import CreateClub from './CreateClub';
import Home from './Home';
import '../css/App.css';
import CreateAccount from './CreateAccount';
import ViewClub from './ViewClub';
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
        this.getCreateClubPage = this.getCreateClubPage.bind(this);
        this.getViewClubPage = this.getViewClubPage.bind(this);
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

    /**
     * Returns the CreatClub page.
     */
    getCreateClubPage() {
        return <CreateClub client={this.props.client} />;
    }

    /**
     * Returns the ViewClub page.
     * @param {Object} filter provides the club name based on the URI
     */
    getViewClubPage(filter) {
        const name = decodeURIComponent(filter.match.params.name);
        return <ViewClub
            client={this.props.client}
            name={name}
        />;
    }

    /**
     * Returns the Home page.
     */
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
                    <Route path='/create-club' render={this.getCreateClubPage} />
                    <Route path='/clubs/:name' component={this.getViewClubPage} />
                    <Route path='/create-account' render={this.getCreateAccountPage} />
                </Switch>
            </BrowserRouter>
        );
    }
}

export default App;
