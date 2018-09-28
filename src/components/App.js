/* eslint-disable no-unused-vars */
import React, { Component } from 'react';
import {
    BrowserRouter,
    Switch,
    Route,
    Redirect,
} from 'react-router-dom';

import SignIn from './accounts/SignIn';
import BounceNavbar from './Navbar';
import Home from './Home';
import ViewClub from './clubs/ViewClub';
import CreateAccount from './accounts/CreateAccount';
import CreateClub from './clubs/CreateClub';
import '../css/App.css';
import AccountSettings from './accounts/AccountSettings';
/* eslint-enable no-unused-vars */

class App extends Component {
    constructor(props) {
        super(props);
        this.state = {
            isNewAccount: false,
            searchQuery: undefined,
        };

        this.onSignIn = this.onSignIn.bind(this);
        this.getSignInPage = this.getSignInPage.bind(this);
        this.getCreateAccountPage = this.getCreateAccountPage.bind(this);
        this.getCreateClubPage = this.getCreateClubPage.bind(this);
        this.getViewClubPage = this.getViewClubPage.bind(this);
        this.getHomePage = this.getHomePage.bind(this);
        this.onSearch = this.onSearch.bind(this);
        this.getAccountSettingsPage = this.getAccountSettingsPage.bind(this);
    }

    /**
     * Updates the state to indicate that the user is signed in.
     * @param {Boolean} isNewAccount whether or not this account was just created
     */
    onSignIn(isNewAccount) {
        this.setState({isNewAccount: isNewAccount});
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
            isNewAccount={this.state.isNewAccount}
            client={this.props.client}
            searchQuery={this.state.searchQuery}
        />;
    }

    /**
     * Stores the search query as component state.
     * @param {String} query
     */
    onSearch(query) {
        this.setState({ searchQuery: query });
    }

    /**
     * Returns an AccountSettings page.
     */
    getAccountSettingsPage() {
        return <AccountSettings
            client={this.props.client}
        />;
    }

    render() {
        return (
            <BrowserRouter>
                <div>
                    <BounceNavbar
                        client={this.props.client}
                        onSearch={this.onSearch}
                    />
                    <Switch>
                        <Route exact path='/' render={this.getHomePage} />
                        <Route path='/sign-in' render={this.getSignInPage} />
                        <Route path='/create-club' render={this.getCreateClubPage} />
                        <Route path='/clubs/:name' component={this.getViewClubPage} />
                        <Route path='/create-account' render={this.getCreateAccountPage} />
                        <Route path='/account-settings' render={this.getAccountSettingsPage} />
                        <Route path='*' render={() => <Redirect to='/' />} />
                    </Switch>
                </div>
            </BrowserRouter>
        );
    }
}

export default App;
