/* eslint-disable no-unused-vars */
import React, { Component } from 'react';
import { Link, Redirect } from 'react-router-dom';
import {
    Nav,
    NavItem,
    NavDropdown,
    MenuItem,
    Button,
    Image
} from 'react-bootstrap';
import '../css/Navbar.css';
import UserDefaultLogo from '../media/user-default-logo.png';
/* eslint-enable no-unused-vars */

class NavbarSignedIn extends Component {
    constructor() {
        super();
        this.state = {
            goToSettings: false,
            goToProfile: false
        };

        this.handleSettingsClick = this.handleSettingsClick.bind(this);
    }

    componentDidUpdate() {
        if (this.state.goToSettings) {
            this.setState({ goToSettings: false });
        }
    }

    handleSettingsClick() {
        this.setState({ goToSettings: true });
    }

    render() {
        let pageRedirect;
        if (this.state.goToSettings) {
            pageRedirect = <Redirect to='/account-settings'></Redirect>;
        }

        return (
            <div>
                {pageRedirect}
                <Nav pullRight>
                    <NavItem eventKey={1} href="#"
                        className="navButton">
                        <Button
                            bsClass='btn btn-secondary'
                            onClick={this.props.handleMyClubsClick}>
                            My Clubs
                        </Button>
                    </NavItem>
                    <NavItem eventKey={2} href="#"
                        className="navButton">
                        <Button
                            bsClass='btn btn-secondary'
                            onClick={this.props.handleExploreClick}>
                            Explore
                        </Button>
                    </NavItem>
                    <NavDropdown
                        eventKey={3}
                        title={
                            <div className="accountButton">
                                <Image src={UserDefaultLogo}/>
                                <span>Account</span>
                            </div>
                        } 
                        id="profile-dropdown" >
                        <MenuItem eventKey={3.1} href=''>Profile</MenuItem>
                        <MenuItem 
                            eventKey={3.2}
                            onClick={this.handleSettingsClick}>
                            Settings
                        </MenuItem>
                        <MenuItem divider />
                        <MenuItem 
                            eventKey={3.3}
                            onClick={this.props.handleLogOut}>
                                Log Out
                        </MenuItem>
                    </NavDropdown>
                </Nav>
            </div>
        );
    }
}

export default NavbarSignedIn;
