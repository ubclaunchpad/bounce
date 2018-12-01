/* eslint-disable no-unused-vars */
import React, { Component } from 'react';
import { NavLink, BrowserRouter, Redirect } from 'react-router-dom';
import {
    Navbar,
    Nav,
    NavItem,
    FormControl,
    FormGroup,
    Button,
    Glyphicon,
    Image
} from 'react-bootstrap';
import SmallLogo from '../media/small-logo.png';
import '../css/Navbar.css';
import NavbarSignedIn from './NavbarSignedIn';
import NavbarLoggedOut from './NavbarLoggedOut';
/* eslint-enable no-unused-vars */

class BounceNavbar extends Component {
    constructor(props) {
        super(props);
        this.state = {
            goToHome: false,
            goToSignIn: false,
            goToMyClubs: false,
            goToExplore: false,
            signedIn: false,
            query: undefined,
        };

        this.handleLogOut = this.handleLogOut.bind(this);
        this.handleHomeClick = this.handleHomeClick.bind(this);
        this.handleSignInClick = this.handleSignInClick.bind(this);
        this.handleMyClubsClick = this.handleMyClubsClick.bind(this);
        this.handleExploreClick = this.handleExploreClick.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleInput = this.handleInput.bind(this);
    }

    /**
     * Set goTo props to false after component updates so page
     * does not rerender on every component update
     */
    componentDidUpdate() {
        if (this.state.goToHome) {
            this.setState({ goToHome: false });
        }
        if (this.state.goToSignIn) {
            this.setState({ goToSignIn: false });
        }
        if (this.state.goToMyClubs) {
            this.setState({ goToMyClubs: false });
        }
        if (this.state.goToExplore) {
            this.setState({ goToExplore: false });
        }
    }

    /**
     * Set client token to null, allowing navbarComponent to render
     * NavbarLoggedOut instead of NavbarSignedIn
     */
    handleLogOut() {
        this.props.client.signOut();
        this.props.onSearch();
    }

    /**
     * Redirects to the Home page with an empty search query when
     * the Bounce logo is clicked.
     */
    handleHomeClick() {
        this.setState({ goToHome: true });
        this.props.onSearch();
    }

    /**
     * Redirects to Sign In page with an empty search query when
     * Sign In button is clicked.
     */
    handleSignInClick() {
        this.setState({ goToSignIn: true });
        this.props.onSearch();
    }

    /**
     * Redirects to My Club page when
     * My Clubs button is clicked.
     */
    handleMyClubsClick() {
        this.setState({ goToMyClubs: true });
    }

    /**
     * Redirects to Explore page when
     * Explore button is clicked.
     */
    handleExploreClick() {
        this.setState({ goToExplore: true });
    }

    /**
     * Updates component state when the user types in the search bar.
     * @param {Event} event
     */
    handleInput(event) {
        event.preventDefault();
        this.setState({ query: event.target.value });
    }

    /**
     * Searches for clubs when the user hits the search button.
     */
    handleSubmit(event) {
        event.preventDefault();
        // Trigger redirect to Home page so it can display search results
        this.setState({ goToHome: true });
        this.props.onSearch(this.state.query);
    }

    render() {
        let pageRedirect;
        let navbarComponent;
        if (this.state.goToHome) {
            pageRedirect = <Redirect to='/'></Redirect>;
        }
        if (this.state.goToSignIn) {
            pageRedirect = <Redirect to='/sign-in'></Redirect>;
        }
        if (this.state.goToMyClubs) {
            // Stub: direct page to my Clubs
        }
        if (this.state.goToExplore) {
            // Stub: direct page to my Explore
        }

        navbarComponent = this.props.client.isSignedIn() ?
            <NavbarSignedIn
                handleLogOut={this.handleLogOut}
                handleMyClubsClick={this.handleMyClubsClick}
                handleExploreClick={this.handleExploreClick} /> :
            <NavbarLoggedOut
                handleSignInClick={this.handleSignInClick} />;

        return (
            <Navbar id='navbar' toggleNavKey={1} fluid>
                {pageRedirect}
                <Navbar.Header>
                    <BrowserRouter>
                        <NavLink to='/' onClick={this.handleHomeClick}>
                            <Navbar.Brand>
                                <Image src={SmallLogo}></Image>
                            </Navbar.Brand>
                        </NavLink>
                    </BrowserRouter>
                    <Navbar.Toggle />
                </Navbar.Header>
                <Navbar.Collapse>
                    <Nav>
                        <NavItem eventKey={1} href="#">
                            <Navbar.Form>
                                <form>
                                    <FormGroup>
                                        <FormControl
                                            type='text'
                                            placeholder='Search'
                                            onChange={this.handleInput}
                                        />
                                    </FormGroup>
                                    <Button type='submit'>
                                        <Glyphicon
                                            glyph='search'
                                            onClick={this.handleSubmit}>
                                        </Glyphicon>
                                    </Button>
                                </form>
                            </Navbar.Form>
                        </NavItem>
                    </Nav>
                    {navbarComponent}
                </Navbar.Collapse>
            </Navbar>
        );
    }
}

export default BounceNavbar;
